# Framework Kiểm Thử Chiến Lược Phái Sinh Việt Nam
**Phiên bản:** 1.0  
**Lĩnh vực:** Phái sinh (Futures/Options) - Thị trường Việt Nam  
**Khung thời gian:** 1M, 5M, 1H, 4H, 1D  
**Loại kiểm thử:** Quantitative Risk & Validation  

---

## 1. Tổng quan về Triết lý Kiểm thử (Testing Philosophy)

Triết lý kiểm thử này xây dựng trên ba trụ cột cốt lõi:

> **Cốt lõi:** Mọi chiến lược phải được xác thực thông qua lenses định lượng, không thể dựa vào trực giác hay kỳ vọng. Rủi ro luôn là ưu tiên hàng đầu, không lợi nhuận.

### Nguyên tắc 1: Risk-First Validation
- ✓ Kiểm tra **drawdown tối đa** trước khi xem xét lợi nhuận
- ✓ Định lượng **tối đa tổn thất liên tiếp** (Max Consecutive Losses)
- ✓ Đảm bảo **tỷ Risk-to-Reward ≥ 1:1.5** ở mỗi giao dịch
- ✓ Giới hạn **risk per trade ≤ 2% tài khoản**

### Nguyên tắc 2: Robust Cross-Timeframe Validation
- ✓ Xác thực logic trên **tất cả khung thời gian chính**: 1M, 5M, 1H, 4H, 1D
- ✓ Kiểm tra **nhất quán kết quả** giữa các khung (nếu logic cải thiện trên 1H, có cải thiện trên 4H không?)
- ✓ Phát hiện **timeframe-specific overfitting** (nếu kết quả quá tốt trên 1M, cảnh báo overfitting)

### Nguyên tắc 3: Degradation Testing & Edge Cases
- ✓ Kiểm tra hiệu suất trên **thị trường trending vs ranging**
- ✓ Kiểm tra **volatility spikes** (gap, flash crash events)
- ✓ Kiểm tra **liquidity stress** (high spread, low volume events)
- ✓ Tìm **fail scenarios**: khi nào chiến lược hoạt động xấu nhất?

### Nguyên tắc 4: Replicability & Transparency
- ✓ Mọi tham số phải có **logic xác định** (không tuning tùy ý)
- ✓ Mọi giả thuyết phải có **null hypothesis** (cái gì nếu không có logic này?)
- ✓ Mọi kết quả phải **tái lập được** với dữ liệu mới

---

## 2. Bộ quy tắc Logic bắt buộc (Hard Rules)

### A. Xử lý Nhiễu Dữ liệu & Dữ liệu Không hợp lệ

#### Rule HM-1: Loại trừ dữ liệu dị thường (Anomaly Filtering)
```
NẾU: Giá di chuyển >10% trong 1 nến
THÌ: Đánh dấu nến này là "anomaly"
     - Không sử dụng nến này để tính toán indicator
     - Không phát tín hiệu giao dịch từ nến này
     - Log sự kiện để kiểm tra sau (gap opening, halting, etc.)
```

**Tiêu chí cụ thể:**
- Gap > 5%: Check halting/suspension events
- Volume spike > 5x trung bình: Possible data error, verify
- Price move > 10% without volume: Likely data error, reject

#### Rule HM-2: Loại trừ dữ liệu không đủ thanh khoản (Liquidity Validation)
```
NẾU: Spread trung bình > 0.5% (phí sinh)
THÌ: Không giao dịch trên khung này
     - Drawdown lý thuyết vs thực tế có sai lệch quá lớn
     - Slippage không kiểm soát được
```

**Tiêu chí cụ thể:**
- Spread < 0.2%: ✓ Đủ thanh khoản
- Spread 0.2% - 0.5%: ⚠ Cấnh báo, cần kiểm tra thêm
- Spread > 0.5%: ✗ Từ chối, không đủ thanh khoản

#### Rule HM-3: Xác thực tính liên tục dữ liệu (Continuity Check)
```
NẼU: Có gap thời gian > 1.5x khung thời gian (ví dụ: khung 1M gap 1.5 phút)
THÌ: - Đánh dấu giai đoạn này là "illiquid period"
     - Tắt tất cả tín hiệu giao dịch
     - Không tính drawdown từ dữ liệu gap
```

---

### B. Quản lý Rủi ro & Kiểm soát Vị thế (Position Management)

#### Rule RK-1: Giới hạn Rủi ro trên mỗi giao dịch (Per-Trade Risk Cap)
```
Risk per Trade = (Entry Price - Stop Loss) × Position Size
               ≤ 2% of Total Account

NẾU: Risk > 2%
THÌ: - Giảm Position Size
     - Hoặc tăng SL (xấu hơn, không khuyên dùng)
     - NÓI KHÔNG với giao dịch nếu SL hợp lý không đạt được
```

**Công thức tính:**
- Max Loss per Trade = Account Balance × 2%
- Position Size = Max Loss / (Entry - Stop Loss)

