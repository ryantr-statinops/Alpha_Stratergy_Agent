
"""
name:    MFTVFast_30min
summary: Trend+Vol: MFTrendVol(13) — 30min
thesis:  multifactor | 30min
idea:    4-layer trend confirmation
"""
class CustomStrategy(SimpleAlgorithm):

    mid_window = 13
    vol_window = 20
    adx_window = 9

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        ema = self.feat.ema(close, timeperiod=self.mid_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.vol_window)

        trend_ok = close > ema
        volume_ok = volume > vol_sma
        vn30_confirm = vn30_roc > 0

        core_long = trend_ok & vn30_confirm
        core_short = (~trend_ok) & (~vn30_confirm)

        strong_long = core_long & (adx > 22) & (adx < 45) & volume_ok & (return_roll > 0)
        weak_long = core_long & (adx > 18) & (adx < 45) & (return_roll > 0)
        strong_short = core_short & (adx > 22) & (adx < 45) & volume_ok & (return_roll < 0)
        weak_short = core_short & (adx > 18) & (adx < 45) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(close, ema) | (adx < 15)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
