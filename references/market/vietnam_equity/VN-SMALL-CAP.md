# Quantitative Market Characteristics — VN-SMALL-CAP (Round 2)

Tài liệu này tổng hợp các đặc tính thị trường, cấu trúc giao dịch, hành vi giá và cơ hội xây dựng chiến lược định lượng (Quantitative Trading) đối với Universe **VN-SMALL-CAP** (Nhóm cổ phiếu vốn hóa nhỏ / Penny tại thị trường chứng khoán Việt Nam).

---

## 1. Tổng quan Universe

- **Thành phần cấu tạo:** Universe VN-SMALL-CAP bao gồm các cổ phiếu có quy mô vốn hóa nhỏ (thường dưới 2,000 tỷ VND), chủ yếu là các cổ phiếu có thị giá thấp (dưới 10,000 VND, thường gọi là "cổ phiếu trà đá") giao dịch trên sàn HOSE, HNX và sàn UPCoM.
- **Quy mô vốn hóa:** Chiếm chưa đầy 10% tổng vốn hóa toàn thị trường.
- **Thanh khoản:** Rất thấp trong điều kiện bình thường, nhưng có thể tăng vọt đột biến khi có sóng đầu cơ. Giá trị giao dịch hàng ngày của cả nhóm thường chiếm dưới 15% toàn thị trường.
- **Cơ cấu ngành:** Đa dạng nhưng chất lượng tài chính thấp. Thường gồm doanh nghiệp bất động sản quy mô nhỏ, xây dựng dân dụng, nông nghiệp, và các doanh nghiệp đang gặp khó khăn tài chính, tái cấu trúc hoặc có nguy cơ hủy niêm yết.

> **[Established Knowledge] Ý nghĩa đối với Quant Trading:**
> Small-cap là nhóm cổ phiếu có rủi ro hệ thống và rủi ro thanh khoản cao nhất. Tuy nhiên, đây lại là mỏ vàng để khai thác các **Alpha dị biệt (Anomalies)** ngắn hạn nhờ biên độ biến động cực lớn và quán tính tăng trần liên tiếp. Chiến lược chạy trên universe này bắt buộc phải giới hạn dung lượng vốn cực nhỏ (Capacity < 20 tỷ VND) để tránh tác động làm méo mó giá.

---

## 2. Market Structure (Cấu trúc thị trường)

### Quy chế giao dịch và ảnh hưởng tới Strategy:
- **Tick Size (Bước giá):**
  - Sàn HOSE: Do hầu hết thị giá dưới 10,000 VND, bước giá là 10 VND.
  - Sàn HNX và UPCoM: Quy định bước giá 100 VND.
  - *Ý nghĩa định lượng:* Bước giá 100 VND đối với cổ phiếu giá 3,000 - 5,000 VND trên HNX/UPCoM tạo ra khoảng trống Bid-Ask spread cực rộng tính theo % thị giá (2% - 3% giá trị vị thế trên mỗi tick). Chiến lược giao dịch bắt buộc phải sử dụng các lệnh giới hạn (Limit Order) thay vì lệnh thị trường để kiểm soát chi phí spread này.
- **Biên độ dao động:** HOSE $\pm 7\%$, HNX $\pm 10\%$, UPCoM $\pm 15\%$.
  - *Ý nghĩa định lượng:* Biên độ $\pm 15\%$ của sàn UPCoM tạo ra mức độ bùng nổ giá cực mạnh, nhưng cũng đi kèm rủi ro sụt giảm tài sản cực lớn trong một phiên.
- **Hạn chế giao dịch và cảnh báo:** Nhiều mã Small-cap thuộc diện bị cảnh báo, kiểm soát, hoặc chỉ được giao dịch vào phiên chiều.
  - *Ý nghĩa định lượng:* Phải xây dựng bộ lọc tiền xử lý dữ liệu (data preprocessing) để tự động loại bỏ các cổ phiếu bị hạn chế giao dịch hoặc có lịch sử ngừng giao dịch đột ngột.
