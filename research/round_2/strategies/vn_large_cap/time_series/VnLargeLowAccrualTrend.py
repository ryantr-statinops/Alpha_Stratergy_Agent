"""
name:    VnLargeLowAccrualTrend
summary: Long large caps whose earnings are backed by cash rather than accruals,
         with price above the 10/30 EMA trend.
idea:    Accrual quality separates profit that is actually collected as cash from
         accounting estimates. A low or negative accrual ratio (net profit minus
         operating cash flow, scaled by total assets) marks earnings quality at
         large caps, where price discovery is efficient. Only names in a 10/30
         EMA uptrend are held; exit on accrual bloat or a trend break.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=10)
        ema_slow = self.feat.ema(close, timeperiod=30)

        accrual = (net_profit - operating_cash_flow) / total_assets
        accrual_known = (
            self.op.notna(net_profit)
            & self.op.notna(operating_cash_flow)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & self.op.notna(accrual)
        )

        base_entry = accrual_known & (accrual < 0.0) & (close > ema_slow)
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = accrual_known & (accrual > 0.05) | (close < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
