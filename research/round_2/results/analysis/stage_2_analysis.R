## stage_2_analysis.R
## Phân tích thống kê các alpha Stage 2 từ backtest/results_stage_2.csv
## + Layer 3 diagnostics (factor_diagnostics.csv) + Layer 4 validation (economic_validation.csv)
##
## Yêu cầu: R >= 4.0 (chỉ dùng base R, không cần package ngoài)
## Chạy:   Rscript backtest/stage_2_analysis.R
## Kết quả: in ra console + ghi các CSV vào backtest/out_analysis/

## =====================================================================
## 0. Config
## =====================================================================

## --- Tìm thư mục chứa dữ liệu (backtest/) một cách bền vững ---------
## Nguồn ứng viên (theo thứ tự ưu tiên):
##   1) thư mục chứa script  (Rscript <path>/stage_2_analysis.R -> --file=)
##   2) thư mục của file khi dùng source() trong R console (sys.frame()$ofile)
##   3) thư mục làm việc hiện tại (getwd())
## Sau đó dò ngược lên các cấp cha (dirname) tối đa 8 tầng để tìm
## backtest/results_stage_2.csv — luôn dùng scalar, không tạo vector.

(setwd('D:/01_Workspace/02_Finance_Trading/Alpha_bot'))
find_base <- function() {
  candidates <- character(0)

  args <- commandArgs(trailingOnly = FALSE)
  f <- sub("^--file=", "", args[grepl("^--file=", args)])
  if (length(f) > 0 && nzchar(f)) candidates <- c(candidates, dirname(normalizePath(f)))

  of <- tryCatch(sys.frame(1)$ofile, error = function(e) NULL)
  if (!is.null(of) && nzchar(of)) candidates <- c(candidates, dirname(normalizePath(of)))

  candidates <- c(candidates, getwd())

  for (c in unique(candidates)) {
    d <- suppressWarnings(tryCatch(normalizePath(c, mustWork = FALSE),
                                   error = function(e) NA_character_))
    if (is.na(d)) next
    for (i in 0:8) {
      if (file.exists(file.path(d, "results_stage_2.csv"))) return(d)
      if (file.exists(file.path(d, "backtest", "results_stage_2.csv"))) return(file.path(d, "backtest"))
      parent <- dirname(d)
      if (identical(parent, d)) break
      d <- parent
    }
  }
  stop("Không tìm thấy results_stage_2.csv. Hãy chạy từ thư mục dự án Alpha_bot ",
       "(setwd('D:/01_Workspace/02_Finance_Trading/Alpha_bot')) rồi chạy lại.")
}
BASE <- find_base()

RESULT_CSV   <- file.path(BASE, "results_stage_2.csv")
DIAG_CSV     <- file.path(BASE, "factor_diagnostics.csv")
ECON_CSV     <- file.path(BASE, "economic_validation.csv")
OUT_DIR      <- file.path(BASE, "out_analysis")
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

`%||%` <- function(a, b) if (is.null(a) || is.na(a)) b else a

## Ngưỡng PASS theo universe (nguồn: tools/common.py)
THRESH <- list(
  "VN-SMALL-CAP" = c(sharpe = 1.0, cagr = 0.25, max_drawdown = -0.45, profit_factor = 1.3, calmar = 0.8),
  "VN-MID-CAP"   = c(sharpe = 1.0, cagr = 0.18, max_drawdown = -0.40, profit_factor = 1.1, calmar = 0.8),
  "VN-LARGE-CAP" = c(sharpe = 1.2, cagr = 0.15, max_drawdown = -0.35, profit_factor = 1.2, calmar = 1.1)
)

## =====================================================================
## 1. Load + chuẩn hoá
## =====================================================================

load_csv <- function(path) {
  if (!file.exists(path)) {
    warning("Không tìm thấy file: ", path)
    return(NULL)
  }
  read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
}

res   <- load_csv(RESULT_CSV)
diag  <- load_csv(DIAG_CSV)
econ  <- load_csv(ECON_CSV)

if (is.null(res)) stop("Thiếu results_stage_2.csv")

## chuyển cột numeric an toàn (giữ NA thay vì lỗi)
num <- function(x) suppressWarnings(as.numeric(x))

res$timestamp      <- res$timestamp
res$cagr           <- num(res$cagr)
res$sharpe         <- num(res$sharpe)
res$max_drawdown   <- num(res$max_drawdown)
res$profit_factor  <- num(res$profit_factor)
res$calmar         <- num(res$calmar)
for (p in c("train_", "test_")) {
  res[[paste0(p, "cagr")]]          <- num(res[[paste0(p, "cagr")]])
  res[[paste0(p, "sharpe")]]        <- num(res[[paste0(p, "sharpe")]])
  res[[paste0(p, "max_drawdown")]]  <- num(res[[paste0(p, "max_drawdown")]])
  res[[paste0(p, "profit_factor")]] <- num(res[[paste0(p, "profit_factor")]])
  res[[paste0(p, "calmar")]]        <- num(res[[paste0(p, "calmar")]])
}

