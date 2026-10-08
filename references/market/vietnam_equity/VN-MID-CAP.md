# Quantitative Market Characteristics — VN-MID-CAP (Round 2)

Tài liệu này tổng hợp các đặc tính thị trường, cấu trúc giao dịch, hành vi giá và cơ hội xây dựng chiến lược định lượng (Quantitative Trading) đối với Universe **VN-MID-CAP** (Nhóm cổ phiếu vốn hóa trung bình tại thị trường chứng khoán Việt Nam).

---

## 1. Tổng quan Universe

- **Thành phần cấu tạo:** Universe VN-MID-CAP bao gồm các cổ phiếu có quy mô vốn hóa tầm trung (thường dao động từ 2,000 tỷ VND đến 15,000 tỷ VND), nằm ngoài rổ chỉ số VN30 nhưng thuộc rổ chỉ số VN100 hoặc sàn HNX có thanh khoản tốt.
- **Quy mô vốn hóa:** Chiếm khoảng 20% - 25% vốn hóa toàn thị trường.
- **Thanh khoản:** Rất năng động, đóng góp lớn vào khối lượng giao dịch hàng ngày của thị trường (thường chiếm từ 30% - 40% tổng giá trị giao dịch toàn thị trường).
- **Cơ cấu ngành:** Tập trung mạnh vào các nhóm ngành nhạy bén với chu kỳ kinh tế và dòng tiền đầu cơ: Bất động sản tầm trung (Mid-cap Real Estate), Chứng khoán (Securities), Vật liệu xây dựng & Đầu tư công (Steel/Construction), Dầu khí (Oil & Gas), Thủy sản, Dệt may, Hóa chất và Phân bón.

> **[Established Knowledge] Ý nghĩa đối với Quant Trading:**
> Mid-cap là phân khúc mang lại tỷ suất sinh lời điều chỉnh rủi ro tốt nhất cho các chiến lược **Trend Following** (Bám đuổi xu hướng) và **Momentum** (Động lượng) nhờ chuyển động giá dốc, biên độ rộng và tính bám xu hướng cực kỳ rõ nét. Dung lượng vốn phù hợp cho phân khúc này là từ 50 - 150 tỷ VND.

---

## 2. Market Structure (Cấu trúc thị trường)

### Quy chế giao dịch và ảnh hưởng tới Strategy:
- **Tick Size (Bước giá):** Phân bổ trên cả HOSE và HNX:
  - Sàn HOSE: Giá dưới 10,000 VND có bước giá 10 VND; từ 10,000 - 49,950 VND có bước giá 50 VND.
  - Sàn HNX: Quy định đồng nhất bước giá 100 VND cho mọi khung giá.
  - *Ý nghĩa định lượng:* Bước giá 100 VND trên sàn HNX đối với cổ phiếu giá thấp (dưới 20,000 VND) tạo ra mức chênh lệch Bid-Ask spread theo phần trăm rất lớn (Spread cost lớn), cần được tính toán kỹ trong chi phí giao dịch ròng (Net-of-fee).
- **Biên độ dao động:** HOSE quy định biên độ $\pm 7\%$, sàn HNX là $\pm 10\%$.
  - *Ý nghĩa định lượng:* Biên độ $\pm 10\%$ của sàn HNX tạo ra xung lực giá mạnh hơn trong các phiên breakout, giúp tối ưu hóa lợi nhuận cho chiến lược động lượng.
- **Thanh khoản đối ứng:** Thanh khoản biến động mạnh theo sóng ngành. 
  - *Ý nghĩa định lượng:* Phải thiết kế bộ lọc thanh khoản di động (ví dụ: trung bình giá trị giao dịch 20 phiên > 10 tỷ VND) để loại bỏ các giai đoạn cổ phiếu rơi vào trạng thái mất thanh khoản ngắn hạn.
- **Chu kỳ T+2.5:**
  - *Ý nghĩa định lượng:* Hiện tượng bán chốt lời của hàng T+2.5 thường tạo ra các nhịp rung lắc rất mạnh của nhóm Mid-cap vào khoảng thời gian **13:30 - 14:15**, tạo cơ hội cho các lệnh mua đuổi trong phiên (Intraday Pullback) với giá tốt hơn.

