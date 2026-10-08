"""
name:    VnMidCsTaxPerShare
summary: Buy mid caps with low current tax per share while the uptrend holds.
         Low-tax-burden vote plus trend vote. Covers pair E+K: tax load per
         share outstanding.
idea:    E+K pair #60 - Tax per share. Low tax_current/common_shares means the
         per-share tax burden is light, leaving more after-tax value per
         share. A clean size-free way to compare tax load across firms.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        tax_current = self.data.fun_is_business_income_tax_current_quarterly_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel

        tax_per_share = self.feat.safe_divide_panel(tax_current, common_shares)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (tax_current >= 0)
            & (common_shares > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        tax_rank = self.op.rank_cs_panel(-tax_per_share, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = tax_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
