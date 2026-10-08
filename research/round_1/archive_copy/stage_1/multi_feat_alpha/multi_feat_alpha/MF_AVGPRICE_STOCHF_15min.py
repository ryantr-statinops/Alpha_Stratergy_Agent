class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_ = self.data.pv_open
        avgprice = self.feat.avgprice(open_, high, low, close)
        stochf_k, stochf_d = self.feat.stochf(high, low, close, fastk_period=10, fastd_period=3)

        long_setup = (close > avgprice) & (stochf_k > stochf_d)
        short_setup = (close < avgprice) & (stochf_k < stochf_d)
        exit_setup = self.op.crossed(close, avgprice) | self.op.crossed(stochf_k, stochf_d)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
