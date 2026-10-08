class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        rolling_covariance = self.feat.rolling_covariance(close, volume, window=20)
        cmo = self.feat.cmo(close, timeperiod=14)

        long_setup = (rolling_covariance > 0) & (cmo > 0)
        short_setup = (rolling_covariance < 0) & (cmo < 0)
        exit_setup = self.op.crossed_above_value(rolling_covariance, 0) | self.op.crossed_below_value(rolling_covariance, 0) | self.op.crossed_above_value(cmo, 0) | self.op.crossed_below_value(cmo, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
