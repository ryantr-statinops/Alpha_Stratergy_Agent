"""
name:    VnMidBetaFollower
summary: Long mid caps whose beta to VN30 confirms the broader rally.
idea:    Mid-cap followers join a VN30 rally only when their beta is elevated.
         Requiring a 60-day beta above 0.5 and price above the slow average
         enters the follower names as the wave broadens, strengthening while
         beta is still rising. Exit on trend break or when beta collapses.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ema_slow = self.feat.ema(close, timeperiod=30)
        beta_val = self.feat.beta(close, vn30_close, timeperiod=21)

        known = (
            self.op.notna(beta_val)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (vn30_close > 0)
        )

        base_long = known & (beta_val > 0.3) & (close > ema_slow)
        strong_long = base_long & self.op.rising(beta_val, 3)
        exit_setup = known & ((close < ema_slow) | (beta_val < 0.1))

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