- **Không có đòn bẩy (No Margin):** Hầu hết Small-cap không được các CTCK cấp margin.
  - *Ý nghĩa định lượng:* Mô hình phân bổ vốn phải là Long-only bằng tiền mặt và không phụ thuộc vào nguồn vốn vay.

---

## 3. Price Behaviour (Hành vi giá)

### Các đặc trưng hành vi giá daily:
- **Christmas Tree Pattern (Mô hình Cây thông Noel):**
  - **[Established Knowledge]** Chu kỳ chuyển động giá của Small-cap rất ngắn và đối xứng: Giá tăng dốc đứng trần liên tiếp trong nhiều phiên (đẩy giá), sau đó rơi tự do sàn liên tiếp không có thanh khoản (giảm sàn mất thanh khoản) tạo thành hình cây thông trên đồ thị.
- **Consecutive Limit Locks (Hiện tượng khóa trần/sàn liên tục):**
  - **[Observation]** Khi dòng tiền đầu cơ cá nhân hưng phấn, cổ phiếu Small-cap có xác suất khóa trần (Limit Up) liên tiếp từ 5 - 10 phiên rất cao. Hiện tượng tự tương quan dương của return daily lúc này đạt mức tối đa.
- **High False Breakout Rate:**
  - **[Observation]** Các điểm breakout đỉnh cũ ở Small-cap có tỷ lệ thất bại rất cao do dòng tiền đầu cơ rút đi nhanh chóng khi thị trường chung có dấu hiệu rủi ro.
- **Extreme Gaps (Khoảng trống giá cực đoan):**
  - **[Observation]** Gaps xuất hiện ở Small-cap thường là các khoảng trống trần/sàn mở phiên do lệnh mua/bán tích lũy từ đêm hôm trước đè bẹp lượng thanh khoản đối ứng sẵn có.

---

## 4. Volatility Characteristics (Đặc tính biến động)

### Bảng phân tích biến động:

| Chỉ số biến động | Đặc điểm thực tế | Ứng dụng xây dựng chiến lược |
|---|---|---|
| **Mức độ Volatility** | **Cực cao và không ổn định.** | Cần sử dụng các bộ lọc biến động để tránh các pha giật giá vô hướng. |
| **Volatility Squeeze** | Cổ phiếu đi ngang cạn kiệt biến động trong nhiều tháng (biến động gần bằng 0). | Thời điểm gom tích lũy giá rẻ cho chiến lược Mean Reversion dài hạn. |
| **ATR (Average True Range)** | ATR biến động cực mạnh và gián đoạn (Spiky ATR). | Không nên dùng ATR để tính quy mô dừng lỗ quá chặt vì dễ bị quét sai hướng do nhiễu. |

- **[Hypothesis] Volatility Jump:** Sự tăng vọt đột ngột của biến động đi kèm Volume bắt đầu nhích lên từ vùng đáy tích lũy là tín hiệu sớm báo hiệu sóng đầu cơ bắt đầu.

---

## 5. Volume Characteristics (Đặc tính khối lượng)

- **Hiện tượng Khóa thanh khoản (Liquidity Lock):**
  - **[Established Knowledge]** Trong pha đẩy giá mạnh, cổ phiếu rơi vào trạng thái "Dư mua trần" hàng triệu đơn vị nhưng khối lượng khớp lệnh hàng ngày cực nhỏ (Dry Volume) do không ai bán ra. Ngược lại, trong pha giảm, hiện tượng "Dư bán sàn" không ai mua làm tê liệt khả năng thoát vị thế.
- **Volume Spike ở đáy:**
  - **[Observation]** Một phiên Volume Spike vượt $> 4.0 \times \text{SMA\_Volume}(20)$ xuất hiện tại vùng giá đi ngang đáy lịch sử thường là dấu hiệu gom hàng chủ động của Smart Money (đội lái).

---

## 6. Time-based Behaviour (Hành vi theo thời gian)

