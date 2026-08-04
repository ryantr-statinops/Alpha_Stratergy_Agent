"""
name:    VnLargeEpsReportMomentum
summary: Hold profitable large caps in an 8/24 EMA trend and use positive EPS
         reports to increase exposure.
idea:    Positive EPS is the persistent eligibility state and the 8/24 trend
         controls holding. A positive report step plus SMA10 volume is only a
         strong-position overlay, avoiding a strategy that trades for a single
         report day and then loses its signal.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        eps = self.data.fun_is_eps_basis_quarterly

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        vol_base = self.feat.sma(volume, timeperiod=10)

        eps_growth = self.op.pct_change(eps, periods=1)
        fundamentals_known = self.op.notna(eps) & (eps > 0) & self.op.notna(eps_growth)

        base_entry = fundamentals_known & (close > ema_slow) & (ema_fast > ema_slow)
        strong_entry = base_entry & (eps_growth > 0) & (volume > vol_base)
        exit_setup = (eps < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
