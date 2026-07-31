"""
name:    VnInsurancePremiumMomentum
summary: Enter long when insurance premium revenue, underwriting profit,
         and daily price momentum improve together.
idea:    Insurance stocks can re-rate when premium growth improves and
         claim pressure stays controlled. Because the backtest is daily
         and under 3000 candles, the strategy uses active price timing
         with fundamentals as a loose quality filter.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull daily price, volume, and insurance fundamentals into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume

        premium_revenue = self.data.fun_is_net_revenue_of_insurance_premium_quarterly
        written_premium = self.data.fun_is_gross_written_premium_quarterly
        insurance_profit = self.data.fun_is_net_operating_profit_from_insurance_operation_quarterly
        claim_expenses = self.data.fun_is_claim_and_maturity_payment_expenses_quarterly
        financial_profit = self.data.fun_is_profit_from_financial_activities_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        # Fast daily trend and volume filters keep the strategy active.
        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals stay flat between report updates.
        # pct_change captures report-step changes when new values arrive.
        premium_step = self.op.fillna(self.op.pct_change(premium_revenue, periods=1), value=0)
        written_premium_step = self.op.fillna(self.op.pct_change(written_premium, periods=1), value=0)
        insurance_profit_step = self.op.fillna(self.op.pct_change(insurance_profit, periods=1), value=0)
        claim_step = self.op.fillna(self.op.pct_change(claim_expenses, periods=1), value=0)
        financial_profit_step = self.op.fillna(self.op.pct_change(financial_profit, periods=1), value=0)
        net_profit_step = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)

        # Long when price trend is active, premium growth is not deteriorating,
        # claims are not rising too sharply, and profit quality is acceptable.
        long_setup = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (volume > volume_base)
            & (premium_step > -0.05)
            & (written_premium_step > -0.05)
            & (insurance_profit_step > -0.08)
            & (financial_profit_step > -0.08)
            & (net_profit_step > -0.08)
            & (claim_step < 0.15)
        )

        # Exit when trend breaks or reported insurance profit weakens sharply.
        exit_setup = (
            (ema_fast < ema_slow)
            | (insurance_profit_step < -0.15)
            | (net_profit_step < -0.15)
            | (claim_step > 0.25)
        )

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)