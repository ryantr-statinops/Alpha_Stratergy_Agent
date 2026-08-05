"""
name:    VnLargeCashConversionInflectionTrend
summary: Long large caps where the cash-conversion spread (CFO minus PAT,
         scaled by assets) is positive and improving, in an uptrend.
idea:    The gap between operating cash flow and reported net profit reveals
         earnings quality. A positive and widening cash-conversion spread
         signals that profits are increasingly backed by cash collection —
         a quality inflection, not just earnings growth. This second-order
         accounting signal captures changes in earnings authenticity that
         standard value and growth factors miss.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & (net_profit > 0)
            & (operating_cash_flow > 0)
        )

        cash_spread = (operating_cash_flow - net_profit) / total_assets
        spread_change = self.op.pct_change(cash_spread, periods=1)

        base_entry = (
            fundamentals_known
            & self.op.notna(spread_change)
            & (cash_spread > 0)
            & (spread_change > 0)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (operating_cash_flow < 0)
            | (net_profit < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)