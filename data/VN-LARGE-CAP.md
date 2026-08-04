# Quantitative Market Characteristics — VN-LARGE-CAP (Round 2)

Tài liệu này tổng hợp các đặc tính thị trường, cấu trúc giao dịch, hành vi giá và cơ hội xây dựng chiến lược định lượng (Quantitative Trading) đối với Universe **VN-LARGE-CAP** (Nhóm cổ phiếu vốn hóa lớn tại thị trường chứng khoán Việt Nam).

---

## 1. Tổng quan Universe

- **Thành phần cấu tạo:** Universe VN-LARGE-CAP bao gồm các cổ phiếu có quy mô vốn hóa lớn nhất thị trường, chủ yếu nằm trong rổ chỉ số VN30 hoặc VN100 đáp ứng các tiêu chuẩn khắt khe về tỷ lệ tự do chuyển nhượng (free-float) và thanh khoản giao dịch.
- **Quy mô vốn hóa:** Chiếm hơn 70% tổng vốn hóa toàn thị trường chứng khoán Việt Nam.
- **Thanh khoản:** Chiếm tỷ trọng lớn nhất về giá trị giao dịch hàng ngày (thường dao động từ 40% - 60% tổng giá trị giao dịch của sàn HOSE).
- **Cơ cấu ngành:** Chiếm ưu thế tuyệt đối bởi nhóm ngành Ngân hàng (Financials/Banks), Bất động sản vốn hóa lớn (Real Estate), Tiêu dùng thiết yếu (Consumer Staples - VNM, MSN), Tập đoàn đa ngành (VIC, VHM) và Công nghệ/Bán lẻ (FPT, MWG).

> **[Established Knowledge] Ý nghĩa đối với Quant Trading:**
> Universe này là môi trường lý tưởng nhất để vận hành các chiến lược có dung lượng vốn lớn (Capacity cao > 500 tỷ VND) nhờ độ rộng thị trường sâu. Đây là chân Long/Short cốt lõi khi thiết kế các chiến lược Market Neutral (Trung lập thị trường) nhằm triệt tiêu hệ số Beta hệ thống.

---

## 2. Market Structure (Cấu trúc thị trường)

### Quy chế giao dịch và ảnh hưởng tới Strategy:
- **Tick Size (Bước giá):** Trên sàn HOSE, bước giá được chia theo 3 phân khúc. Đối với Large-cap, giá hầu hết nằm ở phân khúc giá cao:
  - Giá từ 10,000 - 49,950 VND: Bước giá là 50 VND.
  - Giá từ 50,000 VND trở lên: Bước giá là 100 VND.
  - *Ý nghĩa định lượng:* Bước giá lớn so với thị giá giúp giảm thiểu hiện tượng nhiễu bảng điện (nhiễu vi cấu trúc) và tạo ra vùng Bid-Ask spread tương đối vững chãi.
- **Biên độ dao động:** HOSE quy định biên độ hàng ngày là $\pm 7\%$.
- **Cơ chế khớp lệnh định kỳ (ATO & ATC):** 
  - Phiên ATO (9:00 - 9:15) và ATC (14:30 - 14:45) là nơi tập trung khối lượng giao dịch cực kỳ lớn từ các tổ chức lớn.
  - *Ý nghĩa định lượng:* Phiên ATC là thời điểm duy nhất các quỹ ETF thực hiện cơ cấu danh mục (Rebalancing). Điều này tạo ra một lượng cung/cầu nhân tạo khổng lồ, thường gây ra hiện tượng lệch giá tạm thời (temporary price pressure) vào đúng giây cuối cùng của phiên ATC.
- **Room khối ngoại (Foreign Ownership Limit):** Các cổ phiếu cột trụ như FPT, MWG, REE thường xuyên kín room ngoại.
  - *Ý nghĩa định lượng:* Khi một cổ phiếu hở room ngoại, áp lực mua đuổi từ các quỹ nước ngoài sẽ kích hoạt một đợt tăng giá có quán tính rất cao (Momentum).
- **Chu kỳ thanh toán T+2.5:** Cổ phiếu mua ngày T sẽ về tài khoản vào chiều ngày T+2, cho phép giao dịch từ phiên chiều ngày T+2.
  - *Ý nghĩa định lượng:* Áp lực bán lượng hàng T+2 thường tập trung mạnh vào khung giờ từ **13:00 - 14:00** hàng ngày, tạo ra một dip giảm giá ngắn hạn (intraday dip).

---

## 3. Price Behaviour (Hành vi giá)

