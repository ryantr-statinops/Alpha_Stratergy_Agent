"""
name:    VnMidCsRetentionRatioV2
summary: Long mid-cap stocks with high earnings retention, only while the name
         trades above its EMA (long-bias trend gate). Flat when no eligible
         name is above trend. v2: trend as eligibility gate.
idea:    B+O pair #28 (v2) - High 1 - dividends/net_profit keeps earnings
         compounding in the business. v1 failed OOS under a forced short leg;
         v2 restricts to trend-up names and goes to cash once the trend breaks.
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
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (net_profit > 0)
            & (dividends <= 0) & (trend > 1.0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        retention_rank = self.op.rank_cs_panel(retention, mask=eligible)
        weights = self.op.portfolio_weights_panel(retention_rank, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)