---

## 3. Price Behaviour (Hành vi giá)

### Các đặc trưng hành vi giá daily:
- **High Momentum Persistence (Quán tính xu hướng cực cao):**
  - **[Established Knowledge]** Cổ phiếu Mid-cap có quán tính xu hướng mạnh nhất thị trường. Khi dòng tiền đầu cơ đồng thuận kích hoạt sóng ngành, xu hướng tăng giá của Mid-cap có độ dốc rất lớn và kéo dài ổn định từ 20 - 45 phiên daily.
- **Reliable Breakouts (Bứt phá đáng tin cậy):**
  - **[Observation]** Các phiên breakout đỉnh 20 phiên hoặc 50 phiên đi kèm khối lượng vượt trội ($> 2.0 \times \text{SMA\_Volume}(20)$) ở nhóm Mid-cap có tỷ lệ thành công (không bị lấp gap quay đầu) lên tới 65%, cao hơn rõ rệt so với Large-cap.
- **Trend-Following Gaps (Gap tiếp diễn xu hướng):**
  - **[Observation]** Khác với Large-cap, khoảng trống giá (gap) xuất hiện ở Mid-cap khi có tin tức báo cáo tài chính đột biến thường đóng vai trò là Gap tiếp diễn xu hướng (Continuation Gap) hơn là bị lấp lại ngay lập tức.
- **Sharp Pullbacks (Nhịp chỉnh dốc):**
  - **[Observation]** Do dòng tiền cá nhân chiếm tỷ trọng lớn (>85% giao dịch), các nhịp điều chỉnh (pullback) trong trend tăng của Mid-cap thường diễn ra rất nhanh và khốc liệt (thường giảm từ 10% - 15% từ đỉnh ngắn hạn trước khi bật tăng trở lại).

---

## 4. Volatility Characteristics (Đặc tính biến động)

### Bảng phân tích biến động:

| Chỉ số biến động | Đặc điểm thực tế | Ứng dụng xây dựng chiến lược |
|---|---|---|
| **Mức độ Volatility** | Cao, biên độ dao động ngày rộng. | Tạo ra mức đệm Sharpe tốt nếu kiểm soát được điểm vào lệnh. |
| **Bollinger Band Squeeze** | Biên độ co hẹp cực hạn thể hiện sự tích lũy của dòng tiền nội bộ. | Thiết kế bộ lọc phát hiện điểm bùng nổ biến động (Volatility Breakout). |
| **ATR (Average True Range)** | Biến động mạnh theo sóng ngành, ATR tăng vọt khi vào trend. | Bắt buộc sử dụng dừng lỗ động theo ATR (ví dụ: Chandelier Exit) để tránh bị rũ bỏ quá sớm. |

- **[Hypothesis] Volatility Clustering:** Sự tích lũy biến động thấp (low volatility regime) ở các ngành chứng khoán/bất động sản thường là tín hiệu báo trước cho một con sóng ngành mới khi lãi suất hoặc chính sách tiền tệ có sự dịch chuyển.

---

## 5. Volume Characteristics (Đặc tính khối lượng)

- **Mối quan hệ Price - Volume:**
  - **[Established Knowledge]** Volume là huyết mạch của cổ phiếu Mid-cap. Do phân khúc này chịu ảnh hưởng lớn từ các hội nhóm và tự doanh trong nước, sự đồng thuận về khối lượng cực kỳ quan trọng. Sự tăng giá mà không có thanh khoản hỗ trợ thường dẫn đến các cú úp bô đảo chiều nhanh (flash crash).
- **Volume Spike (Đột biến khối lượng):**
  - **[Observation]** Phiên giao dịch có khối lượng tăng đột biến vượt $3.0 \times \text{SMA\_Volume}(20)$ mà giá tăng trần ($\ge 6.8\%$) thường xác nhận dòng tiền lớn (Smart Money) đã hoàn thành giai đoạn gom hàng và bắt đầu đẩy giá.

---

