class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        volume = self.data.pv_volume
        mid = (high + low) / 2
        skew = (close - mid) / (high - low + 1e-9)
        skew_avg = self.feat.rolling_mean(skew, window=self.window)
        trend_sma = self.feat.sma(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)
        vol_rank = self.feat.rolling_rank(volume, window=10)

        long_setup = (skew_avg > 0.15) & (close > trend_sma) & (adx > 18) & (rsi > 50) & (vol_rank > 0.5)
        short_setup = (skew_avg < -0.15) & (close < trend_sma) & (adx > 18) & (rsi < 50) & (vol_rank > 0.5)
        exit_setup = (adx < 16)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
