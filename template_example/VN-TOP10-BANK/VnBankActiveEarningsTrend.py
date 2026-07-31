"""
name:    VnBankActiveEarningsTrend
summary: Enter long when earnings are improving and price is reclaiming a
         faster trend.
idea:    This version reacts earlier than a strict quality model. It
         allows mildly mixed fundamentals as long as the stock is still
         above the slow trend and the earnings trend is not clearly
         weakening.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price, volume, and fundamental series into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly
        operating_income = self.data.fun_is_total_operating_income_quarterly

        # Faster trend windows make the strategy react sooner.
        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change here measures the step change when a new fundamental value lands,
        # not a true day-by-day operating growth rate.
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)
        income_growth = self.op.fillna(self.op.pct_change(operating_income, periods=1), value=0)

        # Weak long allows early entry when the stock is still above trend and the
        # fundamentals are not clearly deteriorating.
        weak_long = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (profit_growth > -0.03)
            & (eps_growth > -0.03)
            & (income_growth > -0.03)
        )

        # Strong long requires positive fundamental momentum plus volume confirmation.
        strong_long = weak_long & (profit_growth > 0) & (eps_growth > 0) & (volume > volume_base)

        # Exit only when trend breaks or earnings weaken more clearly.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.06) | (eps_growth < -0.06)

        # Apply exits first, then half size, then full size so stronger confirmation can override.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)