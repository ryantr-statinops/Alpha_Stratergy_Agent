"""
name:    VnInsurancePremiumQualityHold
summary: Hold insurance stocks only when premium revenue, net profit, and
         investment income support a slower trend.
idea:    To reduce fee drag, the alpha should avoid frequent reversals.
         This model waits for durable insurance revenue and profit
         quality, then exits only when trend or fundamentals weaken
         clearly.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull daily price and insurance fundamentals into short names.
        close = self.data.pv_close

        premium_revenue = self.data.fun_is_net_revenue_of_insurance_premium_quarterly
        investment_profit = self.data.fun_is_profit_from_financial_activities_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        claims = self.data.fun_is_total_insurance_claim_settlement_expenses_quarterly

        # Slower trend windows reduce turnover and fee drag.
        ema_fast = self.feat.ema(close, timeperiod=30)
        ema_slow = self.feat.ema(close, timeperiod=90)

        # Daily-aligned fundamentals step when reports update; they are not smooth daily signals.
        premium_step = self.op.fillna(self.op.pct_change(premium_revenue, periods=1), value=0)
        investment_step = self.op.fillna(self.op.pct_change(investment_profit, periods=1), value=0)
        profit_step = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        claims_step = self.op.fillna(self.op.pct_change(claims, periods=1), value=0)

        # Long only when the slow trend is intact and the main insurance quality
        # lines are not deteriorating.
        long_setup = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (premium_step > -0.05)
            & (investment_step > -0.05)
            & (profit_step > -0.05)
            & (claims_step < 0.15)
        )

        # Exit only on a clearer trend break or obvious deterioration.
        exit_setup = (
            (ema_fast < ema_slow)
            | (profit_step < -0.15)
            | (premium_step < -0.15)
            | (claims_step > 0.30)
        )

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)