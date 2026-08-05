"""
name:    VnLargeCapexVnIndexTrendGuard
summary: CapexDisciplineTrend baseline plus a regime guard that flattens all
         positions while the VN30 index trades below its own 20-day EMA. Trend
         block (12/36 EMA) unchanged so recovery re-entry stays fast.
idea:    The 2022 drawdown is a broad-market event, not a firm issue. When the
         index is below its medium-term trend, beta drags every long even with
         good fundamentals. An index-level regime guard flattens during that
         window to protect capital and un-inflate full-sample volatility, while
         the untouched firm trend block re-enters on the rebound.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=12)
        ema_slow = self.feat.ema(close, timeperiod=36)
        vn30_ema = self.feat.ema(vn30_close, timeperiod=20)

        fundamentals_known = self.op.notna(operating_cash_flow) & self.op.notna(capex)

        index_guard = vn30_close < vn30_ema

        base_entry = (
            fundamentals_known
            & (operating_cash_flow > 0)
            & (capex < operating_cash_flow)
            & (close > ema_slow)
            & (~index_guard)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (operating_cash_flow < 0) | (capex > operating_cash_flow) | (close < ema_slow) | index_guard

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)