
"""
name:    BOQXExtreme_30min
summary: Quantile BO: Q95%(20) + volume — 30min
thesis:  breakout | 30min
idea:    Quantile breakout with volume
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 20
    vol_window = 26
    q_high = 0.95
    q_low = 0.05

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (((close > upper) & (volume > vol_sma)) & (return_roll > 0)) & (adx > 22)
        short_setup = (((close < lower) & (volume > vol_sma)) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
