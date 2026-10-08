"""
name:    VnLargePatSurpriseTrend
summary: Long large caps with positive year-over-year PAT growth confirmed
         by positive quarterly cash flow, in an uptrend.
idea:    Earnings surprises are more reliable when confirmed by cash flow.
         A company reporting rising net profit with positive operating cash
         flow signals that the profit improvement is backed by real cash
         collection, not accrual manipulation. This filtered PEAD captures
         delayed market reaction to quality earnings news.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit_q = self.data.fun_is_net_profit_loss_after_tax_quarterly
        operating_cash_flow_q = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        profit_growth = self.op.pct_change(net_profit_q, periods=1)
        cfo_known = self.op.notna(operating_cash_flow_q) & (operating_cash_flow_q > 0)

        fundamentals_known = (
            self.op.notna(net_profit_q)
            & self.op.notna(profit_growth)
            & (net_profit_q > 0)
        )

        base_entry = (
            fundamentals_known
            & cfo_known
            & (profit_growth > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (net_profit_q < 0)
            | (operating_cash_flow_q < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
