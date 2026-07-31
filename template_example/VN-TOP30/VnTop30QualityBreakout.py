"""
name:    VnTop30QualityBreakout
summary: Scale long exposure in VN Top 30 stocks when price breaks trend
         and fundamentals confirm improving quality.
idea:    Large-cap Vietnam stocks often trade better when price confirms
         the move, profits are improving, and the balance sheet is still
         healthy. Half size starts the move early, full size waits for
         stronger confirmation.
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
        eps = self.data.fun_is_eps_basis_quarterly
        operating_income = self.data.fun_is_total_operating_income_quarterly
        equity = self.data.fun_bs_shareholders_equity_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual

        # Use a moderate trend pair so the strategy reacts without becoming too noisy.
        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        volume_base = self.feat.sma(volume, timeperiod=20)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # pct_change measures the step when a new reported value lands.
        profit_growth = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_growth = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)
        income_growth = self.op.fillna(self.op.pct_change(operating_income, periods=1), value=0)

        # Equity-to-assets is a simple capital strength proxy.
        capital_ratio = self.op.fillna(equity / total_assets, value=0)

        # Operating cash flow is in billions in the VN stock universe.
        # Use it as a broad quality filter rather than a precise timing signal.
        cash_flow_positive = operating_cash_flow > 0

        # Weak long starts when the trend is positive and the fundamentals are not weakening.
        weak_long = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (profit_growth > -0.02)
            & (eps_growth > -0.02)
            & (capital_ratio > 0.06)
        )

        # Strong long requires clearer earnings improvement, price participation,
        # and healthier operating quality.
        strong_long = (
            weak_long
            & (profit_growth > 0)
            & (eps_growth > 0)
            & (income_growth > 0)
            & cash_flow_positive
            & (volume > volume_base)
            & (atr > 0)
            & (capital_ratio > 0.08)
        )

        # Exit when trend breaks or earnings weaken clearly.
        exit_setup = (ema_fast < ema_slow) | (profit_growth < -0.05) | (eps_growth < -0.05)

        # Apply exits first, then half size, then full size so stronger confirmation can override.
        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)