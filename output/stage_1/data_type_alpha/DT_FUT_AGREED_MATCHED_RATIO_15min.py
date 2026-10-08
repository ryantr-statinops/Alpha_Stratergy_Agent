class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        agreed_vol = self.data.fut_agreed_volume_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        ratio = self.feat.div(agreed_vol, matched_vol)
        ratio_sma = self.feat.sma(ratio, timeperiod=10)
        roc = self.feat.roc(close, timeperiod=5)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        return_1 = self.op.pct_change(close, periods=1)
        return_roll = self.feat.rolling_mean(return_1, window=10)

        long_setup = (ratio > ratio_sma) & (roc > 0) & (adx > 20) & (return_roll > 0)
        short_setup = (ratio > ratio_sma) & (roc < 0) & (adx > 20) & (return_roll < 0)
        exit_setup = (ratio < ratio_sma) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
