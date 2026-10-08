"""
name:    VnMidCsRetentionRatio
summary: Buy mid caps with high earnings retention while the uptrend holds.
         Retention vote plus trend vote. Covers pair B+O: dividends vs net
         profit (retention ratio).
idea:    B+O pair #28 - Retention ratio. High 1 - dividends/net_profit means
         earnings are reinvested for growth rather than fully paid out; a
         firm that keeps more of its profit retains compounding power.
         Dividends are a nonpositive outflow, so payout uses the negated value.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        dividends = self.data.fun_cf_dividends_paid_quarterly_panel

        payout = 0 - dividends
        payout_ratio = self.feat.safe_divide_panel(payout, net_profit)
        retention = 1 - payout_ratio
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (net_profit > 0)
            & (dividends <= 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        retention_rank = self.op.rank_cs_panel(retention, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = retention_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
