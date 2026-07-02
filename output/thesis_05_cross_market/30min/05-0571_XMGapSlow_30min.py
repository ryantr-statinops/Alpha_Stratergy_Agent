
"""
name:    XMGapSlow_30min
summary: Gap: Gap(20) — 30min
thesis:  cross_market | 30min
idea:    Overnight gap capture
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 20

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12
    adx_window = 9
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        dji_close = self.data.pv_dji_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=9)

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        gap = (open_price / close - 1) * 100
        dji_direction = dji_roc > 0

        long_setup = ((dji_direction & (gap < 0.5)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = (((~dji_direction) & (gap > -0.5)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(gap, 0.5) | self.op.crossed_below(gap, -0.5)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
