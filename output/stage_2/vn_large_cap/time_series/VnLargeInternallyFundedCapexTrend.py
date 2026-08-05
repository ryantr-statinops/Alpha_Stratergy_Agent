"""
name:    VnLargeInternallyFundedCapexTrend
summary: Long large caps where operating cash flow fully funds capital expenditure
         with no net external borrowing, in an uptrend.
idea:    A large cap that funds its investments entirely from internal cash
         generation and avoids increasing its debt load signals strong capital
         discipline. Combined with an uptrend, this filters for companies that
         grow without relying on external financing, a hallmark of quality.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual
        proceeds = self.data.fun_cf_proceeds_from_borrowings_annual
        repayments = self.data.fun_cf_repayment_of_borrowings_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(capex)
            & self.op.notna(proceeds)
            & self.op.notna(repayments)
        )

        no_net_borrowing = repayments >= proceeds

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & no_net_borrowing
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
