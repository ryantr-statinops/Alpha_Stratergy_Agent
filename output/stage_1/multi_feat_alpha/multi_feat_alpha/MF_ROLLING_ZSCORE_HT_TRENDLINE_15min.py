class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        rolling_zscore = self.feat.rolling_zscore(close, window=20)
        ht_trendline = self.feat.ht_trendline(close)

        long_setup = (rolling_zscore < -2) & (close > ht_trendline)
        short_setup = (rolling_zscore > 2) & (close < ht_trendline)
        exit_setup = self.op.crossed_above_value(rolling_zscore, -1) | self.op.crossed_below_value(rolling_zscore, 1) | self.op.crossed(close, ht_trendline)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
