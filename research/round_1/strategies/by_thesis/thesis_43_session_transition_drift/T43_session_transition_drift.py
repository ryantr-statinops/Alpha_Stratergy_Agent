class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-02:30", "06:00-06:30"]
    position_close_ranges = ["02:20-02:30", "06:20-06:30"]
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        sma_10 = self.feat.sma(close, timeperiod=10)
        ret = self.op.pct_change(close, periods=1)
        mom = self.feat.rolling_sum(ret, window=5)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=10)

        long_setup = (close > sma_10) & (mom > 0) & (adx > 18) & (rsi > 50)
        short_setup = (close < sma_10) & (mom < 0) & (adx > 18) & (rsi < 50)
        exit_setup = (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
