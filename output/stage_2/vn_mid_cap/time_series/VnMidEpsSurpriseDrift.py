"""
name:    VnMidEpsSurpriseDrift
summary: Long mid caps with positive EPS surprise drift above the trend.
idea:    PEAD is meaningful in Vietnam and stronger when institutional holding
         is low - typical of mid caps. After a positive quarterly EPS print,
         returns drift for 20-60 sessions. Requiring positive EPS, accelerating
         EPS growth and price above the slow average rides the drift. Exit on
         trend break or when the surprise decays.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        eps = self.data.fun_is_eps_basis_quarterly

        ema_slow = self.feat.ema(close, timeperiod=30)

        eps_growth = self.op.pct_change(eps, periods=1)

        fundamentals_known = (
            self.op.notna(eps)
            & (eps > 0)
            & self.op.notna(eps_growth)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = (
            fundamentals_known
            & (close > ema_slow)
            & (eps_growth > 0.05)
        )
        strong_long = weak_long & (eps_growth > 0.15)
        exit_setup = fundamentals_known & ((close < ema_slow) | (eps_growth < -0.02))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
