class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        midprice = self.feat.midprice(high, low, timeperiod=10)

        long_setup = close > midprice
        short_setup = close < midprice
        exit_setup = self.op.crossed(close, midprice)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