- **Hiệu ứng cuối sóng thị trường (Late-Stage Effect):**
  - **[Established Knowledge]** Sóng Penny (Small-cap) thường xuất hiện vào giai đoạn cuối cùng của một chu kỳ tăng trưởng thị trường chung (Bull Market). Khi các nhóm cổ phiếu Large-cap và Mid-cap đã tăng quá cao và chững lại, dòng tiền nóng của nhà đầu tư cá nhân sẽ tìm đến Small-cap để đầu cơ ngắn hạn.
- **Thời gian khớp lệnh trong ngày:**
  - **[Observation]** Giao dịch sôi động nhất tập trung vào đầu phiên sáng (9:15 - 10:00) khi các lệnh mua/bán trần sàn được đẩy vào nhanh để tranh quyền ưu tiên khớp lệnh.

---

## 7. Liquidity Characteristics (Đặc tính thanh khoản)

- **Rủi ro trượt giá (Slippage):** Cực kỳ lớn. Nếu thoát vị thế bằng lệnh thị trường (MP/ATC) trong phiên giảm, mức độ trượt giá có thể lên tới 5% - 7% ngay lập tức.
- **Độ sâu thị trường (Market Depth):** Rất mỏng. Sổ lệnh (order book) thường trống rỗng ở các bước giá trung gian, chỉ tập trung lệnh ở giá trần hoặc giá sàn.
- **Ảnh hưởng tới Strategy:** Mô hình định lượng bắt buộc phải tính toán chi phí ma sát trượt giá cực cao (ví dụ: tối thiểu 2% - 3% cho mỗi vòng giao dịch) để đảm bảo kết quả backtest không bị ảo.

---

## 8. Statistical Behaviour (Hành vi thống kê)

- **Fat Tails & High Kurtosis:** Phân phối tỷ suất sinh lời của Small-cap có độ nhọn cực kỳ lớn và đuôi rất dài ở cả hai phía. Điều này có nghĩa là các sự kiện cực đoan (giảm sàn liên tục hoặc tăng trần liên tục) xảy ra với tần suất lớn hơn nhiều so với dự báo của lý thuyết tài chính thông thường.
- **Day-of-week Effect:**
  - **[Hypothesis]** Cổ phiếu Small-cap có xu hướng bị bán mạnh vào ngày Thứ Sáu do tâm lý e ngại tin tức xấu cuối tuần của nhà đầu tư cá nhân nhỏ lẻ.

---

## 9. Alpha Opportunities (Cơ hội tạo Alpha)

### 1. Late-Stage Market Rotation (Sóng Penny cuối mùa)
- **Vì sao tồn tại:** Quá trình luân chuyển dòng tiền thông thường khi Large/Mid đã cạn kiệt biên lợi nhuận, dòng tiền nóng tìm kiếm cơ hội sinh lời nhanh ở Penny.
- **Thời điểm hoạt động:** Khi chỉ số VN-Index đi ngang ở vùng đỉnh với thanh khoản cao nhưng giá không tăng thêm, đồng thời khối lượng giao dịch nhóm Small-cap tăng đột biến.
- **Khi nào mất hiệu lực:** Khi thị trường chung bắt đầu sụp đổ (dẫn đến bán tháo toàn diện).
- **Kiểm chứng Backtest:**
  - Tạo feature so sánh volume Small-cap với volume toàn thị trường.
  - Mua rổ Small-cap khi tỷ lệ này vượt phân vị thứ 90 lịch sử và VN-Index đi ngang.

### 2. Historical Low Mean Reversion
- **Vì sao tồn tại:** Doanh nghiệp Small-cap dù xấu nhưng tài sản thanh lý hoặc giá trị nội tại tối thiểu vẫn cao hơn mức giá rẻ mạt của cổ phiếu sau nhiều năm bị lãng quên.
- **Thời điểm hoạt động:** Giai đoạn thị trường sideway kéo dài.
- **Khi nào mất hiệu lực:** Doanh nghiệp thực sự phá sản hoặc bị hủy niêm yết bắt buộc.
- **Kiểm chứng Backtest:**
  - Tìm các cổ phiếu có giá trị sổ sách (B/P) cực cao và giá đi ngang trong biên độ thắt chặt < 5% trong suốt 60 ngày.
  - Mua tích lũy và nắm giữ dài hạn.

