"""
name:    VnInsuranceRSIPremiumRecovery
summary: Enter long when RSI recovers, price trend turns positive, and
         premium quality is not deteriorating.
idea:    Insurance stocks can rebound before reported fundamentals fully
         improve. This alpha uses fast RSI and trend recovery for active
         daily timing, while premium revenue and claims act as
         insurance-specific guardrails.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull daily price, volume, and insurance fundamentals into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume

        premium_revenue = self.data.fun_is_net_revenue_of_insurance_premium_quarterly
        written_premium = self.data.fun_is_gross_written_premium_quarterly
        claim_expenses = self.data.fun_is_total_insurance_claim_settlement_expenses_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        # Fast RSI and trend settings keep the strategy active on daily data.
        rsi = self.feat.rsi(close, timeperiod=7)
        ema_fast = self.feat.ema(close, timeperiod=7)
        ema_slow = self.feat.ema(close, timeperiod=21)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals step on report updates and stay flat between them.
        premium_step = self.op.fillna(self.op.pct_change(premium_revenue, periods=1), value=0)
        written_premium_step = self.op.fillna(self.op.pct_change(written_premium, periods=1), value=0)
        claim_step = self.op.fillna(self.op.pct_change(claim_expenses, periods=1), value=0)
        net_profit_step = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)

        # Long when short-term momentum recovers and insurance quality is acceptable.
        long_setup = (
            (rsi > 48)
            & (ema_fast > ema_slow)
            & (volume > volume_base)
            & (premium_step > -0.08)
            & (written_premium_step > -0.08)
            & (claim_step < 0.25)
            & (net_profit_step > -0.12)
        )

        # Exit when RSI loses recovery mode or claims/profit deteriorate sharply.
        exit_setup = (
            (rsi < 42)
            | (ema_fast < ema_slow)
            | (claim_step > 0.35)
            | (net_profit_step < -0.18)
        )

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)