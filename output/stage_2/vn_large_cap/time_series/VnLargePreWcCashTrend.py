"""
name:    VnLargePreWcCashTrend
summary: Long large caps where operating cash flow before working capital changes
         exceeds net profit, indicating strong underlying earning power, in an
         uptrend.
idea:    Pre-working-capital cash flow strips out the noise of receivables,
         inventory and payables timing. When this measure exceeds reported
         net profit, the company's core operating earning power is stronger
         than the bottom line suggests. This residual quality signal is
         orthogonal to standard value and earnings factors, providing
         diversification. The 14/42 EMA trend confirms the price regime.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        pre_wc_cash = self.data.fun_cf_operating_profit_loss_before_changes_in_wc_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual
        total_assets = self.data.fun_bs_total_assets_annual

        ema_fast = self.feat.ema(close, timeperiod=14)
        ema_slow = self.feat.ema(close, timeperiod=42)

        fundamentals_known = (
            self.op.notna(pre_wc_cash)
            & self.op.notna(net_profit)
            & self.op.notna(total_assets)
            & (total_assets > 0)
            & (net_profit > 0)
        )

        wc_strength = pre_wc_cash / total_assets
        earnings_level = net_profit / total_assets

        base_entry = (
            fundamentals_known
            & (pre_wc_cash > 0)
            & (wc_strength > earnings_level)
            & (close > ema_slow)
        )
        strong_entry = base_entry & (ema_fast > ema_slow)
        exit_setup = (
            (pre_wc_cash < 0)
            | (net_profit < 0)
            | (close < ema_slow)
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
