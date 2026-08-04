"""
name:    VnLargeBollingerSqueezeBreakout
summary: Long large caps after a Bollinger squeeze resolves to the upside.
idea:    Large caps compress into tight ranges before major moves. When BB
         width stays at the 15th percentile of the trailing quarter and
         then price breaks above the upper band with volume, the
         volatility expansion tends to sustain for 15-30 sessions.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        upper, middle, _lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        vol_sma = self.feat.sma(volume, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(upper)
            & self.op.notna(middle)
            & self.op.notna(vol_sma)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (middle > 0)
            & (volume > 0)
            & (vol_sma > 0)
        )
        width = (upper - middle) / middle
        width_q = self.feat.rolling_quantile(width, window=63, q=0.15)
        squeeze = known & self.op.notna(width_q) & (width < width_q)

        base_long = (
            self.op.hold_for(squeeze, 3)
            & (close > upper)
            & (volume > vol_sma)
            & (close > ema_slow)
        )
        exit_setup = known & ((close < middle) | (close < ema_slow))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=1)
