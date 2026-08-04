"""
name:    VnLargeEarningsYieldVolume
summary: Long large caps with positive earnings yield in a 12/36 EMA uptrend
         with volume participation.
idea:    Positive earnings yield adds a value filter to the slower 12/36 trend,
         while the 20-day volume base confirms institutional participation.
         Scaling to full position only on confirmed participation avoids
         entering a cheap large cap whose rally has no real turnover behind it.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        eps = self.data.fun_is_eps_basis_quarterly

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vol_base = self.feat.sma(volume, timeperiod=20)

        earnings_yield = eps / close
        fundamentals_known = (
            self.op.notna(eps)
            & (eps > 0)
            & self.op.notna(earnings_yield)
        )

        base_entry = fundamentals_known & (earnings_yield > 0) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (eps < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