### Các đặc trưng hành vi giá daily:
- **Momentum Persistence (Quán tính xu hướng dài):**
  - **[Established Knowledge]** Cổ phiếu Large-cap có quán tính xu hướng rất bền vững một khi đã hình thành trend. Nguyên nhân do các quỹ đầu tư lớn (mutual funds, pension funds) cần nhiều tuần để giải ngân xong một vị thế lớn, tạo ra áp lực mua/bán ròng kéo dài.
- **Mean Reversion (Đảo chiều trung bình):**
  - **[Observation]** Khi giá dịch chuyển quá 2 độ lệch chuẩn (Z-score > 2) so với đường trung bình di động 20 ngày (SMA20) mà không có tin tức cơ bản hỗ trợ, Large-cap có xác suất đảo chiều về mức trung bình đạt trên 70% trong vòng 5 phiên tiếp theo.
- **False Breakout (Đột phá giả):**
  - **[Hypothesis]** Do lượng cung treo lơ lửng (overhead supply) của Large-cap rất dày từ các cổ đông lớn và nhà đầu tư kẹt hàng cũ, các phiên breakout đỉnh lịch sử mà không có sự xác nhận của khối lượng tối thiểu lớn gấp 2 lần trung bình 20 ngày hầu hết sẽ thất bại (False Breakout) và quay đầu lấp gap.
- **Gap & Gap Fill (Khoảng trống giá):**
  - **[Observation]** Khoảng trống giá (gap) xuất hiện ở phiên ATO của Large-cap chủ yếu do tác động tâm lý từ thị trường chứng khoán Mỹ (chỉ số S&P500/Dow Jones) đêm hôm trước. Các khoảng trống này có xu hướng bị lấp (Gap Fill) trong vòng 3 phiên giao dịch tiếp theo với tỷ lệ lấp gap lên tới 75%.

---

## 4. Volatility Characteristics (Đặc tính biến động)

### Bảng phân tích biến động:

| Chỉ số biến động | Đặc điểm thực tế | Ứng dụng xây dựng chiến lược |
|---|---|---|
| **Mức độ Volatility** | Thấp và ổn định hơn so với Mid-cap và Small-cap. | Phù hợp làm trục tham chiếu rủi ro (Risk Benchmark). |
| **Volatility Clustering** | Biến động mạnh diễn ra theo cụm quanh mùa báo cáo tài chính (Qúy 1, 2, 3, 4) và các kỳ cơ cấu ETF. | Sử dụng mô hình GARCH để dự báo biến động cho việc điều chỉnh vị thế động (Dynamic Sizing). |
| **ATR (Average True Range)** | ATR biến thiên chậm, giữ xu hướng ổn định trong nhiều tuần. | Đặt Stop Loss cứng dựa trên $2 \times \text{ATR}(14)$ rất ít khi bị quét nhiễu (whipsaw). |

- **[Hypothesis] Volatility Expansion:** Các giai đoạn thắt chặt biên độ dao động (Bollinger Band nén chặt) kéo dài trên 15 phiên daily thường dẫn đến một đợt bùng nổ biến động cực mạnh khi có tin tức lợi nhuận hoặc cơ cấu quỹ.

---

## 5. Volume Characteristics (Đặc tính khối lượng)

- **Mối quan hệ Price - Volume:** 
  - **[Established Knowledge]** Ở nhóm Large-cap, dòng tiền thông minh (Smart Money) thể hiện rất rõ qua khối lượng. Sự tăng giá bền vững bắt buộc phải đi kèm khối lượng tăng dần. Mọi đợt tăng giá đi kèm khối lượng sụt giảm (Volume Divergence) đều là tín hiệu cảnh báo phân phối sớm.
- **Volume Spike (Đột biến khối lượng):**
  - **[Observation]** Một phiên Volume Spike vượt $2.5 \times \text{SMA\_Volume}(20)$ ở Large-cap thường đánh dấu sự tham gia của các tổ chức lớn hoặc các quỹ ETF cơ cấu danh mục. Nếu giá tăng kịch trần (tăng $\ge 6.5\%$), đây là điểm bắt đầu của một chu kỳ tăng trưởng trung hạn (xu hướng kéo dài tối thiểu 15-30 phiên).

---

## 6. Time-based Behaviour (Hành vi theo thời gian)

- **Hiệu ứng phiên ATC (ATC Effect):**
  - **[Established Knowledge]** Phiên ATC (14:30 - 14:45) chiếm từ 20% - 35% thanh khoản toàn phiên của Large-cap. Sự dịch chuyển giá trong ATC có tính định hướng rất cao cho phiên tiếp theo.
