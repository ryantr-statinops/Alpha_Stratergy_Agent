class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        wclprice = self.feat.wclprice(high, low, close)
        apo = self.feat.apo(close, fastperiod=5, slowperiod=13, matype=0)

        long_setup = (close > wclprice) & (apo > 0)
        short_setup = (close < wclprice) & (apo < 0)
        exit_setup = self.op.crossed(close, wclprice) | self.op.crossed_above_value(apo, 0) | self.op.crossed_below_value(apo, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