#### Rule RK-2: Giới hạn Drawdown tối đa (Max Drawdown Control)
```
NẾU: Tích lũy Drawdown vượt quá 15% tài khoản
THÌ: - DỪNG GIAO DỊCH ngay lập tức
     - Chờ signal xác nhận chiến lược lại hoạt động tốt
     - Thực hiện post-mortem analysis

NẾU: Tích lũy Drawdown vượt quá 20% tài khoản
THÌ: - Khởi động quy trình "Strategy Pause & Review"
     - Yêu cầu kiểm tra lại toàn bộ framework
     - Không giao dịch cho đến khi xác định được gốc rễ
```

**Điểm dừng chiến lược:**
| Drawdown | Hành động |
|----------|-----------|
| 0-10% | ✓ Bình thường, tiếp tục |
| 10-15% | ⚠ Cảnh báo, giảm position, tăng kiểm soát |
| 15-20% | ⛔ Dừng, review, xác thực |
| > 20% | 🚨 Crisis mode, kiểm tra toàn bộ logic |

#### Rule RK-3: Chặn Drawdown chuỗi (Consecutive Loss Limit)
```
NẾU: Số lần thua liên tiếp ≥ 5 lần
THÌ: - Tạm dừng chiến lược
     - Chờ tối thiểu 3 giao dịch thắng liên tiếp
     - Hoặc chờ tín hiệu xác nhận mạnh (ví dụ: break-out xác thực)
```

**Ngôn ngữ giao dịch:**
- Win Rate phải ≥ 40% (tối thiểu)
- Profit Factor phải ≥ 1.2 (tổng lợi nhuận / tổng tổn thất)
- Nếu không đạt → Chiến lược không valid, cần redesign

#### Rule RK-4: Giới hạn Vị thế mở (Concurrent Position Limit)
```
Số vị thế mở cùng lúc ≤ 3
- Tối ưu để quản lý rủi ro tổng hệ thống
- Tránh correlation risk (nếu 3 vị thế cùng mở đều bị liquidate)
- Tính tối đa tổn thất: 3 × 2% = 6% tối đa

NẾU: Vị thế 4 được signal
THÌ: - Chờ vị thế cũ đóng
     - Hoặc đóng vị thế yếu nhất để chuyên chứ
```

---

### C. Quản lý Tín hiệu & Điều kiện Giao dịch (Signal Validation)

#### Rule TH-1: Đa xác thực Tín hiệu (Multi-Confirmation Rule)
```
Một tín hiệu chỉ được phép "active" khi:
1. ✓ Indicator chính (ví dụ: Moving Average crossover) xác nhận
2. ✓ Indicator phụ (ví dụ: RSI, MACD) xác nhận
3. ✓ Volume hoặc Volatility xác nhận (không phải giả)

NẾU: Chỉ 1 hoặc 2 điều kiện đạt
THÌ: - Tín hiệu yếu, xác suất cao sai lệch
     - Giảm Position Size 50% hoặc Skip trade
```

**Mô hình xác thực:**
- Trend confirmation: Giá > MA20 > MA50 (Khung 1H+)
- Momentum confirmation: RSI 30-70 (không quá sold/overbought)
- Volume confirmation: Volume hôm nay ≥ 80% trung bình 20 nến

#### Rule TH-2: Loại trừ Giao dịch trong Vùng Không xác định (No-Trade Zones)
```
Vùng KHÔNG giao dịch:
1. Giờ mở cửa ±30 phút (7:00-7:30 AM Việt Nam): Spread rộng, dữ liệu không ổn định
2. News release 2 giờ trước/sau (kiểm tra lịch kinh tế)
3. Volatility jump > 2x STD (khung 20 nến): Quá nguy hiểm
4. Khi SMA20 và SMA50 nằm quá gần nhau (< 0.1%): Trending không rõ
```

#### Rule TH-3: Confirm Trend trước khi giao dịch (Trend Validation)
```
NẾU: Khung 1H trending UP
THÌ: - Khung 5M chỉ giao dịch BUY (không SHORT)
     - SHORT chỉ được phép nếu khung 1H flip DOWN

NẾU: Khung 4H ranging (PA nằm trong box)
THÌ: - Tắt tất cả trend-following logic
     - Chuyển sang range-trading (buy support, sell resistance)
```

---

### D. Kiểm soát Giá trị tham số (Parameter Guardrails)

#### Rule TM-1: Giới hạn tham số chính
```
Moving Averages:
- Fast MA: 5 ≤ period ≤ 20
- Slow MA: 40 ≤ period ≤ 100
- Nếu ngoài khoảng này → cảnh báo overfitting

RSI:
- Period: 10 ≤ RSI_period ≤ 21
- Overbought threshold: 65-80 (không cứng 70)
- Oversold threshold: 20-35 (không cứng 30)

ATR (ATR-based Stop Loss):
- Period: 10 ≤ ATR_period ≤ 21
- Multiplier: 1.5 ≤ multiplier ≤ 2.5
- Stop Loss = Entry ± (ATR × multiplier)
```

#### Rule TM-2: Walk-forward validation
```
NẾU: Tham số được tune trên dữ liệu cũ
THÌ: - Phải re-test trên dữ liệu mới (out-of-sample)
     - Nếu hiệu suất giảm > 20% → cảnh báo overfitting
     - Nếu giảm > 50% → từ chối tham số này
```

