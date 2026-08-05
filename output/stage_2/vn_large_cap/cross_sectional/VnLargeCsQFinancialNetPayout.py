"""
name:    VnLargeCsQFinancialNetPayout
summary: Allocate across financial large caps by persistent net payout yield
          built from QUARTERLY cash-flow reports: dividends plus repurchases
          minus share issuance, smoothed over time and scaled by market value.
          Market-neutral cross-sectional book restricted to the financial
          accounting population. Quarterly report frequency increases the
          number of independent observations per name and the freshness of the
          payout policy signal relative to the annual-only version.
idea:    On VN, banks and securities firms are the most persistent cash
          dividend payers, and dividend-cover semantics are internally
          comparable within the financial population. In the panel convention
          dividends and share repurchases are nonpositive outflows and issuance
          is a positive inflow. VN dividends are paid once or twice a year, so
          the quarterly gross payout is spiky; EMA smoothing separates a
          durable payout policy from one-off special payouts. The financial
          flag is economic-intensity based (insurance reserves, loan-granting
          flows, and margin deposits scaled by total assets) on the same
          quarterly frequency.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_quarterly_panel
        repurchases = self.data.fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel
        issuance = self.data.fun_cf_proceeds_from_issue_of_shares_quarterly_panel
        common_shares = self.data.fun_bs_common_shares_quarterly_panel
        close = self.data.pv_close_panel

        insurance_reserve = self.data.fun_bs_insurance_reserve_quarterly_panel
        unearned_premium = self.data.fun_bs_unearned_premium_reserve_quarterly_panel
        loans_granted = self.data.fun_cf_loans_granted_purchases_of_debt_instruments_quarterly_panel
        margin_deposits = self.data.fun_bs_margin_deposits_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel

        insurance_intensity = self.feat.safe_divide_panel(insurance_reserve, total_assets)
        unearned_intensity = self.feat.safe_divide_panel(unearned_premium, total_assets)
        loan_intensity = self.feat.safe_divide_panel(loans_granted, total_assets)
        margin_intensity = self.feat.safe_divide_panel(margin_deposits, total_assets)

        financial = (insurance_intensity > 0.05) | (unearned_intensity > 0.05) | (loan_intensity > 0.03) | (loan_intensity < -0.03) | (margin_intensity > 0.03)

        market_value = close * common_shares
        gross_payout = (0 - dividends) + (0 - repurchases) - issuance
        net_payout_yield = self.feat.safe_divide_panel(gross_payout, market_value)
        persistent_payout = self.feat.ema_panel(net_payout_yield)

        input_sum = dividends + repurchases + issuance + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (repurchases <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (financial == True)

        payout_score = self.op.zscore_cs_panel(persistent_payout, mask=eligible)

        weights = self.op.portfolio_weights_panel(payout_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
