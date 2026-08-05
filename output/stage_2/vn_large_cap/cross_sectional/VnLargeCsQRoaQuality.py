"""
name:    VnLargeCsQRoaQuality
summary: Allocate across profitable large caps by smoothed QUARTERLY return on
          assets: net profit after tax divided by total assets, EMA-smoothed.
          Broad market-neutral cross-sectional book restricted to positive
          profitability. Quarterly frequency refreshes the profitability
          signal four times a year instead of once.
idea:    Persistent high ROA marks companies that generate earnings from the
          asset base without recurring write-offs; smoothing removes quarterly
          noise while keeping the fresher quarterly report cadence. Restricting
          to positive profit enforces the quality gate so the cross-section
          ranks among genuinely profitable names.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        close = self.data.pv_close_panel

        roa = self.feat.safe_divide_panel(profit, total_assets)
        quality = self.feat.ema_panel(roa)

        input_sum = profit + total_assets + close
        eligible = (input_sum == input_sum) & (close > 0) & (total_assets > 0) & (profit > 0)

        quality_score = self.op.zscore_cs_panel(quality, mask=eligible)

        weights = self.op.portfolio_weights_panel(quality_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