---

## 3. Các giả thuyết mẫu (Sample Hypotheses)

Mỗi giả thuyết tuân theo cấu trúc:
```
ID: HYP-[Khung]-[Số hiệu]
Tên: [Mô tả ngắn]
Null Hypothesis: [Nếu logic này bị loại bỏ, có gì xảy ra?]
Alternative Hypothesis: [Logic này sẽ cải thiện chỉ số X bao nhiêu %?]
Metric: [Chỉ số đo lường]
Threshold: [Mức tối thiểu để chấp nhận giả thuyết]
Data Range: [Khoảng dữ liệu kiểm thử]
Status: [TODO / In Progress / VALIDATED / REJECTED]
```

---

### Khung 1 Phút (1M) - Ultra-Short-Term Scalping

#### HYP-1M-001: EMA Crossover + RSI Confirmation
**Tên:** Giao dịch breakout EMA5/EMA12 với xác thực RSI  
**Null Hypothesis:** Không có logic EMA crossover, chỉ giao dịch ngẫu nhiên  
**Alternative Hypothesis:** EMA crossover + RSI sẽ tăng win rate ≥ 48% (từ baseline ~50% random)  

**Logic chi tiết:**
```
BUY Signal:
  ✓ EMA5 > EMA12 (crossover xảy ra trong 3 nến gần nhất)
  ✓ RSI(14) 40-60 (not overbought/oversold)
  ✓ Volume hôm nay ≥ 70% trung bình 20 nến
  → Entry at market, SL = EMA12 - 0.5 × ATR(10)

SELL Signal:
  ✓ EMA5 < EMA12 (crossover DOWN)
  ✓ Hoặc RSI > 75 (lấy lợi nhuận)
  → Close at market
```

**Metric đo lường:**
- Win Rate ≥ 48%
- Profit Factor ≥ 1.1
- Avg Win / Avg Loss ≥ 1.2
- Max Consecutive Losses ≤ 4

**Threshold chấp nhận:** Phải đạt ≥3/4 metric trên  
**Data Range:** Kiểm thử trên 4 tuần dữ liệu 1M gần nhất  
**Status:** TODO

---

#### HYP-1M-002: Support/Resistance Bounce (Micro-reversal)
**Tên:** Giao dịch bounce từ S/R cục bộ với ATR tối ưu  
**Null Hypothesis:** Bounce từ S/R không có lợi nhuận vượt trội (alpha = 0)  
**Alternative Hypothesis:** Bounce từ S/R sẽ đạt RRR ≥ 1:2 với success rate ≥ 55%  

**Logic chi tiết:**
```
Xác định S/R cục bộ (khung 1M):
  - Resistance: Cao điểm trong 20 nến gần nhất
  - Support: Thấp điểm trong 20 nến gần nhất

BUY từ Support:
  ✓ Giá chạm Support ±1 tick
  ✓ Không breachthrough (close > support)
  ✓ Candle close là bullish (close > open)
  → Entry 1 tick trên support
  → SL = Support - 2 × ATR(10)
  → TP = Support + 2 × (Entry - SL)

SELL từ Resistance:
  ✓ Giá chạm Resistance ±1 tick
  ✓ Không break out
  ✓ Candle close là bearish
  → Entry 1 tick dưới resistance
  → TP = Resistance - 2 × (Resistance - Entry)
```

**Metric đo lường:**
- Success Rate ≥ 55%
- RRR trung bình ≥ 1:1.8
- Độ tin cậy S/R ≥ 3 lần chạm (không S/R yếu)
- Max Drawdown ≤ 10%

**Threshold chấp nhận:** ≥3/4 metric  
**Data Range:** 4 tuần, giờ cao điểm (9-11 AM & 2-3 PM Việt Nam)  
**Status:** TODO

---

### Khung 5 Phút (5M) - Short-Term Momentum

#### HYP-5M-001: MACD Histogram Divergence + Trend Filter
**Tên:** Giao dịch MACD histogram reversal khi có trend xác nhận từ 1H  
**Null Hypothesis:** MACD histogram không có giá trị dự đoán riêng lẻ  
**Alternative Hypothesis:** MACD + trend filter sẽ tăng Sharpe ratio ≥ 0.8 (từ 0.3 baseline)  

**Logic chi tiết:**
```
Bước 1: Confirm Trend từ khung 1H
  - NẾU EMA5 > EMA20 (khung 1H) → Trend UP
  - NẾU EMA5 < EMA20 (khung 1H) → Trend DOWN
  - NẾU nằm giữa → Skip trade (no trend)

Bước 2: Giao dịch MACD trên khung 5M
  NẾU Trend UP (khung 1H):
    ✓ MACD histogram từ âm chuyển dương (BULLISH divergence)
    ✓ MACD line > Signal line
    ✓ RSI(5) < 70 (chưa overbought)
    → BUY signal, entry at market
    → SL = Low của nến MACD crossover - ATR(10)
    → TP = Entry + 2 × ATR(10)
  
  NẾU Trend DOWN (khung 1H):
    ✓ MACD histogram từ dương chuyển âm (BEARISH divergence)
    ✓ MACD line < Signal line
    ✓ RSI(5) > 30 (chưa oversold)
    → SHORT signal
```

