"""
name:    VnTop30QualityLeverageSpread
summary: Scale long exposure when profitability improves faster than
         leverage pressure and the stock stays in a stable trend.
idea:    A stock with improving profit, healthy capital, and controlled
         funding pressure is more durable than one moving only on price
         momentum. This model tries to capture that lower-correlation
         quality spread.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price, volume, and fundamental series into short names so the
        # rule logic stays readable.
        close = self.data.pv_close
        volume = self.data.pv_volume

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        operating_income = self.data.fun_is_total_operating_income_quarterly
        eps = self.data.fun_is_eps_basis_quarterly
        financial_expenses = self.data.fun_is_financial_expenses_quarterly
        interest_expenses = self.data.fun_is_interest_expenses_quarterly
        equity = self.data.fun_bs_shareholders_equity_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly

        # Use a moderate trend filter so price confirms the fundamentals, but does not dominate them.
        ema_fast = self.feat.ema(close, timeperiod=18)
        ema_slow = self.feat.ema(close, timeperiod=54)
        volume_base = self.feat.sma(volume, timeperiod=20)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change here measures the step change when a new fundamental value lands,
        # not a true day-by-day operating growth rate.
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        income_growth = self.op.fillna(self.op.pct_change(operating_income, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        # Funding pressure is a different signal from raw profit growth.
        # Lower growth in interest and financial expenses is generally better.
        financial_cost_growth = self.op.fillna(self.op.pct_change(financial_expenses, periods=1), value=0)
        interest_cost_growth = self.op.fillna(self.op.pct_change(interest_expenses, periods=1), value=0)

        # Equity-to-assets is a simple capital strength proxy.
        capital_ratio = self.op.fillna(equity / total_assets, value=0)

        # Weak long starts when the business is improving and cost pressure is not accelerating.
        weak_long = (
            (close > ema_slow)
            & (profit_growth > -0.02)
            & (income_growth > -0.02)
            & (eps_growth > -0.02)
            & (financial_cost_growth < 0.05)
            & (interest_cost_growth < 0.05)
            & (capital_ratio > 0.06)
        )

        # Strong long requires clearer profit improvement and price/volume confirmation.
        strong_long = (
            weak_long
            & (profit_growth > 0)
            & (income_growth > 0)
            & (eps_growth > 0)
            & (ema_fast > ema_slow)
            & (volume > volume_base)
            & (capital_ratio > 0.08)
        )

        # Exit when trend breaks or cost pressure rises sharply.
        exit_setup = (ema_fast < ema_slow) | (financial_cost_growth > 0.15) | (interest_cost_growth > 0.15)

        # Apply exits first, then half size, then full size so stronger confirmation can override.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)