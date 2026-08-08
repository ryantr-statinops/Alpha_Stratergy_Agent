"""
name:    VnMidCsTaxCfoStable
summary: Buy mid caps with low and stable tax relative to operating cash flow
         while the uptrend holds. Tax-vs-CFO vote plus trend vote. Covers
         pair E+M: tax paid out of operating cash flow.
idea:    E+M pair #62 - Tax paid vs CFO. Low and stable tax_current/CFO means
         the tax bill is a small, predictable share of cash generation; a
         wild or heavy ratio flags distortion from non-recurring items.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel

        tax_ratio = self.feat.safe_divide_panel(tax_current, operating_cash_flow)
        tax_stability = self.feat.rolling_std_panel(tax_ratio)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current >= 0)
            & (operating_cash_flow > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        level_rank = self.op.rank_cs_panel(-tax_ratio, mask=eligible)
        stability_rank = self.op.rank_cs_panel(-tax_stability, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = level_rank + stability_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