**Metric đo lường:**
- Sharpe Ratio ≥ 0.8
- Win Rate ≥ 52%
- Độ tin cậy Divergence: MACD histogram ≥ 3 bar (không quá yếu)
- Drawdown Max ≤ 12%

**Threshold chấp nhận:** Sharpe ≥ 0.8 LÀ MUST-HAVE  
**Data Range:** 6 tuần, tất cả giờ giao dịch  
**Status:** TODO

---

#### HYP-5M-002: Bollinger Band Squeeze + Volatility Expansion
**Tên:** Giao dịch breakout sau Bollinger Band squeeze  
**Null Hypothesis:** Squeeze không dự báo volatility expansion  
**Alternative Hypothesis:** Squeeze sẽ dự báo breakout thành công ≥ 58% trường hợp  

**Logic chi tiết:**
```
Xác định Squeeze:
  Bandwidth = (Upper BB - Lower BB) / SMA(20)
  SQUEEZE xảy ra khi Bandwidth < 1.5% (thấp hơn 30 nến)

Giao dịch Breakout sau Squeeze:
  NẾU: Squeeze được xác nhận trong 5 nến
  VÀ:  Nến thứ 6 close > Upper BB (hoặc < Lower BB)
  
  → BUY trên Upper BB breakout
    SL = Middle BB (SMA 20)
    TP = Entry + 2 × (Upper BB - Lower BB)
  
  → SHORT trên Lower BB breakout
    SL = Middle BB
    TP = Entry - 2 × (Upper BB - Lower BB)
```

**Metric đo lường:**
- Breakout Success Rate ≥ 58%
- Avg Win / Avg Loss ≥ 1.4
- Max Consecutive Losses ≤ 5
- Win Rate ≥ 45%

**Threshold chấp nhận:** ≥3/4 metric  
**Data Range:** 6 tuần, loại trừ khung 7-8 AM (pre-open noise)  
**Status:** TODO

---

### Khung 1 Giờ (1H) - Intraday Core

#### HYP-1H-001: 20-50 EMA Crossover + Volume Confirmation
**Tên:** Giao dịch trend reversal khi EMA20 crossover EMA50 với volume spike  
**Null Hypothesis:** EMA crossover là giả tín hiệu không có alpha  
**Alternative Hypothesis:** EMA20 > EMA50 crossover sẽ tạo profitable trend ≥ 60% thời gian, avg trend duration ≥ 4 giờ  

**Logic chi tiết:**
```
Xác định Crossover:
  ✓ Nến trước: EMA20 < EMA50
  ✓ Nến hiện tại: EMA20 > EMA50 (BULLISH CROSS)
  ✓ Volume nến hiện tại ≥ 1.3 × Avg Volume (20 nến)

BUY Entry:
  → Entry: High của nến crossover + 1 tick (confirmation)
  → SL: Low của 3 nến gần nhất (support động)
  → TP: Entry + ATR(21) × 2.5 (first target)
  → Trailing stop sau target 1 (protect profit)

SELL Exit:
  ✓ Close < EMA20 (trend flip)
  ✓ Hoặc TP đạt
  ✓ Hoặc SL chạm
```

**Metric đo lường:**
- Trend Success Rate ≥ 60%
- Avg Trend Duration ≥ 4 giờ
- Win Rate ≥ 55%
- Profit Factor ≥ 1.35
- Max Drawdown ≤ 14%

**Threshold chấp nhận:** ≥4/5 metric  
**Data Range:** 8 tuần, loại trừ khung 3-5 AM (low liquidity)  
**Status:** TODO

---

#### HYP-1H-002: RSI Divergence (Hidden Reversal Signal)
**Tên:** Giao dịch reversal khi giá tạo HH nhưng RSI tạo LH (bullish divergence)  
**Null Hypothesis:** Divergence là random pattern, không có mức độ dự báo cao  
**Alternative Hypothesis:** Bullish divergence sẽ reverse downtrend ≥ 62% trường hợp, reversal avg ≥ 3 giờ  

**Logic chi tiết:**
```
Bullish Divergence (Hidden Reversal):
  ✓ Giá tạo Lower High (LH): High hiện tại < High trước 1-3 giờ
  ✓ RSI tạo Higher Low (HL): RSI low hiện tại > RSI low trước 1-3 giờ
  ✓ RSI trong vùng oversold (< 35) lần thứ hai
  ✓ Divergence thời gian ≤ 3 nến (không quá xa)

LONG Entry:
  → Entry: Break trên high nến thứ 2 (nến tạo LH)
  → SL: Low nến tạo LH - ATR(21)
  → TP1: Entry + ATR(21)
  → TP2: Entry + 2.5 × ATR(21)

Confirm Close:
  ✓ Close > Entry + 0.5 × ATR
  ✓ Hoặc 2 giờ hold (tối thiểu)
  ✓ Hoặc TP/SL đạt
```

**Metric đo lường:**
- Reversal Success Rate ≥ 62%
- Win Rate ≥ 58%
- Avg Reversal Duration ≥ 3 giờ
- Profit Factor ≥ 1.4
- False Signal Rate ≤ 30%

