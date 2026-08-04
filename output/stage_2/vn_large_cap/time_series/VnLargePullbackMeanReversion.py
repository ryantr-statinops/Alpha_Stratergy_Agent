"""
name:    VnLargePullbackMeanReversion
summary: Long large caps pulling back >8% from 20-day high inside an uptrend.
idea:    Large caps exhibit mean reversion after sharp pullbacks when the
         broader trend is intact. Buying an 8%+ drawdown from the 20-day
         high with RSI confirming oversold and price above the slow average
         captures the bounce back toward the trend.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        ema_slow = self.feat.ema(close, timeperiod=30)
        roll_high = self.feat.rolling_max(close, window=20)
        rsi_val = self.feat.rsi(close, timeperiod=9)
        ret3 = self.op.fillna(self.op.pct_change(close, periods=3), 0)

        known = (
            self.op.notna(ema_slow)
            & self.op.notna(roll_high)
            & self.op.notna(rsi_val)
            & (close > 0)
            & (roll_high > 0)
        )

        drawdown = close / roll_high
        base_long = known & (close > ema_slow) & (drawdown < 0.92) & (rsi_val < 45)
        strong_long = base_long & (ret3 > 0)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
