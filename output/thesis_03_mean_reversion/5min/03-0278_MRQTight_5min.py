
"""
name:    MRQTight_5min
summary: Quantile Rev: Q95%/Q5%(14) — 5min
thesis:  mean_reversion | 5min
idea:    Quantile extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 14
    q_high = 0.95
    q_low = 0.05

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        upper = self.feat.rolling_quantile(close, self.q_window, self.q_high)
        lower = self.feat.rolling_quantile(close, self.q_window, self.q_low)

        long_setup = (close < lower) & (return_roll > 0)
        short_setup = (close > upper) & (return_roll < 0)
        exit_setup = (self.op.crossed_above(close, lower) | self.op.crossed_below(close, upper)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
