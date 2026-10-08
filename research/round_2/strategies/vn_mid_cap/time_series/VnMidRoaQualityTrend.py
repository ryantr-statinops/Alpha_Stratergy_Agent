"""
name:    VnMidRoaQualityTrend
summary: Long mid caps combining ROA quality with a confirmed uptrend.
idea:    ROA measures how productively a mid cap uses its whole asset base,
         complementing the ROE-based VnMidTrendQuality. Requiring positive ROA
         above 1%, positive profit and price above the 36-day average enters
         quality names in a trend. Exit on trend break or when ROA turns
         negative.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)

        roa = net_profit / total_assets

        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(roa)
            & self.op.notna(ema_slow)
            & (close > 0)
        )

        weak_long = (
            fundamentals_known
            & (net_profit > 0)
            & (roa > 0.01)
            & (close > ema_slow)
        )
        strong_long = weak_long & (ema_fast > ema_slow)
        exit_setup = fundamentals_known & ((close < ema_slow) | (roa < 0))

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
