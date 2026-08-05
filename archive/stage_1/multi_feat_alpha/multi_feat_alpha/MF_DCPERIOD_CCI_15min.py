class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        dcperiod = self.feat.dcperiod(close)
        cci = self.feat.cci(high, low, close, timeperiod=14)

        long_setup = (dcperiod < 15) & (cci > 0)
        short_setup = (dcperiod < 15) & (cci < 0)
        exit_setup = self.op.crossed_above_value(cci, 0) | self.op.crossed_below_value(cci, 0) | (dcperiod > 20)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
