class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        vn30_close = self.data.pv_vn30_close
        correl = self.feat.correl(close, vn30_close, timeperiod=30)
        roc = self.feat.roc(close, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=14)
        return_1 = self.op.pct_change(close, periods=1)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        long_setup = (correl > 0.5) & (roc > 0) & (adx > 22) & (return_roll > 0)
        short_setup = (correl > 0.5) & (roc < 0) & (adx > 22) & (return_roll < 0)
        exit_setup = (correl < 0.3) | self.op.crossed(roc, 0) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
