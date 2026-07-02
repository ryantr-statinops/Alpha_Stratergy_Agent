
"""
name:    MomVolVQFast_15min
summary: Momentum+Volume: ROC(13) + volume Q80 — 15min
thesis:  momentum | 15min
idea:    Momentum + volume quantile
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 13
    vol_window = 20

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        vol_q80 = self.feat.rolling_quantile(volume, self.vol_window, 0.80)

        long_setup = (((roc > 0) & (volume > vol_q80)) & (return_roll > 0)) & (adx > 22)
        short_setup = (((roc < 0) & (volume > vol_q80)) & (return_roll < 0)) & (adx > 22)
        exit_setup = ((self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
