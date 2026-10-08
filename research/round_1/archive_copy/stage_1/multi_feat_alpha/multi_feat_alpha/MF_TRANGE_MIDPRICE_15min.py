class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        trange = self.feat.trange(high, low, close)
        midprice = self.feat.midprice(high, low, timeperiod=14)
        trange_ma = self.feat.rolling_mean(trange, window=20)

        long_setup = (trange > trange_ma) & (close > midprice)
        short_setup = (trange > trange_ma) & (close < midprice)
        exit_setup = self.op.crossed(close, midprice) | (trange < trange_ma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
