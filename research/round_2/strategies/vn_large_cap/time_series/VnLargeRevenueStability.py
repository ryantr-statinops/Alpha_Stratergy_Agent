"""
name:    VnLargeRevenueStability
summary: Long large caps whose operating cash flow and profit stay stable
         while price holds above its long-term trend.
idea:    Large caps are priced for consistency. The combination of a positive
         annual operating cash flow, positive quarterly net profit and price
         above the 60-day average isolates names whose business model delivers
         recurring revenue without speculative price extension.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        total_assets = self.data.fun_bs_total_assets_quarterly

        sma60 = self.feat.sma(close, timeperiod=60)
        ema_slow = self.feat.ema(close, timeperiod=54)

        profit_margin = net_profit / total_assets
        profit_growth = self.op.pct_change(net_profit, periods=1)

        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(profit_margin)
            & self.op.notna(profit_growth)
        )

        weak_long = (
            fundamentals_known
            & (close > sma60)
            & (operating_cash_flow > 0)
            & (profit_margin > 0.005)
        )

        strong_long = (
            weak_long
            & (close > ema_slow)
            & (profit_growth > -0.02)
            & (profit_margin > 0.01)
        )

        exit_setup = (close < sma60) | (operating_cash_flow < 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
