class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        rolling_percentile_rank = self.feat.rolling_percentile_rank(close, window=20)
        beta = self.feat.beta(close, volume, timeperiod=5)

        long_setup = (rolling_percentile_rank > 0.8) & (beta > 0.5)
        short_setup = (rolling_percentile_rank < 0.2) & (beta < -0.5)
        exit_setup = self.op.crossed_below_value(rolling_percentile_rank, 0.5) | self.op.crossed_above_value(rolling_percentile_rank, 0.5) | self.op.crossed_above_value(beta, 0) | self.op.crossed_below_value(beta, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
