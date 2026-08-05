class CustomStrategy(SimpleAlgorithm):
    window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        ret = self.op.pct_change(close, periods=1)
        abs_ret = self.op.abs(ret)
        avg_abs = self.feat.rolling_mean(abs_ret, window=self.window)
        trend = self.feat.sma(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)

        long_setup = (close > trend) & (adx > 18) & (rsi > 55)
        short_setup = (close < trend) & (adx > 18) & (rsi < 45)
        exit_setup = (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
