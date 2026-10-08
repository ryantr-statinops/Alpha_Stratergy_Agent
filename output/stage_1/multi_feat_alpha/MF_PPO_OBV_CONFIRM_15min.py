class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        ppo = self.feat.ppo(close, fastperiod=12, slowperiod=26, matype=0)
        obv = self.feat.obv(close, volume)
        obv_ma = self.feat.sma(obv, timeperiod=20)

        long_setup = (ppo > 0) & (obv > obv_ma)
        short_setup = (ppo < 0) & (obv < obv_ma)
        exit_setup = self.op.crossed(ppo, 0) | self.op.crossed(obv, obv_ma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