## 6. Time-based Behaviour (Hành vi theo thời gian)

- **Intraday Liquidity Pattern:**
  - **[Observation]** Khác với Large-cap tập trung vào ATO/ATC, thanh khoản Mid-cap phân bổ đều hơn trong phiên. Khung giờ từ **10:00 - 11:00** sáng và **13:45 - 14:15** chiều là hai thời điểm dòng tiền đầu cơ hoạt động sôi nổi nhất và định hình xu hướng chính của ngày.
- **Hiệu ứng mùa công bố Báo cáo tài chính (Earnings Seasonality):**
  - **[Established Knowledge]** Diễn ra vào tháng 1, 4, 7, 10. Mid-cap phản ứng rất nhạy bén với thông tin doanh thu/lợi nhuận. Do thông tin cơ bản dễ bị rò rỉ sớm, giá cổ phiếu Mid-cap thường có hiện tượng tăng trước khi tin ra chính thức khoảng 1-2 tuần (Buy the rumor, sell the news).

---

## 7. Liquidity Characteristics (Đặc tính thanh khoản)

- **Bid-Ask Spread:** Thường chênh lệch từ 2 - 4 ticks giá trong những phiên thanh khoản bình thường.
- **Slippage (Trượt giá rủi ro):** Có thể xảy ra trượt giá tương đối lớn (0.5% - 1.5%) nếu đặt lệnh thị trường (Market Order) với quy mô lệnh quá lớn (vượt quá 5% khối lượng giao dịch trung bình 15 phút).
- **Liquidity Shock:** Khi thị trường chung đảo chiều xấu, thanh khoản bên mua của Mid-cap có thể biến mất rất nhanh, dẫn đến tình trạng mất thanh khoản tạm thời (dư bán sàn hàng loạt). Chiến lược cần tích hợp bộ lọc dừng lỗ khẩn cấp khi thị trường chung (VN-Index) vi phạm điều kiện an toàn.

---

## 8. Statistical Behaviour (Hành vi thống kê)

- **Return Distribution:** Phân phối lợi nhuận của Mid-cap lệch phải rõ rệt (Positive Skewness) với đuôi dày (Fat tail) bên phải. Điều này thể hiện cơ hội ăn trọn các con sóng tăng giá cực mạnh (right tail events) lớn hơn nhiều so với Large-cap.
- **Autocorrelation:** Hệ số tự tương quan bậc 1 (lag-1 autocorrelation) của tỷ suất sinh lời daily dương rất mạnh và ổn định trong các pha uptrend, khẳng định quán tính xu hướng là đặc trưng thống kê cốt lõi của Mid-cap.

---

## 9. Alpha Opportunities (Cơ hội tạo Alpha)

### 1. Sector Momentum / Leader-Follower Effect
- **Vì sao tồn tại:** Nhà đầu tư cá nhân có xu hướng giao dịch theo tâm lý đám đông và sóng ngành. Khi cổ phiếu đầu ngành (Leader) bứt phá tăng trần, dòng tiền sẽ nhanh chóng lan tỏa sang các cổ phiếu Mid-cap cùng ngành có hệ số Beta cao (Followers).
- **Thời điểm hoạt động:** Giai đoạn đầu và giữa của sóng ngành.
- **Khi nào mất hiệu lực:** Giai đoạn cuối của chu kỳ tăng trưởng, khi thị trường bước vào pha phân phối toàn diện.
- **Kiểm chứng Backtest:**
  - Tính toán đà tăng trung bình của top 3 cổ phiếu lớn nhất ngành.
  - Nếu đà tăng này vượt ngưỡng xác định, thực hiện mua các cổ phiếu Mid-cap cùng ngành có xung lực giá tốt nhất.

### 2. Volatility Breakout (BB Squeeze)
- **Vì sao tồn tại:** Quá trình tích lũy chặt chẽ của dòng tiền thông minh làm cạn kiệt thanh khoản và nén chặt biên độ dao động trước khi bùng nổ xu hướng mới.
- **Thời điểm hoạt động:** Cổ phiếu đi ngang sideway dài từ 3-4 tuần.
- **Khi nào mất hiệu lực:** Thị trường chung đi ngang không xu hướng (Choppy market).
- **Kiểm chứng Backtest:**
  - Feature đo độ rộng Bollinger Band nhỏ hơn phân vị thứ 15 lịch sử.
  - Mua khi giá đóng cửa cắt lên đường biên trên của Bollinger Band đi kèm Volume lớn.