**Threshold chấp nhận:** ≥4/5 metric  
**Data Range:** 8 tuần, downtrend periods only  
**Status:** TODO

---

### Khung 4 Giờ (4H) - Swing Core

#### HYP-4H-001: Ichimoku Cloud Breakout + Trend Strength
**Tên:** Giao dịch breakout khỏa cloud Ichimoku với xác thực trend từ 1D  
**Null Hypothesis:** Cloud breakout không dự báo swing trend bền vững  
**Alternative Hypothesis:** Cloud breakout sẽ tạo swing trend ≥ 65% thành công, avg swing ≥ 8-16 giờ  

**Logic chi tiết:**
```
Setup Ichimoku (khung 4H):
  - Conversion Line = (9-period High + 9-period Low) / 2
  - Base Line = (26-period High + 26-period Low) / 2
  - Cloud = Senkou Span (plotted 26 periods ahead)

BULLISH Setup:
  ✓ Giá break > Upper Cloud (Senkou Span A)
  ✓ Conversion Line > Base Line
  ✓ Conversion Line > Cloud (bullish alignment)
  ✓ Chikou Span > Price 26 bars ago (future strength signal)

LONG Entry:
  → Entry: Break trên Upper Cloud
  → SL: Low của nến breakout - ATR(21)
  → TP: Entry + 3 × ATR(21) (first target, giữ 50% position)
  → Trailing TP: Move SL to break-even sau TP1

CONFIRM:
  ✓ Cloud dịch UP (tương lai bullish)
  ✓ Giá stay > Cloud ≥ 2 nến
```

**Metric đo lường:**
- Breakout Success Rate ≥ 65%
- Win Rate ≥ 60%
- Avg Swing Duration ≥ 8 giờ
- Max Profit per Swing ≥ 2.5 × Risk
- Profit Factor ≥ 1.5

**Threshold chấp nhận:** ≥4/5 metric  
**Data Range:** 12 tuần, các swing trend periods  
**Status:** TODO

---

#### HYP-4H-002: Support/Resistance Retest (Higher Probability Entry)
**Tên:** Giao dịch retest S/R cấp swing sau breakout  
**Null Hypothesis:** Retest không cải thiện entry probability  
**Alternative Hypothesis:** Retest entry sẽ tăng success rate to ≥ 68%, giảm max drawdown ≥ 15%  

**Logic chi tiết:**
```
Bước 1: Xác định S/R (khung 4H)
  - Resistance cũ: High khối lượng từ 8-12 tuần trước
  - Support cũ: Low khối lượng từ 8-12 tuần trước

Bước 2: Confirm Breakout
  ✓ Giá break > Resistance + 20 pips
  ✓ Volume ≥ 1.5 × Avg Volume
  ✓ Stay > Resistance ≥ 2 nến (không fake breakout)

Bước 3: Chờ Retest
  ✓ Giá pull back tới Resistance cũ (giờ support mới)
  ✓ Nhưng NOT CLOSE dưới
  ✓ Bounce từ level này

LONG Entry tại Retest:
  → Entry: High nến bounce + 1 tick
  → SL: Low nến bounce - 10 pips (tight control)
  → TP: 2 × Risk (ratio tốt hơn initial breakout)
  → Max Hold: 4 nến nếu không hit TP (move on)

Validate:
  ✓ Entry volume ≥ 1.2 × Avg
  ✓ Bounce close bullish (close > open)
```

**Metric đo lường:**
- Retest Success Rate ≥ 68%
- Win Rate ≥ 65%
- Avg Win/Avg Loss ≥ 1.6
- Max Drawdown ≤ 10% (vs 15% breakout direct)
- Entry Quality Score ≥ 4/5

**Threshold chấp nhận:** ≥4/5 metric  
**Data Range:** 12 tuần, confirmed breakout only  
**Status:** TODO

---

### Khung 1 Ngày (1D) - Position/Swing Long-term

#### HYP-1D-001: Weekly Trend Structure + Monthly Support
**Tên:** Giao dịch position trend khi confirm từ weekly + monthly support hold  
**Null Hypothesis:** Monthly support không có significant impact, trend = random walk  
**Alternative Hypothesis:** Position held at monthly support sẽ thành công ≥ 70%, avg position ≥ 10 ngày  

**Logic chi tiết:**
```
Setup (Multi-timeframe):
  Khung DAILY:
    ✓ EMA20 > EMA50 (uptrend)
    ✓ RSI > 50 (bullish momentum)
    ✓ Price > SMA200 (long-term uptrend)
  
  Khung WEEKLY:
    ✓ EMA20(W) > EMA50(W) (weekly uptrend)
    ✓ Cloud (W) bullish (để retest cloud dưới là support)
  
  Khung MONTHLY:
    ✓ Key support từ Low tháng trước hoặc trước đó
    ✓ Giá không break dưới support này

LONG Entry:
  → Điều kiện: Giá retest Monthly support
  → Entry: High nến retest + close bullish
  → SL: Low của 2 nến retest - 50 pips (safety)
  → TP: Monthly Resistance hoặc High tháng trước
  → Hold: ≥ 10 ngày

Monitor:
  ✓ Keep SL at level, don't move (avoid whipsaw)
  ✓ Partial take profit at 50% level
  ✓ Trail profit after 5 ngày hold
```