- **Mùa cơ cấu quỹ (ETF Rebalancing Seasonality):**
  - **[Established Knowledge]** Diễn ra vào tuần thứ 3 của các tháng 3, 6, 9, 12 hàng năm. Các cổ phiếu được dự báo thêm vào rổ chỉ số lớn (như VN30, FTSE, VNM) thường có hiện tượng tăng giá trước đó 2 tuần và bị bán mạnh (hoặc mua mạnh) vào đúng phiên ATC của ngày cơ cấu cuối cùng.
- **Hiệu ứng chốt NAV cuối quý (Window Dressing Effect):**
  - **[Observation]** Vào tuần giao dịch cuối cùng của Quý 2 (tháng 6) và Quý 4 (tháng 12), các quỹ đầu tư lớn thường có xu hướng kéo giá các cổ phiếu cột trụ nắm giữ nhiều để làm đẹp báo cáo tài sản (NAV).

---

## 7. Liquidity Characteristics (Đặc tính thanh khoản)

- **Bid-Ask Spread:** Cực kỳ mỏng, thường chỉ chênh lệch 1 tick giá đối với các mã dẫn đầu (VCB, HPG, FPT, MBB).
- **Slippage (Trượt giá):** Rất thấp. Thích hợp cho việc xây dựng các mô hình phân bổ danh mục quy mô lớn mà không sợ tác động tiêu cực của chi phí trượt giá ăn mòn Sharpe.
- **Liquidity Shock:** Hiếm khi xảy ra đột ngột trong điều kiện thị trường bình thường. Tuy nhiên, trong các đợt thị trường chung hoảng loạn (Systemic Risk), Large-cap là nhóm bị các quỹ bán đầu tiên để thu hồi tiền mặt (do tính thanh khoản cao nhất), tạo ra hiện tượng bán tháo diện rộng tạm thời.

---

## 8. Statistical Behaviour (Hành vi thống kê)

- **Return Distribution:** Phân phối tỷ suất sinh lời của Large-cap gần phân phối chuẩn nhất trong 3 phân khúc, tuy nhiên vẫn tồn tại đặc tính đuôi dày (fat tail) lệch trái (tức là có rủi ro sụt giảm mạnh đột ngột lớn hơn xác suất phân phối chuẩn dự báo).
- **Earnings Drift (PEAD):**
  - **[Established Knowledge]** Thống kê lịch sử cho thấy các cổ phiếu Large-cap công bố EPS vượt kỳ vọng đồng thuận (consensus EPS) của thị trường từ 15% trở lên sẽ có hiệu suất vượt trội (outperform) so với rổ chỉ số chung trong vòng 40 ngày giao dịch tiếp theo.

---

## 9. Alpha Opportunities (Cơ hội tạo Alpha)

### 1. ETF Rebalancing Arbitrage
- **Vì sao tồn tại:** Luật lệ hoạt động của các quỹ ETF buộc họ phải mua/bán một lượng cổ phiếu định trước vào phiên ATC ngày cơ cấu để giảm thiểu sai số bám sát chỉ số (tracking error).
- **Thời điểm hoạt động:** 2 tuần trước ngày cơ cấu ETF chính thức.
- **Khi nào mất hiệu lực:** Khi thông tin danh mục thay đổi đã được thị trường phản ánh hết vào giá quá sớm (fully priced in).
- **Kiểm chứng Backtest:** 
  - Khởi tạo tín hiệu mua tại ngày công bố danh mục ETF mới cho các mã được thêm vào.
  - Thoát vị thế ở phiên ATC ngày cơ cấu cuối cùng hoặc phiên ATO ngày tiếp theo.

### 2. Foreign Net Flow Momentum
- **Vì sao tồn tại:** Khối ngoại giải ngân theo dòng vốn lớn dài hạn. Lực mua liên tục tạo ra sự mất cân bằng cung cầu tạm thời kéo dài.
- **Thời điểm hoạt động:** Thị trường có xu hướng rõ ràng, dòng vốn FDI hoặc dòng vốn ngoại tệ chảy vào mạnh.
- **Khi nào mất hiệu lực:** Giai đoạn tỷ giá căng thẳng hoặc khối ngoại đảo chiều rút vốn đồng loạt.
- **Kiểm chứng Backtest:**
  - Định nghĩa tín hiệu mua khi tỷ lệ mua ròng khối ngoại trên tổng khối lượng (`Foreign_Net_Ratio`) vượt 20% liên tiếp trong 5 ngày.
  - Thoát khi tỷ lệ này chuyển sang bán ròng hoặc giá cắt xuống SMA20.

