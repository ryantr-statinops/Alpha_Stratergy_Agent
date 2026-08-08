"""
name:    VnMidCsProfitCapexReturn
summary: Buy mid caps with high net profit relative to capex while the
         uptrend holds. Return-on-investment vote plus trend vote. Covers
         pair B+N: net profit vs capital expenditure.
idea:    B+N pair #27 - Investment return quality. High net_profit/capex is a
         ROIC-style proxy: profit is earned from a modest investment program
         rather than heavy spending. Capex is a nonpositive outflow, so the
         ratio uses the negated outflow.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel

        investment = 0 - capex
        return_ratio = self.feat.safe_divide_panel(net_profit, investment)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (net_profit > 0)
            & (capex < 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        return_rank = self.op.rank_cs_panel(return_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = return_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
