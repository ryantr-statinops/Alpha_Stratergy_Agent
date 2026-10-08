class CustomStrategy(SimpleAlgorithm):
    window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        vol_rank = self.feat.rolling_rank(volume, window=self.window)
        price_trend = close - self.feat.rolling_mean(close, window=self.window)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_setup = (vol_rank > 0.7) & (price_trend > 0) & (adx > 20) & (rsi > 50)
        short_setup = (vol_rank > 0.7) & (price_trend < 0) & (adx > 20) & (rsi < 50)
        exit_setup = (adx < 18) | (vol_rank < 0.5) | self.op.abs(price_trend) < 0

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
