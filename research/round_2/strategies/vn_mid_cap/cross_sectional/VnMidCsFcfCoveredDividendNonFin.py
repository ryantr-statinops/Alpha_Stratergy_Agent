"""
name:    VnMidCsFcfCoveredDividendNonFin
summary: Allocate across non-financial mid caps by dividend yield gated by
         free cash flow covering the dividend. Market-neutral cross-sectional
         book restricted to the non-financial accounting population.
idea:    A standalone dividend yield is often a value trap. A yield is durable
         only when trailing free cash flow (operating cash flow minus capex)
         covers the cash dividend. In the panel convention dividends and
         fixed-asset purchases are nonpositive outflows, so free cash flow is
         operating cash flow plus capex and the dividend is the negated payout.
         Banks, insurers, and securities firms run a different accounting
         template where FCF and dividend-cover semantics are not comparable, so
         the cross-section is restricted to the non-financial population.
         The financial flag is economic-intensity based (insurance reserves,
         loan-granting flows, and margin deposits scaled by total assets above
         thresholds) because forward-filled annual fields are broadly populated
         and raw availability does not discriminate populations.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        dividends = self.data.fun_cf_dividends_paid_annual_panel
        operating_cash_flow = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        capex = self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel
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

        dividend_paid = 0 - dividends
        free_cash_flow = operating_cash_flow + capex
        market_value = close * common_shares
        dividend_yield = self.feat.safe_divide_panel(dividend_paid, market_value)

        input_sum = dividends + operating_cash_flow + capex + common_shares + close
        eligible = (input_sum == input_sum) & (dividends < 0) & (capex <= 0) & (common_shares > 0) & (close > 0) & (market_value > 0) & (free_cash_flow > dividend_paid) & (non_financial == True)

        yield_score = self.op.zscore_cs_panel(dividend_yield, mask=eligible)

        weights = self.op.portfolio_weights_panel(yield_score, method='rank_demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
