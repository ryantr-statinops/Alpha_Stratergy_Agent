class CustomStrategy(SimpleAlgorithm):
    threshold = 0.005

    def __algorithm__(self):
        open_price = self.data.pv_open
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        prev_close = self.feat.rolling_mean(close, window=2)
        gap = (open_price - prev_close) / prev_close
        adx = self.feat.adx(high, low, close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)

        long_setup = (gap < -self.threshold) & (close > open_price) & (adx > 18) & (volume > vol_sma) & (rsi < 60)
        short_setup = (gap > self.threshold) & (close < open_price) & (adx > 18) & (volume > vol_sma) & (rsi > 40)
        exit_setup = (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