## dedup: giữ row mới nhất (theo timestamp) cho mỗi filepath
res <- res[order(res$timestamp), ]
res_latest <- res[!duplicated(res$filepath, fromLast = TRUE), ]

## chỉ xét các row có kết quả thực (SIMULATED) để phân tích metrics
sim <- res_latest[res_latest$status == "SIMULATED", ]

cat("==============================================================\n")
cat("STAGE 2 — ALPHA STATISTICS\n")
cat("==============================================================\n")
cat(sprintf("Tổng rows (results CSV)  : %d\n", nrow(res)))
cat(sprintf("Rows duy nhất theo file  : %d\n", nrow(res_latest)))
cat(sprintf("SIMULATED (có metrics)   : %d\n", nrow(sim)))
cat(sprintf("VERIFY_FAILED            : %d\n", sum(res_latest$status == "VERIFY_FAILED")))
cat(sprintf("METRICS_TIMEOUT          : %d\n", sum(res_latest$status == "METRICS_TIMEOUT")))
cat(sprintf("By universe              : ")); print(table(sim$universe))

## =====================================================================
## 2. Stage pass + is_pass theo chuẩn tools/common.py
## =====================================================================

stage_pass <- function(row, prefix = "") {
  thr <- THRESH[[row$universe]]
  if (is.null(thr)) return(FALSE)
  keys <- c("sharpe", "cagr", "max_drawdown", "profit_factor", "calmar")
  vals <- vapply(keys, function(k) {
    v <- row[[paste0(prefix, k)]]
    !is.na(v)
  }, logical(1))
  if (!all(vals)) return(FALSE)
  all(vapply(keys, function(k) {
    v <- row[[paste0(prefix, k)]]
    if (k == "max_drawdown") v >= thr[k] else v >= thr[k]
  }, logical(1)))
}

sim$pass_agg   <- vapply(seq_len(nrow(sim)), function(i) stage_pass(sim[i, ], ""), logical(1))
sim$pass_train <- vapply(seq_len(nrow(sim)), function(i) stage_pass(sim[i, ], "train_"), logical(1))
sim$pass_test  <- vapply(seq_len(nrow(sim)), function(i) stage_pass(sim[i, ], "test_"), logical(1))
sim$is_pass    <- sim$pass_agg & sim$pass_train & sim$pass_test

cat("\n---- PASS theo stage (SIMULATED only) ----\n")
pass_tbl <- data.frame(
  universe = c("VN-SMALL-CAP", "VN-MID-CAP", "VN-LARGE-CAP"),
  n        = NA_integer_, pass_agg = NA_integer_, pass_train = NA_integer_,
  pass_test = NA_integer_, is_pass = NA_integer_
)
for (u in pass_tbl$universe) {
  sub <- sim[sim$universe == u, ]
  if (nrow(sub) == 0) next
  pass_tbl[pass_tbl$universe == u, "n"]         <- nrow(sub)
  pass_tbl[pass_tbl$universe == u, "pass_agg"]  <- sum(sub$pass_agg)
  pass_tbl[pass_tbl$universe == u, "pass_train"]<- sum(sub$pass_train)
  pass_tbl[pass_tbl$universe == u, "pass_test"] <- sum(sub$pass_test)
  pass_tbl[pass_tbl$universe == u, "is_pass"]   <- sum(sub$is_pass)
}
print(pass_tbl)

## survival (multiple-testing): PassTrain mà cũng PassTest
cat("\n---- Survival (Train pass -> Test pass) ----\n")
for (u in c("VN-SMALL-CAP", "VN-MID-CAP", "VN-LARGE-CAP")) {
  sub <- sim[sim$universe == u, ]
  if (nrow(sub) == 0) next
  pt <- sum(sub$pass_train)
  both <- sum(sub$pass_train & sub$pass_test)
  cat(sprintf("  %-14s TrainPass=%3d  Train&Test=%3d  survival=%.3f\n",
              u, pt, both, if (pt > 0) both / pt else NA))
}

## =====================================================================
## 3. Top alpha theo test Sharpe (OOS) + train/test tương phản
## =====================================================================

sim$test_gap <- sim$test_sharpe - sim$train_sharpe
top <- sim[order(sim$test_sharpe, decreasing = TRUE), ]
top <- top[!is.na(top$test_sharpe), ]

cat("\n---- TOP 15 alpha theo Test Sharpe (OOS 2023-24) ----\n")
print(head(top[, c("filename", "universe", "cagr", "sharpe",
                   "train_sharpe", "test_sharpe", "train_cagr", "test_cagr",
                   "profit_factor", "test_profit_factor", "is_pass")], 15), row.names = FALSE)

