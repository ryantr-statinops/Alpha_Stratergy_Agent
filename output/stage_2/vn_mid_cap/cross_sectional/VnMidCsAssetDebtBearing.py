"""
name:    VnMidCsAssetDebtBearing
summary: Buy mid caps with low long-term debt relative to fixed assets while
         the uptrend holds. Low-debt-funding vote plus trend vote. Covers pair
         I+O: asset acquisition funded by debt.
idea:    I+O pair #98 - Asset acquisition via debt. Low
         long_term_liabilities/tangible_fixed_assets means the asset base is
         funded from equity and retained earnings, not borrowed; a light
         debt load on hard assets is safer and leaves capacity for growth.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        long_term_liabilities = self.data.fun_bs_long_term_liabilities_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel

        debt_ratio = self.feat.safe_divide_panel(long_term_liabilities, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (long_term_liabilities >= 0)
            & (fixed_assets > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        debt_rank = self.op.rank_cs_panel(-debt_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = debt_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
