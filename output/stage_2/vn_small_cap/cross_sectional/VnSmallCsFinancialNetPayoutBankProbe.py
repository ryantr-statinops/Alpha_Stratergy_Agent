"""
name:    VnSmallCsFinancialNetPayoutBankProbe
summary: Purely diagnostic probe (Gate 6 sector decomposition). Ranks the
          persistent net-payout-yield signal ONLY within the bank sub-population
          of the financial mask (loan-granting intensity dominant). If the
          parent VnSmallCsFinancialNetPayout edge is a bank concentration bet,
          this probe carries most of the parent's Sharpe; if securities carries
          it, this probe is weak. Diagnostic only, not a trading thesis.
idea:    Decomposes the financial population into mutually exclusive sub-sectors
          by economic intensity (insurance reserves / loan flows / margin
          deposits scaled by total assets). Banks are flagged first (loan
          intensity), securities second (margin deposits), insurance third.
          Population priority: insurance > bank > securities.
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
        loans_granted = self.data.fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel
        margin_deposits = self.data.fun_bs_margin_deposits_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel

        insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)
        unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)
        loan_intensity = self.feat.safe_divide_panel(loans_granted, total_assets)
        margin_intensity = self.feat.safe_divide_panel(margin_deposits, total_assets)

        insurance = (insurance_intensity > 0.05) | (unearned_intensity > 0.05)
        non_insurance = (insurance < 1)
        bank = non_insurance & ((loan_intensity > 0.03) | (loan_intensity < -0.03))

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (bank == True)

        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)

        weights = self.op.portfolio_weights_panel(payout_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
