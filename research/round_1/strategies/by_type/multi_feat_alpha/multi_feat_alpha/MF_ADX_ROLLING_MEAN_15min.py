class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rolling_mean = self.feat.rolling_mean(close, window=20)

        long_setup = (adx > 22) & (close > rolling_mean)
        short_setup = (adx > 22) & (close < rolling_mean)
        exit_setup = self.op.crossed(close, rolling_mean) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
