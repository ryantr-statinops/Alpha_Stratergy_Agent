"""
name:    VnLargeCsQRoeQuality
summary: Allocate across profitable large caps by smoothed QUARTERLY return on
          equity: net profit after tax divided by owners' equity, EMA-smoothed.
          Broad market-neutral cross-sectional book restricted to positive
          profitability and positive equity. Quarterly frequency refreshes the
          profitability signal four times a year instead of once.
idea:    Persistent high ROE marks companies that create value on shareholder
          capital; smoothing removes quarterly noise while keeping the fresher
          quarterly report cadence. Banks are structurally high-leverage, so
          ROE is comparable only within the financial population — the signal
          is kept broad here as the counterpart to the ROA quality test, with
          the accounting-heterogeneity caveat documented in the framework.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        owners_equity = self.data.fun_bs_owners_equity_quarterly_panel
        close = self.data.pv_close_panel

        roe = self.feat.safe_divide_panel(profit, owners_equity)
        quality = self.feat.ema_panel(roe)

        input_sum = profit + owners_equity + close
        eligible = (input_sum == input_sum) & (close > 0) & (owners_equity > 0) & (profit > 0)

        quality_score = self.op.zscore_cs_panel(quality, mask=eligible)

        weights = self.op.portfolio_weights_panel(quality_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
