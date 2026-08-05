class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        zscore = self.feat.zscore(close, timeperiod=20)
        rolling_std = self.feat.rolling_std(close, window=10)

        long_setup = (zscore < -1.5) & (rolling_std > 0)
        short_setup = (zscore > 1.5) & (rolling_std > 0)
        exit_setup = self.op.crossed_above_value(zscore, 0) | self.op.crossed_below_value(zscore, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