cat("\n---- WORST 10 theo Test Sharpe ----\n")
print(tail(top[, c("filename", "universe", "train_sharpe", "test_sharpe", "is_pass")], 10), row.names = FALSE)

## =====================================================================
## 4. Phân bố metrics theo universe
## =====================================================================

cat("\n---- Summary metrics theo universe (SIMULATED) ----\n")
for (u in c("VN-SMALL-CAP", "VN-MID-CAP", "VN-LARGE-CAP")) {
  sub <- sim[sim$universe == u & !is.na(sim$sharpe), ]
  if (nrow(sub) == 0) next
  cat(sprintf("\n[%s] n=%d\n", u, nrow(sub)))
  s <- function(x) round(quantile(x, c(0, 0.25, 0.5, 0.75, 1), na.rm = TRUE), 3)
  cat("  Sharpe agg     : "); print(s(sub$sharpe))
  cat("  CAGR agg       : "); print(s(sub$cagr))
  cat("  PF agg         : "); print(s(sub$profit_factor))
  cat("  Test Sharpe    : "); print(s(sub$test_sharpe))
  cat("  Test CAGR      : "); print(s(sub$test_cagr))
}

## =====================================================================
## 5. Zero files (CAGR == 0 — universe rỗng / data thiếu)
## =====================================================================

zero <- sim[!is.na(sim$cagr) & sim$cagr == 0, ]
cat("\n---- Files có CAGR == 0 (n =", nrow(zero), ") ----\n")
if (nrow(zero) > 0) print(data.frame(file = zero$filename, universe = zero$universe))

## =====================================================================
## 6. Layer 3 / Layer 4 flags (nếu có file diagnostics)
## =====================================================================

if (!is.null(diag)) {
  cat("\n---- Layer 3 Factor Diagnostics ----\n")
  cat(sprintf("  Alphas phân tích : %d\n", nrow(diag)))
  if ("all_fields_valid" %in% names(diag)) {
    cat(sprintf("  Field invalid    : %d\n", sum(diag$all_fields_valid == "no")))
  }
  for (col in c("has_universe_gate", "has_financial_gate", "has_liquidity_gate",
                "has_pos_denominator", "has_positions_api")) {
    if (col %in% names(diag)) {
      v <- diag[[col]]
      cat(sprintf("  %-22s: %d/%d\n", col, sum(as.numeric(v) == 1), length(v)))
    }
  }
  ## gắn diag vào sim theo filename
  if ("filename" %in% names(diag)) {
    dmap <- diag[, c("filename", "n_fields", "n_quarterly", "n_annual",
                     "has_universe_gate", "has_financial_gate")]
    sim2 <- merge(sim, dmap, by = "filename", all.x = TRUE)
    cat("\n  CAGR==0 theo dấu hiệu gate (điều tra data availability):\n")
    z2 <- sim2[!is.na(sim2$cagr) & sim2$cagr == 0 & !is.na(sim2$n_fields), ]
    if (nrow(z2) > 0) print(z2[, c("filename", "n_fields", "n_quarterly", "n_annual",
                                   "has_universe_gate", "has_financial_gate")], row.names = FALSE)
  }
}

if (!is.null(econ)) {
  cat("\n---- Layer 4 Economic Validation ----\n")
  cat(sprintf("  Alphas phân tích : %d\n", nrow(econ)))
  for (col in c("mixed_annual_quarterly", "ni_vs_cfo", "inventory_vs_revenue",
                "receivables_vs_revenue", "debt_vs_interest", "capex_vs_ppe", "dividend_vs_cfo")) {
    if (col %in% names(econ)) {
      v <- econ[[col]]
      cat(sprintf("  %-26s: %d/%d\n", col, sum(as.numeric(v)), length(v)))
    }
  }
}

## =====================================================================
## 7. Xuất CSV tổng hợp
## =====================================================================

write.csv(sim[, c("filename", "universe", "status", "cagr", "sharpe", "profit_factor",
                  "max_drawdown", "calmar", "train_sharpe", "train_cagr",
                  "test_sharpe", "test_cagr", "test_profit_factor",
                  "pass_agg", "pass_train", "pass_test", "is_pass", "test_gap")],
          file.path(OUT_DIR, "alpha_stats.csv"), row.names = FALSE)
write.csv(pass_tbl, file.path(OUT_DIR, "pass_summary.csv"), row.names = FALSE)

cat("\n==============================================================\n")
cat(sprintf("Đã ghi kết quả vào thư mục: %s\n", OUT_DIR))
cat("==============================================================\n")

## =====================================================================
## 8. Biểu đồ kết hợp (1 ảnh duy nhất) — dùng base R, không cần package
## =====================================================================