**Metric đo lường:**
- Position Success Rate ≥ 70%
- Win Rate ≥ 68%
- Avg Position Duration ≥ 10 ngày
- Profit Factor ≥ 1.6
- Max Consecutive Losses ≤ 3 (long-term so fewer trades)

**Threshold chấp nhận:** ≥4/5 metric  
**Data Range:** 6 tháng (24 tuần dữ liệu)  
**Status:** TODO

---

#### HYP-1D-002: Higher High-Higher Low + Breakout New ATH
**Tên:** Giao dịch breakout ATH (All-Time High) sau series HH-HL  
**Null Hypothesis:** HH-HL pattern không có alpha, breakout ATH là random noise  
**Alternative Hypothesis:** HH-HL + ATH breakout sẽ tạo strong trend ≥ 72%, avg ≥ 15 ngày, breakout hold ≥ 90%  

**Logic chi tiết:**
```
Pattern Recognition (khung 1D):
  ✓ Minimum 3 lần Higher High (HH):
    High(n) > High(n-1) > High(n-2)
  ✓ Minimum 3 lần Higher Low (HL):
    Low(n) > Low(n-1) > Low(n-2)
  ✓ Pattern duration: 20-40 ngày (tối ưu)
  ✓ Trend angle: 45-70° (không quá mạnh, không quá yếu)

ATH Breakout Entry:
  → Trigger: Close > All-Time High
  → Entry: ATH + 1 pip (confirmation close)
  → SL: Low nến breakout - 100 pips
  → TP: ATH + (ATH - Lowest Low in pattern) × 1.5
  → Hold: ≥ 15 ngày

Confirmation Rules:
  ✓ Close > ATH (không fake wick)
  ✓ Volume ≥ 1.5 × 50-day average
  ✓ Next 2-3 nến tiếp tục > ATH (sustained)
```

**Metric đo lường:**
- ATH Breakout Success Rate ≥ 72%
- Win Rate ≥ 70%
- Breakout Breakout Hold Rate ≥ 90% (không bị reversed)
- Avg Position Duration ≥ 15 ngày
- Profit Factor ≥ 1.7
- Avg Win ≥ 3 × Avg Loss

**Threshold chấp nhận:** ≥5/6 metric (rất strictly)  
**Data Range:** 12 tháng (confirmed ATH patterns only)  
**Status:** TODO

---

## 4. Chỉ dẫn cho Alpha Bot (AI Cross-Verification Protocol)

### ⚙️ Hướng dẫn sử dụng Framework này

Khi AI/Bot đọc file này, vui lòng tuân thủ quy trình sau để **cross-verify** một chiến lược mới hoặc một giả thuyết mới:

#### **Bước 1: Xác thực Compliance với Hard Rules** ⛔
Trước khi tiếp tục bất kỳ phân tích nào:
```
□ Kiểm tra: Chiến lược có xử lý Anomalies không? (Rule HM-1)
□ Kiểm tra: Chiến lược có check Liquidity không? (Rule HM-2)
□ Kiểm tra: Chiến lược có validate dữ liệu Continuity không? (Rule HM-3)
□ Kiểm tra: Có Risk Cap ≤ 2% per trade không? (Rule RK-1)
□ Kiểm tra: Có Max Drawdown limit (15-20%) không? (Rule RK-2)
□ Kiểm tra: Có Consecutive Loss limit không? (Rule RK-3)
□ Kiểm tra: Có Position limit ≤ 3 không? (Rule RK-4)

⚠️ NẾU bất kỳ item nào là FALSE → REJECT chiến lược ngay lập tức
✓ NẾU tất cả TRUE → Tiếp tục Bước 2
```

#### **Bước 2: Ánh xạ vào Template Hypothesis** 📋
```
Câu hỏi: Giả thuyết này thuộc khung thời gian nào (1M, 5M, 1H, 4H, 1D)?
→ Tìm HYP-[Khung]-[Số] phù hợp nhất

Câu hỏi: Chiến lược này có overlap logic nào với hypothesis existing không?
→ Nếu có → Kiểm tra Metric của hypothesis existing
→ Nếu không → Tạo hypothesis mới sử dụng template

Câu hỏi: Mục tiêu metric là gì?
→ Điền vào Alternative Hypothesis
→ Cập nhật Threshold
```

#### **Bước 3: Multi-Timeframe Cross-Check** 🔄
```
□ Nếu logic là 5M → Check consistency trên 1M và 1H
  - Nếu kết quả tốt trên 5M nhưng tệ trên 1M → Cảnh báo Overfitting
  - Nếu kết quả đều tốt → ✓ Robust signal

□ Nếu logic là 1H → Check consistency trên 5M, 4H, 1D
  - Trend từ 4H có match với 1H không?
  - Volume confirmation từ 1D có giúp không?

□ Nếu logic là 1D → Check consistency trên 1H, 4H
  - Support/Resistance từ 1H có phá vỡ 1D structure không?
```

#### **Bước 4: Multi-Stage Validation & Backtest Scenario Planning** 🧪

