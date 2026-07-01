
"""
name:    BOQXExtreme_60min
summary: Quantile BO: Q95%(30) + volume — 60min
thesis:  breakout | 60min
idea:    Quantile breakout with volume
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 30
    vol_window = 34
    q_high = 0.95
    q_low = 0.05

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = ((close > upper) & (volume > vol_sma)) & (return_roll > 0)
        short_setup = ((close < lower) & (volume > vol_sma)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
