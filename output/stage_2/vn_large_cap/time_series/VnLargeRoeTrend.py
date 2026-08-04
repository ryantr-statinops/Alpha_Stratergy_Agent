"""
name:    VnLargeRoeTrend
summary: Long large caps with healthy return on equity in a 12/36 EMA uptrend
         with volume participation.
idea:    Return on equity rewards large caps that deploy shareholder capital
         well. Requiring a positive quarterly ROE with a confirmed 12/36 trend
         and volume support keeps the position in profitable franchises whose
         capital efficiency the market is actively rewarding.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        equity = self.data.fun_bs_owners_equity_quarterly

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vol_base = self.feat.sma(volume, timeperiod=20)

        roe = net_profit / equity
        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(equity)
            & (equity > 0)
            & self.op.notna(roe)
        )

        base_entry = fundamentals_known & (roe > 0.02) & (ema_fast > ema_slow)
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (roe < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
