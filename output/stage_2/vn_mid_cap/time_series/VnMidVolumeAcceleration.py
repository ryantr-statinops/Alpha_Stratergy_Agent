"""
name:    VnMidVolumeAcceleration
summary: Long mid caps when volume accelerates and money flow turns positive.
idea:    Mid-cap volume is the lifeblood of a move: rising volume participation
         with a positive Money Flow Index confirms accumulating smart money.
         The volume ratio must be increasing (rising over three bars) for the
         strong state, and the position exits when flow fades or price breaks
         the slow average.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=20)
        mfi_val = self.feat.mfi(high, low, close, volume, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(vol_sma)
            & self.op.notna(mfi_val)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (volume > 0)
            & (vol_sma > 0)
        )
        vol_ratio = volume / vol_sma

        weak_long = known & (vol_ratio > 1.2) & (mfi_val > 60) & (close > ema_slow)
        strong_long = weak_long & self.op.rising(vol_ratio, 3)
        exit_setup = known & ((close < ema_slow) | (mfi_val < 50))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)