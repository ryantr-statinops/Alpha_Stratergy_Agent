"""
name:    VnMidCsCapexReinvestmentRate
summary: Buy mid caps with high capex reinvestment into the fixed-asset base
         while the uptrend holds. Pair I+N: investment intensity vs asset base.
idea:    I+N pair #97 - Capex vs fixed assets. High capex relative to the
         existing tangible fixed-asset base signals genuine re-investment and
         capacity expansion rather than asset stripping. Capex is a nonpositive
         outflow, so the ratio uses the negated outflow over tangible assets.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        fixed_assets = self.data.fun_bs_tangible_fixed_assets_quarterly_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel

        investment = 0 - capex
        reinvest_rate = self.feat.safe_divide_panel(investment, fixed_assets)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (fixed_assets > 0)
            & (capex <= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        factor_rank = self.op.rank_cs_panel(reinvest_rate, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = factor_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
