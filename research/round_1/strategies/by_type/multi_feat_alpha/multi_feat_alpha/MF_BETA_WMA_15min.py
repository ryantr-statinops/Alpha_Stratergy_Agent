class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        beta = self.feat.beta(close, volume, timeperiod=5)
        wma = self.feat.wma(close, timeperiod=10)

        long_setup = (beta > 0.5) & (close > wma)
        short_setup = (beta < -0.5) & (close < wma)
        exit_setup = self.op.crossed_above_value(beta, 0) | self.op.crossed_below_value(beta, 0) | self.op.crossed(close, wma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
