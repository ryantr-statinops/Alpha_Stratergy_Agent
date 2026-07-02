
"""
name:    MRCCIXSlow_60min
summary: CCI: CCI(60) — 60min
thesis:  mean_reversion | 60min
idea:    CCI extreme reversion
"""
class CustomStrategy(SimpleAlgorithm):

    cci_window = 60

    return_window = 8
    return_threshold = 0.001
    position_close_after_n_candles = 6
    adx_window = 12
    adx_entry_threshold = 16
    adx_exit_threshold = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=12)

        cci = self.feat.cci(high, low, close, timeperiod=self.cci_window)

        long_setup = ((cci < -100) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((cci > 100) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(cci, 0) | self.op.crossed_below(cci, 0)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
