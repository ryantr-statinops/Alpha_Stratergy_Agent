class CustomStrategy(SimpleAlgorithm):
    # Chỉ giữ lại các tham số thực sự cần thiết
    htf_window = 100
    bb_window = 20
    vol_window = 20
    atr_period = 14
    atr_mult = 2.2

    def __algorithm__(self):
        # 1. Dữ liệu
        close, high, low, vol = self.data.pv_vn30_close, self.data.pv_vn30_high, self.data.pv_vn30_low, self.data.pv_vn30_volume
        
        # 2. Indicators (Chỉ lấy những cái cần)
        upper, mid, lower = self.feat.bbands(close, timeperiod=self.bb_window)
        trend = self.feat.sma(close, timeperiod=self.htf_window)
        vol_sma = self.feat.sma(vol, timeperiod=self.vol_window)
        cmf = self.feat.cmf(high, low, close, vol, timeperiod=20)
        atr = self.feat.atr(high, low, close, timeperiod=self.atr_period)
        
        # 3. Lớp lọc (Filters)
        is_uptrend = close > trend
        is_downtrend = close < trend
        is_volatile = vol > (vol_sma * 1.2) # Volume nổ mạnh
        
        # 4. Tín hiệu vào (Signal)
        long_signal = is_uptrend & (close > upper) & is_volatile #& (cmf > 0)
        short_signal = is_downtrend & (close < lower) & is_volatile #& (cmf < 0)
        
        # 5. Lớp bảo vệ (Exit)
        exit = ((close < mid) | (close < (mid - self.atr_mult * atr))) | ((close > mid) | (close > (mid + self.atr_mult * atr)))
        
        # 6. Thực thi
        self.set_positions(exit, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
        