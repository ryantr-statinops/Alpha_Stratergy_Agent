"""
name:    VnSmallCsFinancialNetPayoutInsuranceProbe
summary: Purely diagnostic probe (Gate 6 sector decomposition). Ranks the
          persistent net-payout-yield signal ONLY within the insurance
          sub-population of the financial mask (insurance reserves + unearned
          premium intensity dominant). Expected to be a very thin cross-section
          on VN small cap; a near-empty population yields ~zero metrics and is
          itself evidence that the parent's financial edge is not insurance-led.
          Diagnostic only, not a trading thesis.
idea:    Decomposes the financial population into mutually exclusive sub-sectors
          by economic intensity. Insurance is the highest-priority bucket:
          insurance = (reserve / TA > 0.05) | (unearned premium / TA > 0.05).
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel
        common_shares = self.data.fun_bs_common_shares_annual_panel
        close = self.data.pv_close_panel

        insurance_reserve = self.data.fun_bs_insurance_reserve_annual_panel
        unearned_premium = self.data.fun_bs_unearned_premium_reserve_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)
        unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)

        insurance = (insurance_intensity > 0.05) | (unearned_intensity > 0.05)

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (insurance == True)

        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)

        weights = self.op.portfolio_weights_panel(payout_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