---

## 10. Feature Ideas (Gợi ý Thiết kế Đặc trưng)

1. `Foreign_Net_Ratio_Panel`: 
   - *Cách tính:* `(Foreign_Buy_Volume - Foreign_Sell_Volume) / Total_Volume`.
   - *Đo lường:* Lực mua ròng của khối ngoại trên lát cắt ngang.
2. `ATC_Volume_Dominance`:
   - *Cách tính:* `ATC_Volume / Total_Daily_Volume`.
   - *Đo lường:* Sự chú ý của dòng tiền tổ chức/quỹ lớn tại phiên đóng cửa.
3. `Distance_to_EMA200_Panel`:
   - *Cách tính:* `(pv_close_panel - EMA_panel(pv_close_panel, 200)) / pv_close_panel`.
   - *Đo lường:* Mức độ lệch khỏi giá trị nội tại dài hạn để phục vụ chiến lược Mean Reversion hoặc lọc trend.
4. `Relative_Strength_Index_Panel`:
   - *Cách tính:* Xếp hạng chéo (rank) tốc độ tăng giá của cổ phiếu so với VN30 Index.
   - *Đo lường:* Xác định cổ phiếu Large-cap đang dẫn đầu dòng tiền.

---

## 11. Strategy Opportunities (Cơ hội Chiến lược)

- **Market Neutral (Rất phù hợp):** Long nhóm Large-cap có cơ bản xuất sắc (ROA cao, định giá rẻ) đồng thời Short nhóm Large-cap có cơ bản kém (hoặc Short VN30 Future đối ứng) để ăn chênh lệch alpha ròng và triệt tiêu biến động thị trường.
- **Trend Following (Phù hợp):** Sử dụng các mô hình theo đuổi xu hướng trung và dài hạn (ví dụ: EMA Crossover, Donchian Channel Breakout) vì Large-cap ít bị nhiễu và có xu hướng kéo dài ổn định.
- **Sector Rotation (Phù hợp):** Luân chuyển dòng tiền giữa các nhóm ngành lớn (Ngân hàng, Bất động sản, Thép) dựa trên đà tăng trưởng của ngành.

---

## 12. Những điều cần tránh (Caveats & Risks)

- **Tránh đánh Breakout ngắn hạn tần suất cao:** Large-cap chịu chi phí ma sát và có nhiều false breakout ngắn hạn. Tối ưu hóa mô hình breakout trên nến daily cần thời gian nắm giữ dài (> 10 phiên).
- **Tránh bỏ qua biến số Khối ngoại:** Không đưa dữ liệu giao dịch của khối ngoại vào bộ lọc feature ở VN-LARGE-CAP là một thiếu sót lớn làm giảm độ chính xác của mô hình.
- **Bẫy Overfitting trong mùa báo cáo:** Tránh tối ưu hóa quá mức tham số mô hình xung quanh ngày ra báo cáo tài chính (Qúy) vì biến động tại thời điểm này mang tính chất nhiễu thông tin ngắn hạn rất lớn.

---

## 13. So sánh chéo với các Universe khác

| Đặc tính | VN-LARGE-CAP | VN-MID-CAP | VN-SMALL-CAP |
|---|---|---|---|
| **Thanh khoản** | **Cực cao** (Dễ khớp lệnh lớn, trượt giá tối thiểu) | Trung bình (Slippage vừa phải) | Thấp (Dễ bị kẹt thanh khoản) |
| **Biến động (Volatility)** | **Thấp nhất** (Chuyển động giá mượt) | Cao (Tạo biên độ swing tốt) | Cực cao (Rủi ro đuôi lớn) |
| **Dung lượng vốn (Capacity)** | **Lớn nhất (> 500 tỷ)** | Trung bình (50 - 150 tỷ) | Nhỏ (< 20 tỷ) |
| **Tỷ lệ False Breakout** | **Cao nhất** (Cần xác nhận Volume lớn) | Trung bình | Thấp (Nhưng dễ gặp rủi ro thao túng giá) |
| **Chiến lược tối ưu** | **Market Neutral, ETF Arbitrage** | **Trend Following, Swing Trading** | **Mean Reversion, Liquidity Strategy** |

---
*— Tài liệu tham khảo nội bộ dành riêng cho Quant Research Project —*