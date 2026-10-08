class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        body = self.op.abs(close - open_price)
        range_ = high - low
        impact = body / (range_ + 1e-9)
        avg_impact = self.feat.rolling_mean(impact, window=self.window)
        vol_sma = self.feat.sma(volume, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        return_1 = self.op.pct_change(close, periods=1)
        trend_sma = self.feat.sma(close, timeperiod=10)

        long_setup = (close > open_price) & (impact > avg_impact) & (volume > vol_sma) & (adx > 18) & (return_1 > 0) & (close > trend_sma)
        short_setup = (close < open_price) & (impact > avg_impact) & (volume > vol_sma) & (adx > 18) & (return_1 < 0) & (close < trend_sma)
        exit_setup = (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
