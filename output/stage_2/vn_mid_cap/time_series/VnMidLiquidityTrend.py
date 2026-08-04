"""
name:    VnMidLiquidityTrend
summary: Long mid-cap uptrends with traded value above a liquidity floor.
idea:    Illiquid mid caps spike on small orders and cannot be exited at the
         marked price. Requiring positive trading activity and traded value
         above half of its 20-day average keeps the position in names that can
         actually be traded, scaling up when liquidity is confirmed above the
         average. Exit on trend break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        traded_value = close * volume
        tv_sma = self.feat.sma(traded_value, timeperiod=20)
        ema_slow = self.feat.ema(close, timeperiod=30)

        known = (
            self.op.notna(traded_value)
            & self.op.notna(tv_sma)
            & self.op.notna(ema_slow)
            & (close > 0)
            & (volume > 0)
            & (tv_sma > 0)
        )

        base_long = known & (traded_value > tv_sma * 0.5) & (close > ema_slow)
        strong_long = base_long & (traded_value > tv_sma)
        exit_setup = known & (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_long, position=0.5)
        self.set_positions(strong_long, position=1)
