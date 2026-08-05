"""
name:    VnLargeCsCfoSurprise
summary: Allocate across large caps by year-over-year operating-cash-flow
         surprise scaled by assets. Market-neutral cross-sectional book.
idea:    Cash-flow news diffuses differently from earnings news and receives
         less headline-driven attention. Because daily-aligned fundamentals are
         forward-filled, a daily delta of CFO is a report-day impulse, not a
         state. The signal is therefore CFO relative to its own trailing
         average: a persistent surprise state above the firm's cash trend.
         The eligibility uses a loose deterioration band (loss not exceeding
         2% of assets) instead of a strict positive CFO gate, so borderline but
         improving names stay in the cross-section.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        cash_trend = self.feat.ema_panel(operating_cash_flow)
        surprise_ratio = self.feat.safe_divide_panel(operating_cash_flow, cash_trend)

        input_sum = operating_cash_flow + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0) & (operating_cash_flow > -0.02 * total_assets)

        surprise_score = self.op.zscore_cs_panel(surprise_ratio, mask=eligible)

        weights = self.op.portfolio_weights_panel(surprise_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)