"""
name:    VnLargeCsNetPayoutPersistenceNonFin
summary: Allocate across non-financial large caps by persistent net payout
         yield: dividends plus repurchases minus share issuance, smoothed over
         time and scaled by market value. Market-neutral cross-sectional book
         restricted to the non-financial accounting population.
idea:    Dividends and buybacks are substitutes; subtracting issuance measures
         true economic distribution to shareholders. In the panel convention
         dividends and share repurchases are nonpositive outflows and issuance
         is a positive inflow. Smoothing the net payout yield with an EMA
         separates a durable payout policy from one-off special payouts, while
         market-value scaling keeps the measure comparable across price levels.
         Banks, insurers, and securities firms run a different accounting
         template where payout semantics are not comparable, so the
         cross-section is restricted to the non-financial population.
         The financial flag is economic-intensity based (insurance reserves,
         loan-granting flows, and margin deposits scaled by total assets above
         thresholds) because forward-filled annual fields are broadly populated
         and raw availability does not discriminate populations.
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

        financial = (insurance_intensity > 0.05) | (unearned_intensity > 0.05) | (loan_intensity > 0.03) | (loan_intensity < -0.03) | (margin_intensity > 0.03)
        non_financial = (financial < 1)

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (non_financial == True)

        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)

        weights = self.op.portfolio_weights_panel(payout_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
