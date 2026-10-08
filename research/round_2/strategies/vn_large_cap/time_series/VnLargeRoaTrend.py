"""
name:    VnLargeRoaTrend
summary: Long profitable large caps with positive annual ROA in an 8/24 EMA
         uptrend.
idea:    Return on assets measures how efficiently a large cap generates profit
         from its asset base. Requiring a positive annual ROA together with an
         intact 8/24 EMA uptrend links structural profitability to price action.
         A reduced weak-regime size limits noise while full exposure is reserved
         for confirmed trend alignment.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)

        roa = net_profit / total_assets
        fundamentals_known = (
            self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(roa)
        )

        base_entry = fundamentals_known & (roa > 0) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (roa < 0) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.25)
        self.set_positions(strong_entry, position=1)
