class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        sma_10 = self.feat.sma(close, timeperiod=10)
        basis = (close - sma_10) / sma_10
        basis_avg = self.feat.rolling_mean(basis, window=self.window)
        trend = close - sma_10
        rsi = self.feat.rsi(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (basis_avg > 0) & (trend > 0) & (adx > 22) & (rsi > 55)
        short_setup = (basis_avg < 0) & (trend < 0) & (adx > 22) & (rsi < 45)
        exit_setup = (adx < 18)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
