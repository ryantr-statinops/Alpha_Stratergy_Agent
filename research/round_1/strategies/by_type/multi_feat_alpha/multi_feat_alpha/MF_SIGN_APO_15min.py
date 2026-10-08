class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        apo = self.feat.apo(close, fastperiod=5, slowperiod=13, matype=0)
        midpoint = self.feat.midpoint(close, timeperiod=14)
        sma10 = self.feat.sma(close, timeperiod=10)
        sign_apo = self.op.sign(apo)

        long_setup = (sign_apo > 0) & (close > midpoint) & (close > sma10)
        short_setup = (sign_apo < 0) & (close < midpoint) & (close < sma10)
        exit_setup = self.op.crossed(close, midpoint)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
