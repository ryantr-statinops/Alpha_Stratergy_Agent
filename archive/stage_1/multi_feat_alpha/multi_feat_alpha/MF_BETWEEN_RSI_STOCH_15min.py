class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        rsi = self.feat.rsi(close, timeperiod=10)
        stoch_k, stoch_d = self.feat.stoch(high, low, close, fastk_period=10, slowk_period=3, slowd_period=3)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = self.op.between(rsi, 40, 60) & (stoch_k > stoch_d) & (close > sma10)
        short_setup = self.op.between(rsi, 40, 60) & (stoch_k < stoch_d) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed(stoch_k, stoch_d)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
