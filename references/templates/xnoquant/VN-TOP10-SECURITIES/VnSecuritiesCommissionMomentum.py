"""
name:    VnSecuritiesCommissionMomentum
summary: Scale long exposure in securities stocks when commission income,
         derivatives income, and profit all improve together.
idea:    Securities firms tend to benefit when trading activity expands
         and brokerage/derivatives income rises. Price trend confirms the
         business improvement, while weaker half-size entries catch
         earlier recoveries.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price, volume, and securities-specific fundamentals into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume

        commission_income = self.data.fun_is_fees_and_commission_income_quarterly
        brokerage_expenses = self.data.fun_is_brokerage_expenses_quarterly
        derivatives_income = self.data.fun_is_income_from_derivatives_quarterly
        fvtpl_income = self.data.fun_is_income_from_financial_assets_regconized_profit_loss_fvtpl_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly

        # Use a moderate trend pair so the strategy reacts without becoming too noisy.
        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        volume_base = self.feat.sma(volume, timeperiod=20)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change here measures the step change when a new fundamental value lands,
        # not a true day-by-day operating growth rate.
        commission_growth = self.op.fillna(self.op.pct_change(commission_income, periods=1), value=0)
        derivatives_growth = self.op.fillna(self.op.pct_change(derivatives_income, periods=1), value=0)
        fvtpl_growth = self.op.fillna(self.op.pct_change(fvtpl_income, periods=1), value=0)
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        # Brokerage expenses matter because they can eat into operating leverage.
        # Lower growth in expenses is better.
        expense_pressure = self.op.fillna(self.op.pct_change(brokerage_expenses, periods=1), value=0)

        # Weak long starts when the trend is positive and the income lines are not deteriorating.
        weak_long = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (commission_growth > -0.02)
            & (derivatives_growth > -0.02)
            & (profit_growth > -0.02)
            & (eps_growth > -0.02)
        )

        # Strong long requires clearer improvement in the core income drivers.
        strong_long = (
            weak_long
            & (commission_growth > 0)
            & (derivatives_growth > 0)
            & (fvtpl_growth > 0)
            & (profit_growth > 0)
            & (eps_growth > 0)
            & (expense_pressure < 0.10)
            & (volume > volume_base)
        )

        # Exit when the trend breaks or the income profile weakens clearly.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05) | (eps_growth < -0.05)

        # Apply exits first, then half size, then full size so stronger confirmation can override.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)