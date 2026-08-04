"""
name:    VnLargeValueCashTrend
summary: Long large caps that are both cheap and cash-generative in an 8/24 EMA
         uptrend with volume participation.
idea:    Value and cash quality are each weak on their own, but together they
         identify large caps that are inexpensive AND generate real cash, a
         combination institutional buyers reward. The 8/24 trend and volume
         base confirm the re-rating is actually underway, and the position
         exits if cash flow or the trend fails.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        eps = self.data.fun_is_eps_basis_quarterly
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        vol_base = self.feat.sma(volume, timeperiod=20)

        earnings_yield = eps / close
        fundamentals_known = (
            self.op.notna(eps)
            & (eps > 0)
            & self.op.notna(earnings_yield)
            & self.op.notna(operating_cash_flow)
        )

        base_entry = (
            fundamentals_known
            & (earnings_yield > 0)
            & (operating_cash_flow > 0)
            & (ema_fast > ema_slow)
        )
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (operating_cash_flow < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
