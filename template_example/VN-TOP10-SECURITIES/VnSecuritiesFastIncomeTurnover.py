"""
name:    VnSecuritiesFastIncomeTurnover
summary: Enter long when securities income improves and price reclaims a
         faster trend.
idea:    Securities firms move with market activity. Faster trend windows
         and a lighter income filter let the strategy react earlier to
         changing conditions, which usually increases trade frequency.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price, volume, and securities-specific fundamentals into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume

        fee_income = self.data.fun_is_net_fee_and_commission_income_quarterly
        commission_income = self.data.fun_is_fees_and_commission_income_quarterly
        derivatives_income = self.data.fun_is_income_from_derivatives_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        # Faster trend windows make the model react sooner.
        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change here measures the step change when a new fundamental value lands,
        # not a true day-by-day operating growth rate.
        fee_growth = self.op.fillna(self.op.pct_change(fee_income, periods=1), value=0)
        commission_growth = self.op.fillna(self.op.pct_change(commission_income, periods=1), value=0)
        derivatives_growth = self.op.fillna(self.op.pct_change(derivatives_income, periods=1), value=0)
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)

        # Long when trend is positive and the main income lines are not deteriorating.
        long_setup = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (fee_growth > -0.03)
            & (commission_growth > -0.03)
            & (derivatives_growth > -0.03)
            & (profit_growth > -0.03)
            & (volume > volume_base)
        )

        # Exit quickly when the fast trend loses the slow trend or profit weakens.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.07)

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)