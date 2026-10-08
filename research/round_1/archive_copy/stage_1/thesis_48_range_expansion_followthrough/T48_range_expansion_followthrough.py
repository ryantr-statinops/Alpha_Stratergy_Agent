class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        volume = self.data.pv_volume
        range_ = high - low
        range_avg = self.feat.rolling_mean(range_, window=self.window)
        breakout = range_ > range_avg
        trend = close - self.feat.rolling_mean(close, window=self.window)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)

        long_setup = breakout & (trend > 0) & (adx > 18) & (rsi > 55) & (volume > vol_sma)
        short_setup = breakout & (trend < 0) & (adx > 18) & (rsi < 45) & (volume > vol_sma)
        exit_setup = (adx < 16)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
