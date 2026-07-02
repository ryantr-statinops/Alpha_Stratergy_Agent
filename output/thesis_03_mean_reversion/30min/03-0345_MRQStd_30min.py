
"""
name:    MRQStd_30min
summary: Quantile Rev: Q90%/Q10%(20) — 30min
thesis:  mean_reversion | 30min
idea:    Quantile extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 20
    q_high = 0.9
    q_low = 0.1

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12
    adx_window = 9
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=9)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)

        long_setup = ((close < lower) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((close > upper) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(close, lower) | self.op.crossed_below(close, upper)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
