class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        adosc = self.feat.adosc(high, low, close, volume, fastperiod=3, slowperiod=10)
        trima = self.feat.trima(close, timeperiod=30)

        long_setup = (adosc > 0) & (close > trima)
        short_setup = (adosc < 0) & (close < trima)
        exit_setup = self.op.crossed_above_value(adosc, 0) | self.op.crossed_below_value(adosc, 0) | self.op.crossed(close, trima)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
