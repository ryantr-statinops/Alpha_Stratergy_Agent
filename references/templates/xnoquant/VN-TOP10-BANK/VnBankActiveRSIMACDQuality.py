"""
name:    VnBankActiveRSIMACDQuality
summary: Enter long on faster RSI/MACD recovery when fundamentals are not
         clearly deteriorating.
idea:    For more active trading, technical timing should do most of the
         work. Fundamentals are used only as a guardrail so the strategy
         can trade recoveries without waiting for perfect report-step
         improvement.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull daily price, volume, and fundamental series into short names.
        close = self.data.pv_close
        volume = self.data.pv_volume

        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        eps = self.data.fun_is_eps_basis_quarterly

        # Faster MACD and RSI settings make the strategy react more often.
        macd, macd_signal, _hist = self.feat.macd(
            close,
            fastperiod=8,
            slowperiod=21,
            signalperiod=5,
        )
        rsi = self.feat.rsi(close, timeperiod=9)
        volume_base = self.feat.sma(volume, timeperiod=10)

        # Daily-aligned fundamentals usually stay flat between report updates.
        # These step changes act as loose quality filters, not precise timing signals.
        profit_step = self.op.fillna(self.op.pct_change(net_profit, periods=1), value=0)
        eps_step = self.op.fillna(self.op.pct_change(eps, periods=1), value=0)

        # Long when fast momentum recovers and fundamentals are not sharply worse.
        long_setup = (
            (macd > macd_signal)
            & (rsi > 48)
            & (volume > volume_base)
            & (profit_step > -0.10)
            & (eps_step > -0.10)
        )

        # Exit when momentum rolls over or fundamentals show a large negative step.
        exit_setup = (macd < macd_signal) | (rsi < 42) | (profit_step < -0.15)

        # Apply exits first so the long signal can override when conditions hold.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)