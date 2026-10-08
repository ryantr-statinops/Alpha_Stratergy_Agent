class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        ret = self.op.pct_change(close, periods=1)
        downside = ret * (ret < 0)
        tail_risk = self.feat.rolling_mean(self.op.abs(downside), window=self.window)
        mom = close - self.feat.rolling_mean(close, window=self.window)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)
        trend_sma = self.feat.sma(close, timeperiod=10)

        long_setup = (mom > 0) & (tail_risk < self.feat.rolling_mean(tail_risk, window=self.window)) & (adx > 20) & (rsi > 50) & (close > trend_sma)
        short_setup = (mom < 0) & (tail_risk < self.feat.rolling_mean(tail_risk, window=self.window)) & (adx > 20) & (rsi < 50) & (close < trend_sma)
        exit_setup = (adx < 16)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
