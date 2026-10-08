"""
name:    VnLargeEarningsYieldTrend
summary: Long large caps with positive earnings yield in an 8/24 EMA uptrend.
idea:    Earnings yield (EPS over price) flags reasonably valued large caps,
         but on its own it is a static level the market has largely priced.
         Pairing a positive yield with an intact 8/24 EMA uptrend buys cheap
         quality only once the price confirms the value is being re-rated.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        eps = self.data.fun_is_eps_basis_quarterly

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        earnings_yield = eps / close
        fundamentals_known = (
            self.op.notna(eps)
            & (eps > 0)
            & self.op.notna(earnings_yield)
        )

        base_entry = fundamentals_known & (earnings_yield > 0) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (eps < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
