"""
name:    VnMidCsPayoutCashBalanceV2
summary: Long mid-cap stocks with lean payout relative to cash, only while the
         name trades above its EMA (long-bias trend gate). Flat when no
         eligible name is above trend. v2: trend as eligibility gate.
idea:    G+O pair #83 (v2) - Moderate (dividends+repurchases)/cash keeps the
         capital-return policy sustainable. v1 failed OOS under a forced short
         leg; v2 keeps only trend-up names and goes to cash when the trend
         breaks.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel
        dividends = self.data.fun_cf_dividends_paid_quarterly_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel
        cash = self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel

        payout = (0 - dividends) + (0 - repurchases)
        payout_ratio = self.feat.safe_divide_panel(payout, cash)
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (dividends <= 0)
            & (repurchases <= 0) & (cash > 0) & (trend > 1.0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        payout_rank = self.op.rank_cs_panel(-payout_ratio, mask=eligible)
        weights = self.op.portfolio_weights_panel(payout_rank, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)