"""
name:    VnMidCsRoERank
summary: Allocate across mid caps by return on equity relative to the
         cross-section, rewarding efficient capital allocation.
idea:    In the mid-cap space, sustainable growth tends to follow high and
         stable returns on equity. Ranking the universe by net-profit-over-
         equity and overweighting the most efficient names tilts the book
         toward quality without betting on any single stock.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        roe = self.feat.safe_divide_panel(net_profit, equity)

        eligible = self.op.notna(net_profit) & (equity > 0) & self.op.notna(close)

        signal = roe

        weights = self.op.portfolio_weights_panel(signal, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
