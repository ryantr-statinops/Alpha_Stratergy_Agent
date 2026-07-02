
"""
name:    BOQAggr_5min
summary: Quantile BO: Q85%(8) + volume — 5min
thesis:  breakout | 5min
idea:    Quantile breakout with volume
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 8
    vol_window = 14
    q_high = 0.85
    q_low = 0.15

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72
    adx_window = 7
    adx_entry_threshold = 22
    adx_exit_threshold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=7)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (((close > upper) & (volume > vol_sma)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = (((close < lower) & (volume > vol_sma)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
