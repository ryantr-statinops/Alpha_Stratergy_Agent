class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        ohlc4 = self.feat.ohlc4(open_, high, low, close)
        ppo = self.feat.ppo(close, fastperiod=12, slowperiod=26, matype=0)

        long_setup = (close > ohlc4) & (ppo > 0)
        short_setup = (close < ohlc4) & (ppo < 0)
        exit_setup = self.op.crossed(close, ohlc4) | self.op.crossed_above_value(ppo, 0) | self.op.crossed_below_value(ppo, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
