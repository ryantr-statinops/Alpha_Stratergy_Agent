class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        mama, fama = self.feat.mama(close, fastlimit=0.5, slowlimit=0.05)
        t3 = self.feat.t3(close, timeperiod=10)

        long_setup = (mama > fama) & (close > t3)
        short_setup = (mama < fama) & (close < t3)
        exit_setup = self.op.crossed(close, t3) | self.op.crossed(mama, fama)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
