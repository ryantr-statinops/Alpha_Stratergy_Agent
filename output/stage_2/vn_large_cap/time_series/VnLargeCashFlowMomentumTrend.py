"""
name:    VnLargeCashFlowMomentumTrend
summary: Long large caps with growing annual operating cash flow that funds
         capital expenditure, in an uptrend.
idea:    Cash flow momentum — the combination of rising operating cash flow
         with disciplined capital spending — captures improving business quality.
         Growing CFO signals strengthening operations while maintaining capex
         discipline ensures the company does not overextend. The 8/24 EMA
         trend times entry for risk management.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        cfo_growth = self.op.pct_change(operating_cash_flow, periods=1)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(capex)
            & self.op.notna(total_assets)
            & self.op.notna(cfo_growth)
            & (total_assets > 0)
        )

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (cfo_growth > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (capex > operating_cash_flow)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
