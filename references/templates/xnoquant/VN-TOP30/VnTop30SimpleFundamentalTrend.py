"""
name:    VnTop30SimpleFundamentalTrend
summary: Enter long when profit, EPS, and price trend all improve
         together.
idea:    For VN Top 30 names, a simple combination of earnings growth and
         a positive price trend is often enough to define a cleaner long
         setup. Half size starts the move early, full size waits for
         stronger confirmation.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull price and the main fundamental series into short names so the
        # rule logic stays readable.
        close = self.data.pv_close
        volume = self.data.pv_volume
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly

        # Use a basic trend filter and a volume baseline.
        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        volume_base = self.feat.sma(volume, timeperiod=20)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change here measures the step change when a new fundamental value lands,
        # not a true day-by-day operating growth rate.
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        # Weak long: trend is positive and fundamentals are not deteriorating.
        weak_long = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (profit_growth > -0.02)
            & (eps_growth > -0.02)
        )

        # Strong long: clearer earnings improvement and volume confirmation.
        strong_long = weak_long & (profit_growth > 0) & (eps_growth > 0) & (volume > volume_base)

        # Exit when trend breaks or earnings weaken.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05) | (eps_growth < -0.05)

        # Apply exits first, then half size, then full size.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)