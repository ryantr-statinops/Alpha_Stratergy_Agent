"""
name:    VnTop30CashFlowAcceleration
summary: Scale long exposure when cash flow, earnings, and price trend
         improve together.
idea:    VN Top 30 names often move better when operating cash flow turns
         up before profit growth fully shows in price. This model treats
         cash flow and earnings acceleration as the core signal, then uses
         price trend as confirmation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price, volume, and fundamental series into short names so the
        # rule logic stays readable.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        operating_income = self.data.fun_is_total_operating_income_quarterly
        eps = self.data.fun_is_eps_basis_quarterly
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        equity = self.data.fun_bs_shareholders_equity_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly

        # Use a medium trend pair so price confirms the fundamental move without
        # dominating it.
        ema_fast = self.feat.ema(close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=42)
        volume_base = self.feat.sma(volume, timeperiod=20)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change measures the step when a new reported value lands.
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        income_growth = self.op.fillna(self.op.pct_change(operating_income, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        # Capital support remains a useful background filter.
        capital_ratio = self.op.fillna(equity / total_assets, value=0)

        # Cash flow is in billions in the VN stock universe, so treat it as a
        # broad quality sign rather than a precise timing trigger.
        cash_flow_positive = operating_cash_flow > 0

        # Weak long starts when fundamentals are improving and price is above the slow trend.
        weak_long = (
            (close > ema_slow)
            & (profit_growth > -0.01)
            & (income_growth > -0.01)
            & (eps_growth > -0.01)
            & cash_flow_positive
            & (capital_ratio > 0.06)
        )

        # Strong long requires clearer acceleration plus price and volume confirmation.
        strong_long = (
            weak_long
            & (profit_growth > 0)
            & (income_growth > 0)
            & (eps_growth > 0)
            & (ema_fast > ema_slow)
            & (volume > volume_base)
            & (atr > 0)
            & (capital_ratio > 0.08)
        )

        # Exit when the business growth or trend weakens.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05) | (income_growth < -0.05)

        # Apply exits first, then half size, then full size so stronger confirmation can override.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)