---

## 10. Feature Ideas (Gợi ý Thiết kế Đặc trưng)

1. `Sector_Relative_Strength_Panel`:
   - *Cách tính:* Lấy lợi nhuận 5 ngày của cổ phiếu chia cho lợi nhuận 5 ngày trung bình của nhóm ngành tương ứng.
   - *Đo lường:* Xác định cổ phiếu mạnh nhất trong sóng ngành.
2. `ATR_Compression_Ratio_Panel`:
   - *Cách tính:* `ATR_Panel(pv_close_panel, 5) / ATR_Panel(pv_close_panel, 20)`.
   - *Đo lường:* Phát hiện trạng thái thắt nút cổ chai để chuẩn bị cho chiến lược breakout.
3. `Volume_Acceleration_Panel`:
   - *Cách tính:* `pv_volume_panel / SMA_panel(pv_volume_panel, 20)`.
   - *Đo lường:* Đo mức độ gia tốc của dòng tiền lớn tham gia.

---

## 11. Strategy Opportunities (Cơ hội Chiến lược)

- **Trend Following (Rất phù hợp):** Vận hành các hệ thống bám đuổi xu hướng trung hạn sử dụng các đường trung bình động (EMA 10/30) hoặc kênh Donchian.
- **Swing Trading / Sector Rotation (Rất phù hợp):** Đánh theo chu kỳ luân chuyển dòng tiền giữa các nhóm ngành Mid-cap lớn (Chứng khoán -> Bất động sản -> Đầu tư công).
- **Breakout Strategy (Phù hợp):** Khai thác các mô hình bứt phá đỉnh cũ đi kèm khối lượng đột biến.

---

## 12. Những điều cần tránh (Caveats & Risks)

- **Tránh mua đuổi ở cuối sóng ngành:** Biên độ dao động lớn khiến rủi ro đu đỉnh ngắn hạn ở Mid-cap rất cao. Cần thiết kế bộ lọc RSI hoặc quá mua để ngăn chặn lệnh mua đuổi khi giá đã tăng liên tục > 4 phiên.
- **Tránh dùng Mean Reversion thuần túy trong downtrend:** Cổ phiếu Mid-cap có xu hướng giảm giá liên tục mà không có sự phục hồi kỹ thuật đáng kể nếu đã gãy xu hướng dài hạn.
- **Tránh giao dịch các mã thiếu thanh khoản tự nhiên:** Loại bỏ các mã có khối lượng giao dịch thất thường hoặc do đội lái tự quay tay tạo thanh khoản ảo.

---

## 13. So sánh chéo với các Universe khác

| Đặc tính | VN-MID-CAP | VN-LARGE-CAP | VN-SMALL-CAP |
|---|---|---|---|
| **Độ bám xu hướng** | **Mạnh nhất** (Trend kéo dài và dốc) | Trung bình (Nhiều nhịp dừng chỉnh) | Ngắn hạn (Dễ bị bẻ gãy xu hướng) |
| **Biến động (Volatility)** | **Cao** (Biên độ dao động tốt) | Thấp (Biên độ hẹp) | Cực cao (Khó dự báo) |
| **Rủi ro mất thanh khoản** | **Vừa phải** (Có thể bán được khi cần) | Hầu như không có | Cực cao (Rủi ro kẹt sàn bán không ai mua) |
| **Đặc trưng Alpha** | **Sector Rotation & PEAD** | ETF Arbitrage & Foreign Flow | Liquidity & Anomalies |
| **Dung lượng vốn (Capacity)** | **Trung bình (50 - 150 tỷ)** | Lớn nhất (> 500 tỷ) | Rất nhỏ (< 20 tỷ) |

---
*— Tài liệu tham khảo nội bộ dành riêng cho Quant Research Project —*