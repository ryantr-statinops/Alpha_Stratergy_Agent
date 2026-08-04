"""
name:    VnLargeStableCashQuality
summary: Long large caps with stable positive cash flow and quarterly profit in
         a 12/36 EMA uptrend with volume participation.
idea:    Combining positive annual operating cash flow with positive quarterly
         net profit screens out firms whose cash generation is deteriorating
         even when headline profit looks fine. The 12/36 trend and volume base
         then confirm that the market is rewarding the stable quality.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vol_base = self.feat.sma(volume, timeperiod=20)

        fundamentals_known = (
            self.op.notna(operating_cash_flow)
            & self.op.notna(net_profit)
        )

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (net_profit > 0)
            & (ema_fast > ema_slow)
        )
        strong_entry = base_entry & (volume > vol_base)
        exit_setup = (net_profit < 0) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
