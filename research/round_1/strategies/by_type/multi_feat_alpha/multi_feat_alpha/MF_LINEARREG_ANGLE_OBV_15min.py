class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        linearreg_angle = self.feat.linearreg_angle(close, timeperiod=14)
        obv = self.feat.obv(close, volume)
        obv_ma = self.feat.rolling_mean(obv, window=20)

        long_setup = (linearreg_angle > 0) & (obv > obv_ma)
        short_setup = (linearreg_angle < 0) & (obv < obv_ma)
        exit_setup = self.op.crossed_below_value(linearreg_angle, 0) | self.op.crossed_above_value(linearreg_angle, 0) | self.op.crossed(obv, obv_ma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
