"""
name:    VnLargeCsCashConfirmedPatSurprise
summary: Allocate across large caps by year-over-year PAT surprise, with a
         same-window operating-cash-flow change added as a rank overlay.
         Market-neutral cross-sectional book.
idea:    A PAT surprise is more credible when operating cash flow moves in the
         same direction, which reduces one-off accounting gains. Because
         daily-aligned fundamentals are forward-filled, a daily delta is a
         report-day impulse; the surprise is therefore each metric relative to
         its own trailing average, a persistent state. Rather than cutting the
         cross-section with a hard CFO gate, the CFO deviation is combined as
         an equal-rank overlay: names whose cash confirms the earnings event
         rise, names whose cash runs against it fall, but every reported name
         stays eligible.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        pat_surprise = self.feat.safe_divide_panel(net_profit, self.feat.ema_panel(net_profit))
        cfo_surprise = self.feat.safe_divide_panel(operating_cash_flow, self.feat.ema_panel(operating_cash_flow))

        input_sum = net_profit + operating_cash_flow + total_assets
        eligible = (input_sum == input_sum) & (total_assets > 0)

        pat_rank = self.op.rank_cs_panel(pat_surprise, mask=eligible)
        cfo_rank = self.op.rank_cs_panel(cfo_surprise, mask=eligible)
        pat_score = self.op.zscore_cs_panel(pat_rank + cfo_rank, mask=eligible)

        weights = self.op.portfolio_weights_panel(pat_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)