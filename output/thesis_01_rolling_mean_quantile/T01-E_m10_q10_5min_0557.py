"""
name:    T01-E_m10_q10
summary: Mean + Quantile Fusion
idea:    Combine mean and quantile filters: require price above both upper quantile and mean for long, below both for short.
"""
class CustomStrategy(SimpleAlgorithm):
    mean_window = 10
    q_window = 10
    thesis_group = "01"

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        upper = self.feat.rolling_quantile(close, window=self.q_window, q=0.8)
        lower = self.feat.rolling_quantile(close, window=self.q_window, q=0.2)

        long_setup = (close > upper) & (close > mean)
        short_setup = (close < lower) & (close < mean)
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

