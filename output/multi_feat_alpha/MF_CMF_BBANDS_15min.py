class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        bbands = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        cmf = self.feat.cmf(high, low, close, volume, timeperiod=20)

        long_setup = (close < bbands['lowerband']) & (cmf > 0)
        short_setup = (close > bbands['upperband']) & (cmf < 0)
        exit_setup = self.op.crossed_above_value(close, bbands['middleband']) | self.op.crossed_below_value(close, bbands['middleband']) | self.op.crossed_above_value(cmf, 0) | self.op.crossed_below_value(cmf, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
