"""
name:    VnSmallCsNetPayoutMomentum
summary: Allocate across small caps by persistent net payout yield combined
         with squared price momentum: net payout yield times (close/ema)^2.
         Momentum is the core; net payout is the fundamental discipline layer.
         Market-neutral magnitude-weighted book.
idea:    The passing value-momentum composite wins because a squared momentum
         core captures the stable VN trend factor while a fundamental layer
         keeps the book disciplined. This file tests whether the same structure
         rescues our pure fundamental net-payout alpha: persistent net payout
         yield (dividends plus repurchases minus issuance, EMA-smoothed, scaled
         by market value) replaces earnings yield, and demeaning L1 weighting
         replaces rank weighting so the strongest composite names drive the
         book. Mixed frequency: annual payout fundamentals with daily momentum.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)
        trend_ratio = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0)

        signal = persistent_payout * trend_ratio * trend_ratio

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
