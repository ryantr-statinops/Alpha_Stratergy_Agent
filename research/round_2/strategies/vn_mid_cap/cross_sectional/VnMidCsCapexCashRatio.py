"""
name:    VnMidCsCapexCashRatio
summary: Buy mid caps with low capex relative to cash while the uptrend holds.
         Investment-discipline vote plus trend vote. Covers pair G+N: cash
         used in investments.
idea:    G+N pair #82 - Cash used in investments. Low capex/cash means the
         investment program does not burn through the cash buffer; the firm
         can reinvest without eroding liquidity. Capex is a nonpositive
         outflow, so the ratio uses the negated outflow.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel

        investment = 0 - capex
        burn_ratio = self.feat.safe_divide_panel(investment, cash)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (capex <= 0)
            & (cash > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        burn_rank = self.op.rank_cs_panel(-burn_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = burn_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
