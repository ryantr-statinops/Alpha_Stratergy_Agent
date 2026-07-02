"""
name:    T06-C_m13_v10_r8
summary: Multi-Layer Confirmation
idea:    Stack trend, momentum, volume, volatility, and cross-market filters with graduated position sizing.
"""
class CustomStrategy(SimpleAlgorithm):
    mid_window = 13
    vol_window = 10


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        ema = self.feat.ema(close, timeperiod=self.mid_window)
        trend_ok = close > ema

        roc_val = self.feat.roc(close, timeperiod=8)
        momentum_ok = roc_val > 0

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        volume_ok = volume > vol_sma

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        atr_trend = atr_val > self.feat.sma(atr_val, timeperiod=self.vol_window)

        vn30_roc = self.feat.roc(vn30_close, timeperiod=8)
        vn30_ok = vn30_roc > 0

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        return_roll = self.feat.returns(close, periods=14)

        core_long = trend_ok & momentum_ok & vn30_ok
        core_short = (~trend_ok) & (~momentum_ok) & (~vn30_ok)

        strong_long = core_long & volume_ok & atr_trend & (adx_val > 16) & (return_roll > 0)
        weak_long = core_long & (adx_val > 14) & (return_roll > 0)
        strong_short = core_short & volume_ok & atr_trend & (adx_val > 16) & (return_roll < 0)
        weak_short = core_short & (adx_val > 14) & (return_roll < 0)

        exit_setup = self.op.crossed_below(close, ema) | (adx_val < 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)