##### Multi-Stage Validation
```
Quy trình kiểm thử 2 giai đoạn bắt buộc:

Stage 1: Train (Huấn luyện - In-Sample) — 70% dữ liệu
  □ Cho phép tối ưu hóa tham số
  □ Không được Overfitting (nếu quá tốt so với Test → cảnh báo)
  □ Target: đạt tất cả các chỉ số trong Validation Scorecard

Stage 2: Test (Kiểm thử - Out-of-Sample) — 30% dữ liệu gần nhất
  □ Dữ liệu giấu kín (không được dùng để tune)
  □ Kết quả phải ổn định, pass các chỉ số mục tiêu
  □ Nếu không pass → REJECT, không deploy
```

##### Backtest Scenario Planning
```
Chạy backtest với 4 scenario:
1. NORMAL MARKET (trending, vol normal): Expected profit ratio
2. CHOPPY MARKET (ranging, vol normal): Max drawdown, win rate
3. HIGH VOLATILITY (spikes, gaps): Slippage impact, SL test
4. LOW LIQUIDITY (tight bid/ask, gaps): Actual vs theoretical P&L

Cảnh báo: Nếu bất kỳ scenario nào fail → Redesign logic hoặc parameters
```

#### **Bước 5: Validation Scorecard** 📊
```
Chấm điểm theo tiêu chí Acceptance Criteria:

Metric                          | Target  | Actual | Pass?
--------------------------------|---------|--------|-------
Sharpe Ratio                    | ≥ 1.2   | ?      | □
CAGR                            | ≥ 25%   | ?      | □
Max Drawdown                    | ≥ -40%  | ?      | □
Profit Factor                   | ≥ 1.7   | ?      | □
Calmar Ratio (CAGR / Max DD)    | ≥ 0.9   | ?      | □

VERDICT:
  - Train: Đạt ≥ 4/5 → ✓ Sang Stage Test
  - Train: Đạt < 4/5 → ✗ REJECT, tune lại, không qua Test
  - Test: Đạt ≥ 4/5 → ✓ PASS, sẵn sàng deploy
  - Test: Đạt < 4/5 → ✗ REJECT, quay lại Bước 2 & 3
```

#### **Bước 6: Live Validation Protocol** 🚀
```
Trước khi go live với chiến lược mới:

Phase 1 - Paper Trading (2-4 tuần):
  □ Chạy chiến lược trên simulated account
  □ Compare backtest vs paper trading (chênh lệch ≤ 10% → OK)
  □ Record mọi false signal, slippage, execution issues
  □ Nếu pass → Phase 2

Phase 2 - Micro Position (2-4 tuần):
  □ Trade tiny position (1% risk per trade)
  □ Confirm execution, slippage, real-world impact
  □ Kiểm tra drawdown (có vượt 15% không?)
  □ Nếu pass → Phase 3

Phase 3 - Full Position (Ongoing):
  □ Ramp up vị thế từ từ
  □ Monitor hằng ngày với framework này
  □ Weekly review: Metric có drop không? Logic có flip không?
  □ Monthly review: Comprehensive backtesting với dữ liệu mới
```

#### **Bước 7: Continuous Monitoring & Drift Detection** 📈
```
Hằng ngày kiểm tra:
  □ Win rate hôm nay ≥ 40%? (minimum viable)
  □ Drawdown hôm nay ≤ 5%? (intraday check)
  □ Số lần thua liên tiếp < 5?
  
Hằng tuần kiểm tra:
  □ Win rate tuần này ≥ 45%?
  □ Profit factor tuần này ≥ 1.0? (break-even OK, loss NOT OK)
  □ Max drawdown tuần ≤ 10%?
  □ Có hypothesis nào violated không?
  
Hằng tháng kiểm tra:
  □ Backtest lại với 4 tuần dữ liệu mới
  □ So sánh metric với expected threshold
  □ Nếu metric drop > 20% → Investigate root cause
  □ Nếu metric drop > 40% → SUSPEND chiến lược, review framework
  
⚠️ ALERT TRIGGERS:
  - 3 lần thua liên tiếp → Tăng kiểm soát, giảm position 50%
  - 5 lần thua liên tiếp → STOP trading, root cause analysis
  - Drawdown > 15% → Review all hard rules
  - Drawdown > 20% → FREEZE, full framework audit
```

#### **Bước 8: Documentation & Version Control** 📝
```
Sau mỗi test cycle, cập nhật:
  
HYP-[ID] Status: VALIDATED / IN-PROGRESS / REJECTED
  - Metric Achieved: [Ghi lại kết quả thực tế]
  - Date Tested: [Khoảng dữ liệu]
  - Parameters Used: [Nếu có tune]
  - Notes: [Insights, failures, next steps]

VD:
HYP-1H-001 Status: VALIDATED
  - Win Rate: 56% (Target: 55%) ✓
  - Profit Factor: 1.38 (Target: 1.35) ✓
  - Max Drawdown: 13% (Target: 14%) ✓
  - Date Tested: 2024-11-01 to 2024-12-31
  - Notes: Perform well in trending market, struggled in choppy period 12/15-12/20
  - Next: Test on 1D frame, reduce SL tightness
```

---