---

## 10. Feature Ideas (Gợi ý Thiết kế Đặc trưng)

1. `Limit_Up_Lock_Days`:
   - *Cách tính:* Số ngày liên tiếp giá đóng cửa bằng đúng giá trần tối đa của phiên.
   - *Đo lường:* Sức mạnh của quán tính đầu cơ (Momentum).
2. `Historical_Low_Duration`:
   - *Cách tính:* Số phiên liên tiếp giá dao động trong vùng đáy $\pm 5\%$ của 250 phiên.
   - *Đo lường:* Phát hiện trạng thái tích lũy cạn kiệt trước khi tạo sóng.
3. `Penny_Volume_Spike_Flag`:
   - *Cách tính:* `1` nếu `pv_volume_panel > 4.0 * SMA_panel(pv_volume_panel, 20)` tại vùng đáy, ngược lại bằng `0`.
   - *Đo lường:* Tín hiệu kích hoạt gom hàng của Smart Money.

---

## 11. Strategy Opportunities (Cơ hội Chiến lược)

- **Mean Reversion / Value Accumulation (Rất phù hợp):** Mua gom các cổ phiếu có định giá cực rẻ ở vùng tích lũy dài hạn và kiên nhẫn đợi sóng đầu cơ kéo giá lên.
- **Liquidity Strategy (Phù hợp):** Khai thác các bất cân xứng cung cầu ngắn hạn và các đợt bùng nổ dòng tiền.
- **Trend Following dài hạn (Hoàn toàn KHÔNG phù hợp):** Không chạy các chiến lược bám xu hướng dài hạn ở penny vì xu hướng đảo chiều cực nhanh và gãy sâu không có thanh khoản thoát hàng.

---

## 12. Những điều cần tránh (Caveats & Risks)

- **Bẫy Backtest ảo (Paper Profit Bias):** Tránh tin vào kết quả backtest có Sharpe > 3.0 ở penny nếu chưa cộng chi phí trượt giá (Slippage) tối thiểu 2% - 3% mỗi chiều và chưa lọc điều kiện mất thanh khoản (dư bán sàn không khớp được).
- **Tránh mua đuổi khi đã có > 3 phiên trần:** Mua đuổi penny khi đã tăng nóng có rủi ro kẹt hàng giảm sàn không thể bán được (Christmas Tree Trap).
- **Tránh giao dịch quy mô vốn lớn:** Phân bổ vốn cho Small-cap chỉ nên chiếm tỷ trọng nhỏ (< 10%) trong toàn bộ danh mục giao dịch.

---

## 13. So sánh chéo với các Universe khác

| Đặc tính | VN-SMALL-CAP | VN-MID-CAP | VN-LARGE-CAP |
|---|---|---|---|
| **Rủi ro thanh khoản** | **Cao nhất** (Dễ bị kẹt sàn, không bán được) | Thấp (Dễ xử lý vị thế) | Hầu như không có |
| **Tính bám xu hướng dài**| **Thấp nhất** (Chủ yếu là sóng ngắn dốc) | Cao nhất (Trend dốc bền vững) | Trung bình (Trend chậm ổn định) |
| **Rủi ro thao túng giá** | **Cao nhất** (Dễ bị đội lái điều khiển) | Vừa phải | Thấp nhất |
| **Dung lượng vốn (Capacity)**| **Rất nhỏ (< 20 tỷ)** | Trung bình (50 - 150 tỷ) | Lớn nhất (> 500 tỷ) |
| **Tick Size Impact** | **Rất lớn** (Spread cost tính theo % lớn) | Vừa phải | Nhỏ nhất |

---
*— Tài liệu tham khảo nội bộ dành riêng cho Quant Research Project —*