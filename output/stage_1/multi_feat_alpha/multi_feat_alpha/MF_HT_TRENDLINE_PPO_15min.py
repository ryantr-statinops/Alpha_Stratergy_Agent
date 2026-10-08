class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        ht_trendline = self.feat.ht_trendline(close)
        ppo = self.feat.ppo(close, fastperiod=5, slowperiod=13, signalperiod=5, matype=0)

        long_setup = (close > ht_trendline) & (ppo > 0)
        short_setup = (close < ht_trendline) & (ppo < 0)
        exit_setup = self.op.crossed(close, ht_trendline) | self.op.crossed_above_value(ppo, 0) | self.op.crossed_below_value(ppo, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