## 6. Design Guidelines for AI Agent (Achieving Acceptance Criteria)

### Để đạt Sharpe ≥ 1.2 & Profit Factor ≥ 1.7

- Cần **bộ lọc xu hướng mạnh** tránh vào lệnh trong thị trường Sideway (nhiễu)
- Sử dụng `operations/` như `self.op.crossed_above`, `self.op.crossed_below` để phát hiện điểm đảo chiều chính xác
- Kết hợp 2+ tín hiệu độc lập trước khi entry (ví dụ: trend filter + momentum + volume)
- Không trade khi ADX < 20 (thị trường đi ngang, không có xu hướng rõ)

### Để chặn Max Drawdown (tối thiểu ≥ -40%)

- Thiết kế **exit_setup nhanh** khi giá vi phạm xu hướng hoặc cắt xuống các đường hỗ trợ động (Rolling Mean / Rolling Quantile)
- Dùng trailing exit: đóng vị thế khi giá quay ngược qua các đường trung bình động ngắn hạn
- Không giữ vị thế quá lâu nếu không có xác nhận mới từ thị trường

### Multi-Stage Discipline

- Khi code strategy, luôn nghĩ: *"Logic này có overfit Train không? Khi qua Test nó có còn hoạt động không?"*
- Tham số càng đơn giản (ít tuning) càng ít overfit
- Ưu tiên logic có ý nghĩa thị trường hơn là logic quá phức tạp

---

### 🤖 Quy trình Recommendation cho AI/Bot

Khi AI được yêu cầu **"Kiểm tra chiến lược X"** hoặc **"Validate hypothesis Y"**:

1. **Tự động chạy Bước 1-2:** Compliance check & hypothesis mapping
2. **Report về violations:** Nếu có bất kỳ hard rule violated → báo cáo ngay
3. **Suggest metrics cần test:** Dựa trên hypothesis template
4. **Simulate backtest scenario:** Nếu có dữ liệu, chạy quick backtest
5. **Output scorecard:** Cho user dễ nhìn, dễ quyết định
6. **Recommend action:** Trade / Monitor / Suspend / Redesign

---

### 📞 FAQ cho Alpha Bot

**Q: Khi nào tôi có thể phá vỡ Hard Rules?**  
A: KHÔNG BAO GIỜ. Hard Rules là guardrails để bảo vệ tài khoản. Nếu logic không phù hợp với Hard Rules, hãy redesign logic, không phá vỡ rule.

**Q: Tôi nên ưu tiên Win Rate hay Profit Factor?**  
A: **Profit Factor first.** Win Rate 40% với Profit Factor 1.8 tốt hơn Win Rate 60% với Profit Factor 1.1. Vì Profit Factor = Expected Value * (Opportunity Frequency).

**Q: Hypothesis nào là "must-have" để go live?**  
A: Tối thiểu 2-3 hypothesis từ core timeframe của bạn phải VALIDATED. VD: Nếu trade 1H, tối thiểu HYP-1H-001 và HYP-1H-002 pass. Nếu only 1H hypothesis valid, risk quá lớn.

**Q: Max bao nhiêu hypothesis mà tôi nên test cùng lúc?**  
A: 3-4 hypothesis overlap chứa được. Vì mỗi hypothesis thêm = complexity thêm = chance failed thêm. Keep it simple.

**Q: Nếu backtest tốt nhưng paper trade tệ, tôi phải làm gì?**  
A: 80% trường hợp là **slippage + execution delay**. Backtest assume order fill tức thì, thực tế có slippage. Solution: Tăng SL 1-2 pips, giảm TP 1-2 pips, hoặc reduce position size.

---

## 📚 Tham khảo & Phiên bản

| Thuộc tính | Chi tiết |
|-----------|----------|
| **Framework Version** | 1.0 |
| **Ngày tạo** | 2025-01-15 |
| **Thị trường** | Phái sinh Việt Nam (VN30F, GoldF, etc.) |
| **Khung thời gian** | 1M, 5M, 1H, 4H, 1D |
| **Số Hypothesis** | 8 (mẫu) |
| **Số Hard Rules** | 12 categories |
| **Owner** | Quantitative Risk & Validation Analyst |
| **Last Updated** | 2025-01-15 |

---

## 🚀 Lộ trình tiếp theo

- [ ] **Phase 1:** Validate tất cả 8 hypothesis trên backtest (tuần 1-4)
- [ ] **Phase 2:** Chạy paper trading 4 tuần, compare metric (tuần 5-8)
- [ ] **Phase 3:** Deploy với micro position, monitor 2-4 tuần (tuần 9-12)
- [ ] **Phase 4:** Ramp up, maintain, continuous monitoring (ongoing)
- [ ] **Phase 5:** Quarterly framework review & update hypothesis set

---

**⚖️ Disclaimer:** Framework này là hướng dẫn kiểm thử định lượng, không là tư vấn tài chính hay giao dịch. Tất cả giao dịch đều có rủi ro. Giới hạn tối đa tổn thất theo khả năng tài chính của bạn.

**🔐 Confidential:** Giữ file này an toàn. Framework không được chia sẻ công khai vì chứa logic giao dịch proprietary.
