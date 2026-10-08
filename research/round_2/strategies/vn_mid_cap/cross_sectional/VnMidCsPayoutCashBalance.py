"""
name:    VnMidCsPayoutCashBalance
summary: Buy mid caps with moderate shareholder payouts relative to cash while
         the uptrend holds. Payout-discipline vote plus trend vote. Covers
         pair G+O: cash returned to investors.
idea:    G+O pair #83 - Cash returned to investors. Moderate (dividends+repurchases)/cash
         signals a balanced capital-return policy — enough to reward holders
         without draining the cash buffer. Dividends and repurchases are
         nonpositive outflows, so the ratio uses their negated sum.
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
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15) & (dividends <= 0)
            & (repurchases <= 0) & (cash > 0)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        payout_rank = self.op.rank_cs_panel(-payout_ratio, mask=eligible)
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = payout_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
