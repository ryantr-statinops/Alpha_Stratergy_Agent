"""
name:    VnMidCsTaxCashBuffer
summary: Buy mid caps with low current tax relative to cash while the uptrend
         holds. Tax-burden-vs-cash vote plus trend vote. Covers pair E+G:
         ability to pay tax from the cash buffer.
idea:    E+G pair #56 - Tax paid vs cash buffer. Low tax_current/cash means
         the tax bill is comfortably covered by the cash buffer, leaving
         headroom for operations and growth. Precedent: VnSmallCsTaxStability.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel

        tax_ratio = self.feat.safe_divide_panel(tax_current, cash)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current >= 0)
            & (cash > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        buffer_rank = self.op.rank_cs_panel(-tax_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = buffer_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
