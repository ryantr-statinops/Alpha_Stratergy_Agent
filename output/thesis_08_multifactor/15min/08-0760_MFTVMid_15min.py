
"""
name:    MFTVMid_15min
summary: Trend+Vol: MFTrendVol(26) — 15min
thesis:  multifactor | 15min
idea:    4-layer trend confirmation
"""
class CustomStrategy(SimpleAlgorithm):

    mid_window = 26
    vol_window = 20
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        ema = self.feat.ema(close, timeperiod=self.mid_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.vol_window)

        trend_ok = close > ema
        strength_ok = (adx > 20) & (adx < 45)
        volume_ok = volume > vol_sma
        vn30_confirm = vn30_roc > 0

        long_setup = trend_ok & strength_ok & volume_ok & vn30_confirm
        short_setup = (~trend_ok) & strength_ok & volume_ok & (~vn30_confirm)
        exit_setup = self.op.crossed_below(close, ema) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