make_combined_plot <- function(sim, OUT_DIR) {
  png(file.path(OUT_DIR, "stage_2_combined_plot.png"),
      width = 2000, height = 2600, res = 150)
  par(mfrow = c(3, 2), mar = c(4.2, 4.2, 3, 1), oma = c(0.5, 0.5, 2.5, 0.5))

  uni_col <- c("VN-SMALL-CAP" = "#2e86ab", "VN-MID-CAP" = "#f39c12", "VN-LARGE-CAP" = "#d95f5f")

  ## (1) Train vs Test Sharpe scatter
  plot(sim$train_sharpe, sim$test_sharpe,
       col = uni_col[sim$universe], pch = 16, cex = 1.1,
       xlab = "Train Sharpe (2020-22)", ylab = "Test Sharpe (2023-24)",
       main = "Train vs Test Sharpe")
  abline(0, 1, lty = 2, col = "gray50")
  abline(h = 0, lty = 3, col = "gray70")
  legend("topright", legend = names(uni_col), col = uni_col, pch = 16, bty = "n", cex = 0.8)

  ## (2) Sharpe agg boxplot theo universe
  boxplot(sharpe ~ universe, data = sim,
          col = uni_col[sort(unique(sim$universe))],
          ylab = "Aggregate Sharpe", main = "Aggregate Sharpe by Universe")
  abline(h = 1.0, lty = 2, col = "gray50")
  text(par("usr")[2] * 0.97, 1.05, "SMALL bar 1.0", pos = 2, cex = 0.7, col = "gray40")

  ## (3) Test Sharpe boxplot theo universe
  boxplot(test_sharpe ~ universe, data = sim,
          col = uni_col[sort(unique(sim$universe))],
          ylab = "Test Sharpe", main = "OOS Test Sharpe (2023-24)")
  abline(h = 0, lty = 3, col = "gray70")

  ## (4) CAGR agg boxplot theo universe
  boxplot(cagr ~ universe, data = sim,
          col = uni_col[sort(unique(sim$universe))],
          ylab = "Aggregate CAGR", main = "Aggregate CAGR by Universe")

  ## (5) Test CAGR theo universe
  boxplot(test_cagr ~ universe, data = sim,
          col = uni_col[sort(unique(sim$universe))],
          ylab = "Test CAGR", main = "OOS Test CAGR (2023-24)")
  abline(h = 0, lty = 3, col = "gray70")

  ## (6) Top 15 test Sharpe + label
  o <- order(sim$test_sharpe, decreasing = TRUE)
  topn <- sim[o[seq_len(min(15, nrow(sim)))], ]
  topn <- topn[!is.na(topn$test_sharpe), ]
  if (nrow(topn) > 0) {
    barplot(rev(topn$test_sharpe), horiz = TRUE, las = 1, cex.names = 0.55,
            names.arg = rev(gsub("^Vn(Small|Mid|Large)Cs|^Vn", "", topn$filename)),
            col = uni_col[rev(topn$universe)],
            xlab = "Test Sharpe", main = "Top 15 by OOS Test Sharpe")
  }

  mtext("Alpha_bot — Stage 2 Diagnostics (Aggregate / Train 20-22 / Test 23-24)",
        outer = TRUE, cex = 1.2, font = 2)
  dev.off()

  ## (7) phụ: train-test gap density theo universe (dùng poly: density)
  png(file.path(OUT_DIR, "train_test_gap.png"), width = 1400, height = 900, res = 150)
  gap_u <- split(sim$test_gap, sim$universe)
  cols <- uni_col[names(gap_u)]
  rx <- range(unlist(gap_u), na.rm = TRUE)
  plot(0, 0, type = "n", xlim = rx, ylim = c(0, 1),
       xlab = "Test Sharpe - Train Sharpe", ylab = "Density",
       main = "Train-Test Sharpe gap (âm = overfit)")
  for (u in names(gap_u)) {
    x <- gap_u[[u]]
    x <- x[!is.na(x)]
    if (length(x) < 2) next
    d <- density(x, na.rm = TRUE)
    lines(d, col = uni_col[u], lwd = 2)
    polygon(d, col = adjustcolor(uni_col[u], alpha.f = 0.15))
  }
  abline(v = 0, lty = 2, col = "gray50")
  legend("topright", legend = names(gap_u), col = uni_col[names(gap_u)], lwd = 2, bty = "n")
  dev.off()

  cat(sprintf("Đã tạo biểu đồ: %s\n", file.path(OUT_DIR, "stage_2_combined_plot.png")))
  cat(sprintf("               %s\n", file.path(OUT_DIR, "train_test_gap.png")))
}

if (nrow(sim) > 0) make_combined_plot(sim, OUT_DIR)
