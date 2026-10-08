class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        macd, macdsignal, macdhist = self.feat.macdfix(close, signalperiod=9)

        long_setup = macd > macdsignal
        short_setup = macd < macdsignal
        exit_setup = self.op.crossed(macd, macdsignal)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
