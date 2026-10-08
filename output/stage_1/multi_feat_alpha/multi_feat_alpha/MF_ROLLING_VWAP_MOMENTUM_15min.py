class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        rolling_vwap = self.feat.rolling_vwap(high, low, close, volume, window=20)
        momentum = self.feat.momentum(close, timeperiod=10)

        long_setup = (close > rolling_vwap) & (momentum > 0)
        short_setup = (close < rolling_vwap) & (momentum < 0)
        exit_setup = self.op.crossed(close, rolling_vwap) | self.op.crossed_above_value(momentum, 0) | self.op.crossed_below_value(momentum, 0)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
