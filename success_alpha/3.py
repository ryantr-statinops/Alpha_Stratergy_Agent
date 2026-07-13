class CustomStrategy(SimpleAlgorithm):
    # Parameters
    htf_window = 100
    bb_window = 20
    vol_window = 20

    def __algorithm__(self):
        # 1. Data
        close = self.data.pv_vn30_close
        high = self.data.pv_vn30_high
        low = self.data.pv_vn30_low
        vol = self.data.pv_vn30_volume

        # 2. Indicators 
        upper, mid, lower = self.feat.bbands(close, timeperiod=self.bb_window)
        trend = self.feat.sma(close, timeperiod=self.htf_window)
        vol_sma = self.feat.sma(vol, timeperiod=self.vol_window)
        
        # 3. Filters
        is_uptrend = close > trend
        is_downtrend = ~is_uptrend
        is_volatile = vol > (vol_sma * 1.2) 
        
        # 4. Signal
        long_signal = is_uptrend & (close > upper) & is_volatile
        short_signal = is_downtrend & (close < lower) & is_volatile
        
        # 5. Exit
        exit = (close < mid) | (close > mid)
        
        # 6. Position setting
        self.set_positions(exit, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
        