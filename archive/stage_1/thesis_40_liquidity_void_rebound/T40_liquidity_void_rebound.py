class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        rng = high - low
        rng_z = self.feat.rolling_zscore(rng, window=self.window)
        trend_sma = self.feat.sma(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (rng_z < -0.2) & (close > trend_sma) & (adx > 18)
        short_setup = (rng_z < -0.2) & (close < trend_sma) & (adx > 18)
        exit_setup = (adx < 15) | (rng_z > 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
