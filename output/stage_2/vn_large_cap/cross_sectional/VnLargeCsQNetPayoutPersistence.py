"""
name:    VnLargeCsQNetPayoutPersistence
summary: Allocate across large caps by persistent net payout yield built from
          QUARTERLY cash-flow reports: dividends plus repurchases minus share
          issuance, smoothed over time and scaled by market value. Broad
          market-neutral cross-sectional book (no financial restriction).
idea:    Dividends and buybacks are substitutes; subtracting issuance measures
          true economic distribution to shareholders. In the panel convention
          dividends and share repurchases are nonpositive outflows and issuance
          is a positive inflow. VN dividends are paid once or twice a year, so
          the quarterly gross payout is spiky; EMA smoothing separates a
          durable payout policy from one-off special payouts. Quarterly report
          frequency gives more independent observations per name than the
          annual version.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_quarterly_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_quarterly_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel
        close = self.data.pv_close_panel

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0)

        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)

        weights = self.op.portfolio_weights_panel(payout_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
