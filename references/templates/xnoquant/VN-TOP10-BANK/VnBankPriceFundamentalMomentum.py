"""
name:    VnBankPriceFundamentalMomentum
summary: Enter long when price momentum and reported earnings momentum
         both improve.
idea:    For VN Top 30 stocks, a cleaner setup is when the market is
         already trending up and the reported fundamentals are stepping
         higher at the same time. The strategy avoids custom dataframe
         access and uses only supported data, feature, and operator
         methods.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull daily-aligned price, volume, and fundamental series into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly
        operating_income = self.data.fun_is_total_operating_income_quarterly

        # Use a fast trend pair so the strategy reacts more often.
        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals usually step when new reports arrive.
        # pct_change measures those report-step changes, not continuous daily growth.
        profit_step = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_step = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)
        income_step = self.op.fillna(self.op.pct_change(operating_income, periods=1), value=0)

        # Long only when price is above trend, reporting is improving, and volume confirms.
        long_setup = (
            (close > ema_slow)
            & (ema_fast > ema_slow)
            & (profit_step > -0.03)
            & (eps_step > -0.03)
            & (income_step > -0.03)
            & (volume > volume_base)
        )

        # Exit when price trend breaks or reported fundamentals weaken clearly.
        exit_setup = (ema_fast < ema_slow) | (profit_step < -0.06) | (eps_step < -0.06)

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)