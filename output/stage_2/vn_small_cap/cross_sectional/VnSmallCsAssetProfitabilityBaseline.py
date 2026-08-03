"""
name:    VnSmallCsAssetProfitabilityBaseline
summary: Market-neutral small-cap allocation ranked by quarterly asset profitability.
idea:    Profitable small companies with stronger earnings relative to their asset
         base are underpriced versus weaker peers because fundamental quality is
         incorporated more slowly in the less-followed small-cap segment.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # STEP 1 — Point-in-time panel data
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        # STEP 2 — Scale-adjusted persistent profitability
        asset_profitability = self.feat.safe_divide_panel(net_profit, total_assets)

        # STEP 3 — Economic validity and availability mask
        eligible = (
            (close > 0)
            & (volume > 0)
            & (net_profit > 0)
            & (total_assets > 0)
        )

        # STEP 4 — Market-neutral cross-sectional portfolio
        weights = self.op.portfolio_weights_panel(
            asset_profitability,
            method="rank_demean_l1",
            mask=eligible,
        )
        self.set_portfolio_positions(weights)
