# Data Syntax Reference (Round 2)

Use this file as the canonical catalog for `self.data.*` on the Round 2 equity model.

## Mode Contract

Every strategy uses **exactly one mode** (see `agent/stage_2_guideline.md`).

| Mode | Field suffix | Data shape | Position API | Bounds |
|---|---|---|---|---|
| `time_series` | **no suffix** — `self.data.pv_close` | one time series per field per symbol | `self.set_positions(...)` | Long-only `[0, +1]` |
| `cross_sectional` | **`_panel` suffix** — `self.data.pv_close_panel` | time × symbol panel | `self.set_portfolio_positions(...)` | Market-neutral |

Rules:

- The exact mode name is `time_series`, not `timeseries`.
- `time_series` fields carry no suffix: `self.data.pv_close`.
- `cross_sectional` fields always carry the `_panel` suffix: `self.data.pv_close_panel`.
- **Do not mix** series and panel fields in the same strategy.
- A panel always has time on rows and symbols on columns — including for a single-symbol universe.
- `_quarterly_panel` = quarterly report frequency; `_annual_panel` = annual report frequency.
- Use a report only **after it was published**; never shift fundamental data backward, never backfill.

## Section Index

| Group | Jump to |
|---|---|
| Price Volume | [Price Volume](#price-volume) |
| Income Statement — Quarterly | [Income Statement (Q)](#income-statement-quarterly) |
| Income Statement — Annual | [Income Statement (A)](#income-statement-annual) |
| Balance Sheet — Quarterly | [Balance Sheet (Q)](#balance-sheet-quarterly) |
| Balance Sheet — Annual | [Balance Sheet (A)](#balance-sheet-annual) |
| Cash Flow — Quarterly | [Cash Flow (Q)](#cash-flow-quarterly) |
| Cash Flow — Annual | [Cash Flow (A)](#cash-flow-annual) |

## Quick Lookup

| Group | Count | Representative fields |
|---|---|---|
| Price Volume | 10 | `pv_close_panel`, `pv_volume_panel`, `pv_vn30_close_panel` |
| Income Statement | 130 | `fun_is_net_profit_loss_after_tax_*_panel`, `fun_is_eps_basis_*_panel` |
| Balance Sheet | 271 | `fun_bs_total_assets_*_panel`, `fun_bs_owners_equity_*_panel` |
| Cash Flow | 85 | `fun_cf_net_cash_inflows_outflows_from_operating_activities_*_panel` |

> In `time_series` mode, drop the `_panel` suffix: `self.data.pv_close`, `self.data.fun_is_net_profit_loss_after_tax_quarterly`.

## Reading Tips

- Start with Price Volume for every strategy; add fundamentals for quality filters.
- Income statement drives profitability and growth signals.
- Balance sheet drives capital strength, leverage, and liquidity signals.
- Cash flow drives earnings-quality and cash-conversion signals.
- Keep the field names exactly as written; do not rename them in code.


## Price Volume

| Field | Usage (cross_sectional) |
|---|---|
| `pv_open_panel` | `self.data.pv_open_panel` |
| `pv_high_panel` | `self.data.pv_high_panel` |
| `pv_low_panel` | `self.data.pv_low_panel` |
| `pv_close_panel` | `self.data.pv_close_panel` |
| `pv_volume_panel` | `self.data.pv_volume_panel` |
| `pv_vn30_open_panel` | `self.data.pv_vn30_open_panel` |
| `pv_vn30_high_panel` | `self.data.pv_vn30_high_panel` |
| `pv_vn30_low_panel` | `self.data.pv_vn30_low_panel` |
| `pv_vn30_close_panel` | `self.data.pv_vn30_close_panel` |
| `pv_vn30_volume_panel` | `self.data.pv_vn30_volume_panel` |

## Income Statement (Quarterly)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_is_attributable_to_parent_company_quarterly_panel` | `self.data.fun_is_attributable_to_parent_company_quarterly_panel` |
| `fun_is_business_income_tax_current_quarterly_panel` | `self.data.fun_is_business_income_tax_current_quarterly_panel` |
| `fun_is_business_income_tax_deferred_quarterly_panel` | `self.data.fun_is_business_income_tax_deferred_quarterly_panel` |
| `fun_is_claim_and_maturity_payment_expenses_quarterly_panel` | `self.data.fun_is_claim_and_maturity_payment_expenses_quarterly_panel` |
| `fun_is_claim_expenses_for_reinsurance_assumed_quarterly_panel` | `self.data.fun_is_claim_expenses_for_reinsurance_assumed_quarterly_panel` |
| `fun_is_claim_recoveries_from_outward_reinsurance_quarterly_panel` | `self.data.fun_is_claim_recoveries_from_outward_reinsurance_quarterly_panel` |
| `fun_is_commission_income_from_outward_reinsurance_quarterly_panel` | `self.data.fun_is_commission_income_from_outward_reinsurance_quarterly_panel` |
| `fun_is_commission_on_reinsurance_ceded_quarterly_panel` | `self.data.fun_is_commission_on_reinsurance_ceded_quarterly_panel` |
| `fun_is_commissions_quarterly_panel` | `self.data.fun_is_commissions_quarterly_panel` |
| `fun_is_compensation_quarterly_panel` | `self.data.fun_is_compensation_quarterly_panel` |
| `fun_is_deductions_compensation_quarterly_panel` | `self.data.fun_is_deductions_compensation_quarterly_panel` |
| `fun_is_eps_basis_quarterly_panel` | `self.data.fun_is_eps_basis_quarterly_panel` |
| `fun_is_equalisation_reserve_quarterly_panel` | `self.data.fun_is_equalisation_reserve_quarterly_panel` |
| `fun_is_expense_of_handling_fully_indemnified_goods_quarterly_panel` | `self.data.fun_is_expense_of_handling_fully_indemnified_goods_quarterly_panel` |
| `fun_is_expense_of_recourse_against_the_third_party_quarterly_panel` | `self.data.fun_is_expense_of_recourse_against_the_third_party_quarterly_panel` |
| `fun_is_expenses_from_other_activities_quarterly_panel` | `self.data.fun_is_expenses_from_other_activities_quarterly_panel` |
| `fun_is_financial_expenses_quarterly_panel` | `self.data.fun_is_financial_expenses_quarterly_panel` |
| `fun_is_financial_income_quarterly_panel` | `self.data.fun_is_financial_income_quarterly_panel` |
| `fun_is_gain_loss_from_joint_ventures_quarterly_panel` | `self.data.fun_is_gain_loss_from_joint_ventures_quarterly_panel` |
| `fun_is_general_and_admin_expenses_quarterly_panel` | `self.data.fun_is_general_and_admin_expenses_quarterly_panel` |
| `fun_is_gross_insurance_operating_profit_quarterly_panel` | `self.data.fun_is_gross_insurance_operating_profit_quarterly_panel` |
| `fun_is_gross_written_premium_quarterly_panel` | `self.data.fun_is_gross_written_premium_quarterly_panel` |
| `fun_is_increase_decrease_in_claim_reserve_for_outward_insurance_quarterly_panel` | `self.data.fun_is_increase_decrease_in_claim_reserve_for_outward_insurance_quarterly_panel` |
| `fun_is_increase_decrease_in_claim_reserve_quarterly_panel` | `self.data.fun_is_increase_decrease_in_claim_reserve_quarterly_panel` |
| `fun_is_increase_decrease_in_mathematic_reserves_quarterly_panel` | `self.data.fun_is_increase_decrease_in_mathematic_reserves_quarterly_panel` |
| `fun_is_increase_decrease_in_unearned_premium_reserve_quarterly_panel` | `self.data.fun_is_increase_decrease_in_unearned_premium_reserve_quarterly_panel` |
| `fun_is_increase_decrease_minimum_guaranteed_investment_reserve_quarterly_panel` | `self.data.fun_is_increase_decrease_minimum_guaranteed_investment_reserve_quarterly_panel` |
| `fun_is_increase_decrease_other_primary_insurance_technical_reserves_quarterly_panel` | `self.data.fun_is_increase_decrease_other_primary_insurance_technical_reserves_quarterly_panel` |
| `fun_is_increase_decrease_profit_sharing_reserve_quarterly_panel` | `self.data.fun_is_increase_decrease_profit_sharing_reserve_quarterly_panel` |
| `fun_is_increase_decrease_reinsurance_fee_reserves_quarterly_panel` | `self.data.fun_is_increase_decrease_reinsurance_fee_reserves_quarterly_panel` |
| `fun_is_increase_direct_insurance_technical_reserves_quarterly_panel` | `self.data.fun_is_increase_direct_insurance_technical_reserves_quarterly_panel` |
| `fun_is_loss_adjusting_fee_risk_assessment_quarterly_panel` | `self.data.fun_is_loss_adjusting_fee_risk_assessment_quarterly_panel` |
| `fun_is_minority_interests_quarterly_panel` | `self.data.fun_is_minority_interests_quarterly_panel` |
| `fun_is_net_accounting_profit_loss_before_tax_quarterly_panel` | `self.data.fun_is_net_accounting_profit_loss_before_tax_quarterly_panel` |
| `fun_is_net_operating_income_from_other_activities_quarterly_panel` | `self.data.fun_is_net_operating_income_from_other_activities_quarterly_panel` |
| `fun_is_net_operating_profit_from_insurance_operation_quarterly_panel` | `self.data.fun_is_net_operating_profit_from_insurance_operation_quarterly_panel` |
| `fun_is_net_other_income_expenses_quarterly_panel` | `self.data.fun_is_net_other_income_expenses_quarterly_panel` |
| `fun_is_net_profit_loss_after_tax_quarterly_panel` | `self.data.fun_is_net_profit_loss_after_tax_quarterly_panel` |
| `fun_is_net_revenue_of_insurance_premium_quarterly_panel` | `self.data.fun_is_net_revenue_of_insurance_premium_quarterly_panel` |
| `fun_is_net_sales_from_insurance_business_quarterly_panel` | `self.data.fun_is_net_sales_from_insurance_business_quarterly_panel` |
| `fun_is_other_compensation_quarterly_panel` | `self.data.fun_is_other_compensation_quarterly_panel` |
| `fun_is_other_deductions_quarterly_panel` | `self.data.fun_is_other_deductions_quarterly_panel` |
| `fun_is_other_deductions_reinsurance_quarterly_panel` | `self.data.fun_is_other_deductions_reinsurance_quarterly_panel` |
| `fun_is_other_expenses_quarterly_panel` | `self.data.fun_is_other_expenses_quarterly_panel` |
| `fun_is_other_income_from_insurance_activities_quarterly_panel` | `self.data.fun_is_other_income_from_insurance_activities_quarterly_panel` |
| `fun_is_other_income_quarterly_panel` | `self.data.fun_is_other_income_quarterly_panel` |
| `fun_is_other_insurance_activities_expenses_quarterly_panel` | `self.data.fun_is_other_insurance_activities_expenses_quarterly_panel` |
| `fun_is_other_insurance_operating_expenses_quarterly_panel` | `self.data.fun_is_other_insurance_operating_expenses_quarterly_panel` |
| `fun_is_other_reinsurance_assumed_expenses_quarterly_panel` | `self.data.fun_is_other_reinsurance_assumed_expenses_quarterly_panel` |
| `fun_is_other_reinsurance_ceded_expenses_quarterly_panel` | `self.data.fun_is_other_reinsurance_ceded_expenses_quarterly_panel` |
| `fun_is_others_quarterly_panel` | `self.data.fun_is_others_quarterly_panel` |
| `fun_is_profit_from_financial_activities_quarterly_panel` | `self.data.fun_is_profit_from_financial_activities_quarterly_panel` |
| `fun_is_provision_for_catastrophe_reserve_quarterly_panel` | `self.data.fun_is_provision_for_catastrophe_reserve_quarterly_panel` |
| `fun_is_reinsurance_premium_assumed_quarterly_panel` | `self.data.fun_is_reinsurance_premium_assumed_quarterly_panel` |
| `fun_is_reinsurance_premium_ceded_quarterly_panel` | `self.data.fun_is_reinsurance_premium_ceded_quarterly_panel` |
| `fun_is_revenue_from_insurance_premium_quarterly_panel` | `self.data.fun_is_revenue_from_insurance_premium_quarterly_panel` |
| `fun_is_revenue_from_other_activities_quarterly_panel` | `self.data.fun_is_revenue_from_other_activities_quarterly_panel` |
| `fun_is_risk_minimization_expenses_quarterly_panel` | `self.data.fun_is_risk_minimization_expenses_quarterly_panel` |
| `fun_is_salvages_quarterly_panel` | `self.data.fun_is_salvages_quarterly_panel` |
| `fun_is_selling_expenses_quarterly_panel` | `self.data.fun_is_selling_expenses_quarterly_panel` |
| `fun_is_subrogation_recoveries_quarterly_panel` | `self.data.fun_is_subrogation_recoveries_quarterly_panel` |
| `fun_is_total_compensation_quarterly_panel` | `self.data.fun_is_total_compensation_quarterly_panel` |
| `fun_is_total_direct_insurance_operating_expenses_quarterly_panel` | `self.data.fun_is_total_direct_insurance_operating_expenses_quarterly_panel` |
| `fun_is_total_insurance_claim_settlement_expenses_quarterly_panel` | `self.data.fun_is_total_insurance_claim_settlement_expenses_quarterly_panel` |
| `fun_is_total_reinsurance_premium_ceded_quarterly_panel` | `self.data.fun_is_total_reinsurance_premium_ceded_quarterly_panel` |

## Income Statement (Annual)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_is_attributable_to_parent_company_annual_panel` | `self.data.fun_is_attributable_to_parent_company_annual_panel` |
| `fun_is_business_income_tax_current_annual_panel` | `self.data.fun_is_business_income_tax_current_annual_panel` |
| `fun_is_business_income_tax_deferred_annual_panel` | `self.data.fun_is_business_income_tax_deferred_annual_panel` |
| `fun_is_claim_and_maturity_payment_expenses_annual_panel` | `self.data.fun_is_claim_and_maturity_payment_expenses_annual_panel` |
| `fun_is_claim_expenses_for_reinsurance_assumed_annual_panel` | `self.data.fun_is_claim_expenses_for_reinsurance_assumed_annual_panel` |
| `fun_is_claim_recoveries_from_outward_reinsurance_annual_panel` | `self.data.fun_is_claim_recoveries_from_outward_reinsurance_annual_panel` |
| `fun_is_commission_income_from_outward_reinsurance_annual_panel` | `self.data.fun_is_commission_income_from_outward_reinsurance_annual_panel` |
| `fun_is_commission_on_reinsurance_ceded_annual_panel` | `self.data.fun_is_commission_on_reinsurance_ceded_annual_panel` |
| `fun_is_commissions_annual_panel` | `self.data.fun_is_commissions_annual_panel` |
| `fun_is_compensation_annual_panel` | `self.data.fun_is_compensation_annual_panel` |
| `fun_is_deductions_compensation_annual_panel` | `self.data.fun_is_deductions_compensation_annual_panel` |
| `fun_is_eps_basis_annual_panel` | `self.data.fun_is_eps_basis_annual_panel` |
| `fun_is_equalisation_reserve_annual_panel` | `self.data.fun_is_equalisation_reserve_annual_panel` |
| `fun_is_expense_of_handling_fully_indemnified_goods_annual_panel` | `self.data.fun_is_expense_of_handling_fully_indemnified_goods_annual_panel` |
| `fun_is_expense_of_recourse_against_the_third_party_annual_panel` | `self.data.fun_is_expense_of_recourse_against_the_third_party_annual_panel` |
| `fun_is_expenses_from_other_activities_annual_panel` | `self.data.fun_is_expenses_from_other_activities_annual_panel` |
| `fun_is_financial_expenses_annual_panel` | `self.data.fun_is_financial_expenses_annual_panel` |
| `fun_is_financial_income_annual_panel` | `self.data.fun_is_financial_income_annual_panel` |
| `fun_is_gain_loss_from_joint_ventures_annual_panel` | `self.data.fun_is_gain_loss_from_joint_ventures_annual_panel` |
| `fun_is_general_and_admin_expenses_annual_panel` | `self.data.fun_is_general_and_admin_expenses_annual_panel` |
| `fun_is_gross_insurance_operating_profit_annual_panel` | `self.data.fun_is_gross_insurance_operating_profit_annual_panel` |
| `fun_is_gross_written_premium_annual_panel` | `self.data.fun_is_gross_written_premium_annual_panel` |
| `fun_is_increase_decrease_in_claim_reserve_annual_panel` | `self.data.fun_is_increase_decrease_in_claim_reserve_annual_panel` |
| `fun_is_increase_decrease_in_claim_reserve_for_outward_insurance_annual_panel` | `self.data.fun_is_increase_decrease_in_claim_reserve_for_outward_insurance_annual_panel` |
| `fun_is_increase_decrease_in_mathematic_reserves_annual_panel` | `self.data.fun_is_increase_decrease_in_mathematic_reserves_annual_panel` |
| `fun_is_increase_decrease_in_unearned_premium_reserve_annual_panel` | `self.data.fun_is_increase_decrease_in_unearned_premium_reserve_annual_panel` |
| `fun_is_increase_decrease_minimum_guaranteed_investment_reserve_annual_panel` | `self.data.fun_is_increase_decrease_minimum_guaranteed_investment_reserve_annual_panel` |
| `fun_is_increase_decrease_other_primary_insurance_technical_reserves_annual_panel` | `self.data.fun_is_increase_decrease_other_primary_insurance_technical_reserves_annual_panel` |
| `fun_is_increase_decrease_profit_sharing_reserve_annual_panel` | `self.data.fun_is_increase_decrease_profit_sharing_reserve_annual_panel` |
| `fun_is_increase_decrease_reinsurance_fee_reserves_annual_panel` | `self.data.fun_is_increase_decrease_reinsurance_fee_reserves_annual_panel` |
| `fun_is_increase_direct_insurance_technical_reserves_annual_panel` | `self.data.fun_is_increase_direct_insurance_technical_reserves_annual_panel` |
| `fun_is_loss_adjusting_fee_risk_assessment_annual_panel` | `self.data.fun_is_loss_adjusting_fee_risk_assessment_annual_panel` |
| `fun_is_minority_interests_annual_panel` | `self.data.fun_is_minority_interests_annual_panel` |
| `fun_is_net_accounting_profit_loss_before_tax_annual_panel` | `self.data.fun_is_net_accounting_profit_loss_before_tax_annual_panel` |
| `fun_is_net_operating_income_from_other_activities_annual_panel` | `self.data.fun_is_net_operating_income_from_other_activities_annual_panel` |
| `fun_is_net_operating_profit_from_insurance_operation_annual_panel` | `self.data.fun_is_net_operating_profit_from_insurance_operation_annual_panel` |
| `fun_is_net_other_income_expenses_annual_panel` | `self.data.fun_is_net_other_income_expenses_annual_panel` |
| `fun_is_net_profit_loss_after_tax_annual_panel` | `self.data.fun_is_net_profit_loss_after_tax_annual_panel` |
| `fun_is_net_revenue_of_insurance_premium_annual_panel` | `self.data.fun_is_net_revenue_of_insurance_premium_annual_panel` |
| `fun_is_net_sales_from_insurance_business_annual_panel` | `self.data.fun_is_net_sales_from_insurance_business_annual_panel` |
| `fun_is_other_compensation_annual_panel` | `self.data.fun_is_other_compensation_annual_panel` |
| `fun_is_other_deductions_annual_panel` | `self.data.fun_is_other_deductions_annual_panel` |
| `fun_is_other_deductions_reinsurance_annual_panel` | `self.data.fun_is_other_deductions_reinsurance_annual_panel` |
| `fun_is_other_expenses_annual_panel` | `self.data.fun_is_other_expenses_annual_panel` |
| `fun_is_other_income_annual_panel` | `self.data.fun_is_other_income_annual_panel` |
| `fun_is_other_income_from_insurance_activities_annual_panel` | `self.data.fun_is_other_income_from_insurance_activities_annual_panel` |
| `fun_is_other_insurance_activities_expenses_annual_panel` | `self.data.fun_is_other_insurance_activities_expenses_annual_panel` |
| `fun_is_other_insurance_operating_expenses_annual_panel` | `self.data.fun_is_other_insurance_operating_expenses_annual_panel` |
| `fun_is_other_reinsurance_assumed_expenses_annual_panel` | `self.data.fun_is_other_reinsurance_assumed_expenses_annual_panel` |
| `fun_is_other_reinsurance_ceded_expenses_annual_panel` | `self.data.fun_is_other_reinsurance_ceded_expenses_annual_panel` |
| `fun_is_others_annual_panel` | `self.data.fun_is_others_annual_panel` |
| `fun_is_profit_from_financial_activities_annual_panel` | `self.data.fun_is_profit_from_financial_activities_annual_panel` |
| `fun_is_provision_for_catastrophe_reserve_annual_panel` | `self.data.fun_is_provision_for_catastrophe_reserve_annual_panel` |
| `fun_is_reinsurance_premium_assumed_annual_panel` | `self.data.fun_is_reinsurance_premium_assumed_annual_panel` |
| `fun_is_reinsurance_premium_ceded_annual_panel` | `self.data.fun_is_reinsurance_premium_ceded_annual_panel` |
| `fun_is_revenue_from_insurance_premium_annual_panel` | `self.data.fun_is_revenue_from_insurance_premium_annual_panel` |
| `fun_is_revenue_from_other_activities_annual_panel` | `self.data.fun_is_revenue_from_other_activities_annual_panel` |
| `fun_is_risk_minimization_expenses_annual_panel` | `self.data.fun_is_risk_minimization_expenses_annual_panel` |
| `fun_is_salvages_annual_panel` | `self.data.fun_is_salvages_annual_panel` |
| `fun_is_selling_expenses_annual_panel` | `self.data.fun_is_selling_expenses_annual_panel` |
| `fun_is_subrogation_recoveries_annual_panel` | `self.data.fun_is_subrogation_recoveries_annual_panel` |
| `fun_is_total_compensation_annual_panel` | `self.data.fun_is_total_compensation_annual_panel` |
| `fun_is_total_direct_insurance_operating_expenses_annual_panel` | `self.data.fun_is_total_direct_insurance_operating_expenses_annual_panel` |
| `fun_is_total_insurance_claim_settlement_expenses_annual_panel` | `self.data.fun_is_total_insurance_claim_settlement_expenses_annual_panel` |
| `fun_is_total_reinsurance_premium_ceded_annual_panel` | `self.data.fun_is_total_reinsurance_premium_ceded_annual_panel` |

## Balance Sheet (Quarterly)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_bs_accounts_receivable_quarterly_panel` | `self.data.fun_bs_accounts_receivable_quarterly_panel` |
| `fun_bs_accrued_expenses_quarterly_panel` | `self.data.fun_bs_accrued_expenses_quarterly_panel` |
| `fun_bs_advances_from_customers_quarterly_panel` | `self.data.fun_bs_advances_from_customers_quarterly_panel` |
| `fun_bs_advances_quarterly_panel` | `self.data.fun_bs_advances_quarterly_panel` |
| `fun_bs_beginning_accumulated_undistributed_earnings_quarterly_panel` | `self.data.fun_bs_beginning_accumulated_undistributed_earnings_quarterly_panel` |
| `fun_bs_bonus_and_welfare_funds_quarterly_panel` | `self.data.fun_bs_bonus_and_welfare_funds_quarterly_panel` |
| `fun_bs_budget_funding_quarterly_panel` | `self.data.fun_bs_budget_funding_quarterly_panel` |
| `fun_bs_budget_sources_and_other_funds_quarterly_panel` | `self.data.fun_bs_budget_sources_and_other_funds_quarterly_panel` |
| `fun_bs_capital_and_researves_quarterly_panel` | `self.data.fun_bs_capital_and_researves_quarterly_panel` |
| `fun_bs_capital_surplus_quarterly_panel` | `self.data.fun_bs_capital_surplus_quarterly_panel` |
| `fun_bs_cash_and_cash_equivalents_quarterly_panel` | `self.data.fun_bs_cash_and_cash_equivalents_quarterly_panel` |
| `fun_bs_cash_equivalents_quarterly_panel` | `self.data.fun_bs_cash_equivalents_quarterly_panel` |
| `fun_bs_cash_quarterly_panel` | `self.data.fun_bs_cash_quarterly_panel` |
| `fun_bs_catastrophe_reserve_quarterly_panel` | `self.data.fun_bs_catastrophe_reserve_quarterly_panel` |
| `fun_bs_claim_reserve_quarterly_panel` | `self.data.fun_bs_claim_reserve_quarterly_panel` |
| `fun_bs_common_shares_quarterly_panel` | `self.data.fun_bs_common_shares_quarterly_panel` |
| `fun_bs_construction_in_progress_quarterly_panel` | `self.data.fun_bs_construction_in_progress_quarterly_panel` |
| `fun_bs_convertible_bonds_quarterly_panel` | `self.data.fun_bs_convertible_bonds_quarterly_panel` |
| `fun_bs_current_assets_quarterly_panel` | `self.data.fun_bs_current_assets_quarterly_panel` |
| `fun_bs_current_liabilities_quarterly_panel` | `self.data.fun_bs_current_liabilities_quarterly_panel` |
| `fun_bs_current_period_undistributed_earnings_quarterly_panel` | `self.data.fun_bs_current_period_undistributed_earnings_quarterly_panel` |
| `fun_bs_deferred_income_tax_assets_quarterly_panel` | `self.data.fun_bs_deferred_income_tax_assets_quarterly_panel` |
| `fun_bs_deferred_income_tax_liabilities_quarterly_panel` | `self.data.fun_bs_deferred_income_tax_liabilities_quarterly_panel` |
| `fun_bs_deffered_revenue_quarterly_panel` | `self.data.fun_bs_deffered_revenue_quarterly_panel` |
| `fun_bs_differences_upon_asset_revaluation_quarterly_panel` | `self.data.fun_bs_differences_upon_asset_revaluation_quarterly_panel` |
| `fun_bs_dividend_reserves_quarterly_panel` | `self.data.fun_bs_dividend_reserves_quarterly_panel` |
| `fun_bs_equalization_reserves_quarterly_panel` | `self.data.fun_bs_equalization_reserves_quarterly_panel` |
| `fun_bs_finance_lease_assets_accum_depreciation_quarterly_panel` | `self.data.fun_bs_finance_lease_assets_accum_depreciation_quarterly_panel` |
| `fun_bs_finance_lease_assets_quarterly_panel` | `self.data.fun_bs_finance_lease_assets_quarterly_panel` |
| `fun_bs_financial_reserve_funds_quarterly_panel` | `self.data.fun_bs_financial_reserve_funds_quarterly_panel` |
| `fun_bs_fixed_assets_quarterly_panel` | `self.data.fun_bs_fixed_assets_quarterly_panel` |
| `fun_bs_foreign_exchange_differences_quarterly_panel` | `self.data.fun_bs_foreign_exchange_differences_quarterly_panel` |
| `fun_bs_funds_used_for_fixed_asset_acquisitions_quarterly_panel` | `self.data.fun_bs_funds_used_for_fixed_asset_acquisitions_quarterly_panel` |
| `fun_bs_good_will_quarterly_panel` | `self.data.fun_bs_good_will_quarterly_panel` |
| `fun_bs_government_bonds_purchased_for_resale_payable_quarterly_panel` | `self.data.fun_bs_government_bonds_purchased_for_resale_payable_quarterly_panel` |
| `fun_bs_government_bonds_purchased_for_resale_receivable_quarterly_panel` | `self.data.fun_bs_government_bonds_purchased_for_resale_receivable_quarterly_panel` |
| `fun_bs_held_to_maturity_investment_current_quarterly_panel` | `self.data.fun_bs_held_to_maturity_investment_current_quarterly_panel` |
| `fun_bs_held_to_maturity_investment_non_current_quarterly_panel` | `self.data.fun_bs_held_to_maturity_investment_non_current_quarterly_panel` |
| `fun_bs_insurance_deposits_quarterly_panel` | `self.data.fun_bs_insurance_deposits_quarterly_panel` |
| `fun_bs_insurance_reserve_quarterly_panel` | `self.data.fun_bs_insurance_reserve_quarterly_panel` |
| `fun_bs_intangible_assets_accum_amortization_quarterly_panel` | `self.data.fun_bs_intangible_assets_accum_amortization_quarterly_panel` |
| `fun_bs_intangible_cost_quarterly_panel` | `self.data.fun_bs_intangible_cost_quarterly_panel` |
| `fun_bs_intangible_fixed_assets_quarterly_panel` | `self.data.fun_bs_intangible_fixed_assets_quarterly_panel` |
| `fun_bs_intercompany_receivables_quarterly_panel` | `self.data.fun_bs_intercompany_receivables_quarterly_panel` |
| `fun_bs_intra_company_payables_for_operating_capital_received_quarterly_panel` | `self.data.fun_bs_intra_company_payables_for_operating_capital_received_quarterly_panel` |
| `fun_bs_inventories_net_quarterly_panel` | `self.data.fun_bs_inventories_net_quarterly_panel` |
| `fun_bs_inventories_quarterly_panel` | `self.data.fun_bs_inventories_quarterly_panel` |
| `fun_bs_investment_and_development_funds_quarterly_panel` | `self.data.fun_bs_investment_and_development_funds_quarterly_panel` |
| `fun_bs_investment_properties_quarterly_panel` | `self.data.fun_bs_investment_properties_quarterly_panel` |
| `fun_bs_investment_property_accum_depreciation_quarterly_panel` | `self.data.fun_bs_investment_property_accum_depreciation_quarterly_panel` |
| `fun_bs_investment_property_cost_quarterly_panel` | `self.data.fun_bs_investment_property_cost_quarterly_panel` |
| `fun_bs_investments_in_associates_quarterly_panel` | `self.data.fun_bs_investments_in_associates_quarterly_panel` |
| `fun_bs_investments_in_subsidiaries_quarterly_panel` | `self.data.fun_bs_investments_in_subsidiaries_quarterly_panel` |
| `fun_bs_liabilities_quarterly_panel` | `self.data.fun_bs_liabilities_quarterly_panel` |
| `fun_bs_long_term_accrued_expenses_quarterly_panel` | `self.data.fun_bs_long_term_accrued_expenses_quarterly_panel` |
| `fun_bs_long_term_advances_from_customers_quarterly_panel` | `self.data.fun_bs_long_term_advances_from_customers_quarterly_panel` |
| `fun_bs_long_term_assets_quarterly_panel` | `self.data.fun_bs_long_term_assets_quarterly_panel` |
| `fun_bs_long_term_cost_of_work_in_progress_quarterly_panel` | `self.data.fun_bs_long_term_cost_of_work_in_progress_quarterly_panel` |
| `fun_bs_long_term_deposit_mortgage_quarterly_panel` | `self.data.fun_bs_long_term_deposit_mortgage_quarterly_panel` |
| `fun_bs_long_term_deposits_quarterly_panel` | `self.data.fun_bs_long_term_deposits_quarterly_panel` |
| `fun_bs_long_term_equipment_material_and_spare_parts_quarterly_panel` | `self.data.fun_bs_long_term_equipment_material_and_spare_parts_quarterly_panel` |
| `fun_bs_long_term_incomplete_assets_quarterly_panel` | `self.data.fun_bs_long_term_incomplete_assets_quarterly_panel` |
| `fun_bs_long_term_intercompany_payables_quarterly_panel` | `self.data.fun_bs_long_term_intercompany_payables_quarterly_panel` |
| `fun_bs_long_term_intercompany_receivables_quarterly_panel` | `self.data.fun_bs_long_term_intercompany_receivables_quarterly_panel` |
| `fun_bs_long_term_investments_quarterly_panel` | `self.data.fun_bs_long_term_investments_quarterly_panel` |
| `fun_bs_long_term_liabilities_quarterly_panel` | `self.data.fun_bs_long_term_liabilities_quarterly_panel` |
| `fun_bs_long_term_loans_quarterly_panel` | `self.data.fun_bs_long_term_loans_quarterly_panel` |
| `fun_bs_long_term_prepayments_quarterly_panel` | `self.data.fun_bs_long_term_prepayments_quarterly_panel` |
| `fun_bs_long_term_prepayments_to_suppliers_quarterly_panel` | `self.data.fun_bs_long_term_prepayments_to_suppliers_quarterly_panel` |
| `fun_bs_long_term_receivables_quarterly_panel` | `self.data.fun_bs_long_term_receivables_quarterly_panel` |
| `fun_bs_long_term_trade_payables_quarterly_panel` | `self.data.fun_bs_long_term_trade_payables_quarterly_panel` |
| `fun_bs_long_term_trade_receivables_quarterly_panel` | `self.data.fun_bs_long_term_trade_receivables_quarterly_panel` |
| `fun_bs_margin_deposits_quarterly_panel` | `self.data.fun_bs_margin_deposits_quarterly_panel` |
| `fun_bs_mathematical_reserve_quarterly_panel` | `self.data.fun_bs_mathematical_reserve_quarterly_panel` |
| `fun_bs_minority_interests_quarterly_panel` | `self.data.fun_bs_minority_interests_quarterly_panel` |
| `fun_bs_other_current_assets_quarterly_panel` | `self.data.fun_bs_other_current_assets_quarterly_panel` |
| `fun_bs_other_current_assets_residual_quarterly_panel` | `self.data.fun_bs_other_current_assets_residual_quarterly_panel` |
| `fun_bs_other_funds_quarterly_panel` | `self.data.fun_bs_other_funds_quarterly_panel` |
| `fun_bs_other_long_term_assets_quarterly_panel` | `self.data.fun_bs_other_long_term_assets_quarterly_panel` |
| `fun_bs_other_long_term_assets_residual_quarterly_panel` | `self.data.fun_bs_other_long_term_assets_residual_quarterly_panel` |
| `fun_bs_other_long_term_investments_quarterly_panel` | `self.data.fun_bs_other_long_term_investments_quarterly_panel` |
| `fun_bs_other_long_term_payables_quarterly_panel` | `self.data.fun_bs_other_long_term_payables_quarterly_panel` |
| `fun_bs_other_long_term_receivables_quarterly_panel` | `self.data.fun_bs_other_long_term_receivables_quarterly_panel` |
| `fun_bs_other_long_term_receivables_residual_quarterly_panel` | `self.data.fun_bs_other_long_term_receivables_residual_quarterly_panel` |
| `fun_bs_other_payables_quarterly_panel` | `self.data.fun_bs_other_payables_quarterly_panel` |
| `fun_bs_other_receivable_from_customers_quarterly_panel` | `self.data.fun_bs_other_receivable_from_customers_quarterly_panel` |
| `fun_bs_other_receivables_quarterly_panel` | `self.data.fun_bs_other_receivables_quarterly_panel` |
| `fun_bs_other_reserves_quarterly_panel` | `self.data.fun_bs_other_reserves_quarterly_panel` |
| `fun_bs_other_short_term_payables_quarterly_panel` | `self.data.fun_bs_other_short_term_payables_quarterly_panel` |
| `fun_bs_other_short_term_prepayments_quarterly_panel` | `self.data.fun_bs_other_short_term_prepayments_quarterly_panel` |
| `fun_bs_other_taxes_receivable_quarterly_panel` | `self.data.fun_bs_other_taxes_receivable_quarterly_panel` |
| `fun_bs_owners_equity_quarterly_panel` | `self.data.fun_bs_owners_equity_quarterly_panel` |
| `fun_bs_owners_other_capital_quarterly_panel` | `self.data.fun_bs_owners_other_capital_quarterly_panel` |
| `fun_bs_paid_in_capital_quarterly_panel` | `self.data.fun_bs_paid_in_capital_quarterly_panel` |
| `fun_bs_payable_to_employees_quarterly_panel` | `self.data.fun_bs_payable_to_employees_quarterly_panel` |
| `fun_bs_payables_from_insurance_contract_quarterly_panel` | `self.data.fun_bs_payables_from_insurance_contract_quarterly_panel` |
| `fun_bs_payables_to_suppliers_quarterly_panel` | `self.data.fun_bs_payables_to_suppliers_quarterly_panel` |
| `fun_bs_ppe_finance_cost_quarterly_panel` | `self.data.fun_bs_ppe_finance_cost_quarterly_panel` |
| `fun_bs_ppe_tangible_cost_quarterly_panel` | `self.data.fun_bs_ppe_tangible_cost_quarterly_panel` |
| `fun_bs_preferred_shares_liabilities_quarterly_panel` | `self.data.fun_bs_preferred_shares_liabilities_quarterly_panel` |
| `fun_bs_preferred_shares_quarterly_panel` | `self.data.fun_bs_preferred_shares_quarterly_panel` |
| `fun_bs_prepayments_to_suppliers_quarterly_panel` | `self.data.fun_bs_prepayments_to_suppliers_quarterly_panel` |
| `fun_bs_provision_for_claim_from_outward_reinsurance_quarterly_panel` | `self.data.fun_bs_provision_for_claim_from_outward_reinsurance_quarterly_panel` |
| `fun_bs_provision_for_decline_in_inventories_quarterly_panel` | `self.data.fun_bs_provision_for_decline_in_inventories_quarterly_panel` |
| `fun_bs_provision_for_diminution_quarterly_panel` | `self.data.fun_bs_provision_for_diminution_quarterly_panel` |
| `fun_bs_provision_for_doubtful_debts_quarterly_panel` | `self.data.fun_bs_provision_for_doubtful_debts_quarterly_panel` |
| `fun_bs_provision_for_doubtful_lt_receivable_quarterly_panel` | `self.data.fun_bs_provision_for_doubtful_lt_receivable_quarterly_panel` |
| `fun_bs_provision_for_long_term_investments_quarterly_panel` | `self.data.fun_bs_provision_for_long_term_investments_quarterly_panel` |
| `fun_bs_provision_for_long_term_liabilities_quarterly_panel` | `self.data.fun_bs_provision_for_long_term_liabilities_quarterly_panel` |
| `fun_bs_provision_for_premium_outward_reinsurance_quarterly_panel` | `self.data.fun_bs_provision_for_premium_outward_reinsurance_quarterly_panel` |
| `fun_bs_provision_for_severance_allowances_quarterly_panel` | `self.data.fun_bs_provision_for_severance_allowances_quarterly_panel` |
| `fun_bs_provision_for_st_liabilities_quarterly_panel` | `self.data.fun_bs_provision_for_st_liabilities_quarterly_panel` |
| `fun_bs_receivable_from_insurance_contract_quarterly_panel` | `self.data.fun_bs_receivable_from_insurance_contract_quarterly_panel` |
| `fun_bs_reinsurance_assets_quarterly_panel` | `self.data.fun_bs_reinsurance_assets_quarterly_panel` |
| `fun_bs_short_term_financial_investments_quarterly_panel` | `self.data.fun_bs_short_term_financial_investments_quarterly_panel` |
| `fun_bs_short_term_investments_quarterly_panel` | `self.data.fun_bs_short_term_investments_quarterly_panel` |
| `fun_bs_short_term_loans_quarterly_panel` | `self.data.fun_bs_short_term_loans_quarterly_panel` |
| `fun_bs_short_term_loans_receivables_quarterly_panel` | `self.data.fun_bs_short_term_loans_receivables_quarterly_panel` |
| `fun_bs_short_term_prepayments_quarterly_panel` | `self.data.fun_bs_short_term_prepayments_quarterly_panel` |
| `fun_bs_short_term_unrealized_revenue_quarterly_panel` | `self.data.fun_bs_short_term_unrealized_revenue_quarterly_panel` |
| `fun_bs_shortage_of_current_assets_waiting_for_solution_quarterly_panel` | `self.data.fun_bs_shortage_of_current_assets_waiting_for_solution_quarterly_panel` |
| `fun_bs_statutory_reserve_quarterly_panel` | `self.data.fun_bs_statutory_reserve_quarterly_panel` |
| `fun_bs_tangible_assets_accum_depreciation_quarterly_panel` | `self.data.fun_bs_tangible_assets_accum_depreciation_quarterly_panel` |
| `fun_bs_tangible_fixed_assets_quarterly_panel` | `self.data.fun_bs_tangible_fixed_assets_quarterly_panel` |
| `fun_bs_taxes_and_other_payable_to_state_budget_quarterly_panel` | `self.data.fun_bs_taxes_and_other_payable_to_state_budget_quarterly_panel` |
| `fun_bs_technology_science_development_fund_quarterly_panel` | `self.data.fun_bs_technology_science_development_fund_quarterly_panel` |
| `fun_bs_total_assets_quarterly_panel` | `self.data.fun_bs_total_assets_quarterly_panel` |
| `fun_bs_total_resources_quarterly_panel` | `self.data.fun_bs_total_resources_quarterly_panel` |
| `fun_bs_trade_accounts_payable_quarterly_panel` | `self.data.fun_bs_trade_accounts_payable_quarterly_panel` |
| `fun_bs_trade_accounts_receivable_quarterly_panel` | `self.data.fun_bs_trade_accounts_receivable_quarterly_panel` |
| `fun_bs_treasury_shares_quarterly_panel` | `self.data.fun_bs_treasury_shares_quarterly_panel` |
| `fun_bs_undistributed_commission_expenses_quarterly_panel` | `self.data.fun_bs_undistributed_commission_expenses_quarterly_panel` |
| `fun_bs_undistributed_earnings_quarterly_panel` | `self.data.fun_bs_undistributed_earnings_quarterly_panel` |
| `fun_bs_unearned_commission_income_quarterly_panel` | `self.data.fun_bs_unearned_commission_income_quarterly_panel` |
| `fun_bs_unearned_premium_reserve_quarterly_panel` | `self.data.fun_bs_unearned_premium_reserve_quarterly_panel` |
| `fun_bs_vat_to_be_claimed_quarterly_panel` | `self.data.fun_bs_vat_to_be_claimed_quarterly_panel` |

## Balance Sheet (Annual)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_bs_accounts_receivable_annual_panel` | `self.data.fun_bs_accounts_receivable_annual_panel` |
| `fun_bs_accrued_expenses_annual_panel` | `self.data.fun_bs_accrued_expenses_annual_panel` |
| `fun_bs_advances_annual_panel` | `self.data.fun_bs_advances_annual_panel` |
| `fun_bs_advances_from_customers_annual_panel` | `self.data.fun_bs_advances_from_customers_annual_panel` |
| `fun_bs_beginning_accumulated_undistributed_earnings_annual_panel` | `self.data.fun_bs_beginning_accumulated_undistributed_earnings_annual_panel` |
| `fun_bs_bonus_and_welfare_funds_annual_panel` | `self.data.fun_bs_bonus_and_welfare_funds_annual_panel` |
| `fun_bs_budget_funding_annual_panel` | `self.data.fun_bs_budget_funding_annual_panel` |
| `fun_bs_budget_sources_and_other_funds_annual_panel` | `self.data.fun_bs_budget_sources_and_other_funds_annual_panel` |
| `fun_bs_capital_and_researves_annual_panel` | `self.data.fun_bs_capital_and_researves_annual_panel` |
| `fun_bs_capital_surplus_annual_panel` | `self.data.fun_bs_capital_surplus_annual_panel` |
| `fun_bs_cash_and_cash_equivalents_annual_panel` | `self.data.fun_bs_cash_and_cash_equivalents_annual_panel` |
| `fun_bs_cash_annual_panel` | `self.data.fun_bs_cash_annual_panel` |
| `fun_bs_cash_equivalents_annual_panel` | `self.data.fun_bs_cash_equivalents_annual_panel` |
| `fun_bs_catastrophe_reserve_annual_panel` | `self.data.fun_bs_catastrophe_reserve_annual_panel` |
| `fun_bs_claim_reserve_annual_panel` | `self.data.fun_bs_claim_reserve_annual_panel` |
| `fun_bs_common_shares_annual_panel` | `self.data.fun_bs_common_shares_annual_panel` |
| `fun_bs_construction_in_progress_annual_panel` | `self.data.fun_bs_construction_in_progress_annual_panel` |
| `fun_bs_convertible_bonds_annual_panel` | `self.data.fun_bs_convertible_bonds_annual_panel` |
| `fun_bs_current_assets_annual_panel` | `self.data.fun_bs_current_assets_annual_panel` |
| `fun_bs_current_liabilities_annual_panel` | `self.data.fun_bs_current_liabilities_annual_panel` |
| `fun_bs_current_period_undistributed_earnings_annual_panel` | `self.data.fun_bs_current_period_undistributed_earnings_annual_panel` |
| `fun_bs_deferred_income_tax_assets_annual_panel` | `self.data.fun_bs_deferred_income_tax_assets_annual_panel` |
| `fun_bs_deferred_income_tax_liabilities_annual_panel` | `self.data.fun_bs_deferred_income_tax_liabilities_annual_panel` |
| `fun_bs_deffered_revenue_annual_panel` | `self.data.fun_bs_deffered_revenue_annual_panel` |
| `fun_bs_differences_upon_asset_revaluation_annual_panel` | `self.data.fun_bs_differences_upon_asset_revaluation_annual_panel` |
| `fun_bs_dividend_reserves_annual_panel` | `self.data.fun_bs_dividend_reserves_annual_panel` |
| `fun_bs_equalization_reserves_annual_panel` | `self.data.fun_bs_equalization_reserves_annual_panel` |
| `fun_bs_finance_lease_assets_accum_depreciation_annual_panel` | `self.data.fun_bs_finance_lease_assets_accum_depreciation_annual_panel` |
| `fun_bs_finance_lease_assets_annual_panel` | `self.data.fun_bs_finance_lease_assets_annual_panel` |
| `fun_bs_financial_reserve_funds_annual_panel` | `self.data.fun_bs_financial_reserve_funds_annual_panel` |
| `fun_bs_fixed_assets_annual_panel` | `self.data.fun_bs_fixed_assets_annual_panel` |
| `fun_bs_foreign_exchange_differences_annual_panel` | `self.data.fun_bs_foreign_exchange_differences_annual_panel` |
| `fun_bs_funds_used_for_fixed_asset_acquisitions_annual_panel` | `self.data.fun_bs_funds_used_for_fixed_asset_acquisitions_annual_panel` |
| `fun_bs_good_will_annual_panel` | `self.data.fun_bs_good_will_annual_panel` |
| `fun_bs_government_bonds_purchased_for_resale_payable_annual_panel` | `self.data.fun_bs_government_bonds_purchased_for_resale_payable_annual_panel` |
| `fun_bs_government_bonds_purchased_for_resale_receivable_annual_panel` | `self.data.fun_bs_government_bonds_purchased_for_resale_receivable_annual_panel` |
| `fun_bs_held_to_maturity_investment_current_annual_panel` | `self.data.fun_bs_held_to_maturity_investment_current_annual_panel` |
| `fun_bs_held_to_maturity_investment_non_current_annual_panel` | `self.data.fun_bs_held_to_maturity_investment_non_current_annual_panel` |
| `fun_bs_insurance_deposits_annual_panel` | `self.data.fun_bs_insurance_deposits_annual_panel` |
| `fun_bs_insurance_reserve_annual_panel` | `self.data.fun_bs_insurance_reserve_annual_panel` |
| `fun_bs_intangible_assets_accum_amortization_annual_panel` | `self.data.fun_bs_intangible_assets_accum_amortization_annual_panel` |
| `fun_bs_intangible_cost_annual_panel` | `self.data.fun_bs_intangible_cost_annual_panel` |
| `fun_bs_intangible_fixed_assets_annual_panel` | `self.data.fun_bs_intangible_fixed_assets_annual_panel` |
| `fun_bs_intercompany_receivables_annual_panel` | `self.data.fun_bs_intercompany_receivables_annual_panel` |
| `fun_bs_intra_company_payables_for_operating_capital_received_annual_panel` | `self.data.fun_bs_intra_company_payables_for_operating_capital_received_annual_panel` |
| `fun_bs_inventories_annual_panel` | `self.data.fun_bs_inventories_annual_panel` |
| `fun_bs_inventories_net_annual_panel` | `self.data.fun_bs_inventories_net_annual_panel` |
| `fun_bs_investment_and_development_funds_annual_panel` | `self.data.fun_bs_investment_and_development_funds_annual_panel` |
| `fun_bs_investment_properties_annual_panel` | `self.data.fun_bs_investment_properties_annual_panel` |
| `fun_bs_investment_property_accum_depreciation_annual_panel` | `self.data.fun_bs_investment_property_accum_depreciation_annual_panel` |
| `fun_bs_investment_property_cost_annual_panel` | `self.data.fun_bs_investment_property_cost_annual_panel` |
| `fun_bs_investments_in_associates_annual_panel` | `self.data.fun_bs_investments_in_associates_annual_panel` |
| `fun_bs_investments_in_subsidiaries_annual_panel` | `self.data.fun_bs_investments_in_subsidiaries_annual_panel` |
| `fun_bs_liabilities_annual_panel` | `self.data.fun_bs_liabilities_annual_panel` |
| `fun_bs_long_term_accrued_expenses_annual_panel` | `self.data.fun_bs_long_term_accrued_expenses_annual_panel` |
| `fun_bs_long_term_advances_from_customers_annual_panel` | `self.data.fun_bs_long_term_advances_from_customers_annual_panel` |
| `fun_bs_long_term_assets_annual_panel` | `self.data.fun_bs_long_term_assets_annual_panel` |
| `fun_bs_long_term_cost_of_work_in_progress_annual_panel` | `self.data.fun_bs_long_term_cost_of_work_in_progress_annual_panel` |
| `fun_bs_long_term_deposit_mortgage_annual_panel` | `self.data.fun_bs_long_term_deposit_mortgage_annual_panel` |
| `fun_bs_long_term_deposits_annual_panel` | `self.data.fun_bs_long_term_deposits_annual_panel` |
| `fun_bs_long_term_equipment_material_and_spare_parts_annual_panel` | `self.data.fun_bs_long_term_equipment_material_and_spare_parts_annual_panel` |
| `fun_bs_long_term_incomplete_assets_annual_panel` | `self.data.fun_bs_long_term_incomplete_assets_annual_panel` |
| `fun_bs_long_term_intercompany_payables_annual_panel` | `self.data.fun_bs_long_term_intercompany_payables_annual_panel` |
| `fun_bs_long_term_intercompany_receivables_annual_panel` | `self.data.fun_bs_long_term_intercompany_receivables_annual_panel` |
| `fun_bs_long_term_investments_annual_panel` | `self.data.fun_bs_long_term_investments_annual_panel` |
| `fun_bs_long_term_liabilities_annual_panel` | `self.data.fun_bs_long_term_liabilities_annual_panel` |
| `fun_bs_long_term_loans_annual_panel` | `self.data.fun_bs_long_term_loans_annual_panel` |
| `fun_bs_long_term_prepayments_annual_panel` | `self.data.fun_bs_long_term_prepayments_annual_panel` |
| `fun_bs_long_term_prepayments_to_suppliers_annual_panel` | `self.data.fun_bs_long_term_prepayments_to_suppliers_annual_panel` |
| `fun_bs_long_term_receivables_annual_panel` | `self.data.fun_bs_long_term_receivables_annual_panel` |
| `fun_bs_long_term_trade_payables_annual_panel` | `self.data.fun_bs_long_term_trade_payables_annual_panel` |
| `fun_bs_long_term_trade_receivables_annual_panel` | `self.data.fun_bs_long_term_trade_receivables_annual_panel` |
| `fun_bs_margin_deposits_annual_panel` | `self.data.fun_bs_margin_deposits_annual_panel` |
| `fun_bs_mathematical_reserve_annual_panel` | `self.data.fun_bs_mathematical_reserve_annual_panel` |
| `fun_bs_minority_interests_annual_panel` | `self.data.fun_bs_minority_interests_annual_panel` |
| `fun_bs_other_current_assets_annual_panel` | `self.data.fun_bs_other_current_assets_annual_panel` |
| `fun_bs_other_current_assets_residual_annual_panel` | `self.data.fun_bs_other_current_assets_residual_annual_panel` |
| `fun_bs_other_funds_annual_panel` | `self.data.fun_bs_other_funds_annual_panel` |
| `fun_bs_other_long_term_assets_annual_panel` | `self.data.fun_bs_other_long_term_assets_annual_panel` |
| `fun_bs_other_long_term_assets_residual_annual_panel` | `self.data.fun_bs_other_long_term_assets_residual_annual_panel` |
| `fun_bs_other_long_term_investments_annual_panel` | `self.data.fun_bs_other_long_term_investments_annual_panel` |
| `fun_bs_other_long_term_payables_annual_panel` | `self.data.fun_bs_other_long_term_payables_annual_panel` |
| `fun_bs_other_long_term_receivables_annual_panel` | `self.data.fun_bs_other_long_term_receivables_annual_panel` |
| `fun_bs_other_long_term_receivables_residual_annual_panel` | `self.data.fun_bs_other_long_term_receivables_residual_annual_panel` |
| `fun_bs_other_payables_annual_panel` | `self.data.fun_bs_other_payables_annual_panel` |
| `fun_bs_other_receivable_from_customers_annual_panel` | `self.data.fun_bs_other_receivable_from_customers_annual_panel` |
| `fun_bs_other_receivables_annual_panel` | `self.data.fun_bs_other_receivables_annual_panel` |
| `fun_bs_other_reserves_annual_panel` | `self.data.fun_bs_other_reserves_annual_panel` |
| `fun_bs_other_short_term_payables_annual_panel` | `self.data.fun_bs_other_short_term_payables_annual_panel` |
| `fun_bs_other_short_term_prepayments_annual_panel` | `self.data.fun_bs_other_short_term_prepayments_annual_panel` |
| `fun_bs_other_taxes_receivable_annual_panel` | `self.data.fun_bs_other_taxes_receivable_annual_panel` |
| `fun_bs_owners_equity_annual_panel` | `self.data.fun_bs_owners_equity_annual_panel` |
| `fun_bs_owners_other_capital_annual_panel` | `self.data.fun_bs_owners_other_capital_annual_panel` |
| `fun_bs_paid_in_capital_annual_panel` | `self.data.fun_bs_paid_in_capital_annual_panel` |
| `fun_bs_payable_to_employees_annual_panel` | `self.data.fun_bs_payable_to_employees_annual_panel` |
| `fun_bs_payables_from_insurance_contract_annual_panel` | `self.data.fun_bs_payables_from_insurance_contract_annual_panel` |
| `fun_bs_payables_to_suppliers_annual_panel` | `self.data.fun_bs_payables_to_suppliers_annual_panel` |
| `fun_bs_ppe_finance_cost_annual_panel` | `self.data.fun_bs_ppe_finance_cost_annual_panel` |
| `fun_bs_ppe_tangible_cost_annual_panel` | `self.data.fun_bs_ppe_tangible_cost_annual_panel` |
| `fun_bs_preferred_shares_annual_panel` | `self.data.fun_bs_preferred_shares_annual_panel` |
| `fun_bs_preferred_shares_liabilities_annual_panel` | `self.data.fun_bs_preferred_shares_liabilities_annual_panel` |
| `fun_bs_prepayments_to_suppliers_annual_panel` | `self.data.fun_bs_prepayments_to_suppliers_annual_panel` |
| `fun_bs_provision_for_claim_from_outward_reinsurance_annual_panel` | `self.data.fun_bs_provision_for_claim_from_outward_reinsurance_annual_panel` |
| `fun_bs_provision_for_decline_in_inventories_annual_panel` | `self.data.fun_bs_provision_for_decline_in_inventories_annual_panel` |
| `fun_bs_provision_for_diminution_annual_panel` | `self.data.fun_bs_provision_for_diminution_annual_panel` |
| `fun_bs_provision_for_doubtful_debts_annual_panel` | `self.data.fun_bs_provision_for_doubtful_debts_annual_panel` |
| `fun_bs_provision_for_doubtful_lt_receivable_annual_panel` | `self.data.fun_bs_provision_for_doubtful_lt_receivable_annual_panel` |
| `fun_bs_provision_for_long_term_investments_annual_panel` | `self.data.fun_bs_provision_for_long_term_investments_annual_panel` |
| `fun_bs_provision_for_long_term_liabilities_annual_panel` | `self.data.fun_bs_provision_for_long_term_liabilities_annual_panel` |
| `fun_bs_provision_for_premium_outward_reinsurance_annual_panel` | `self.data.fun_bs_provision_for_premium_outward_reinsurance_annual_panel` |
| `fun_bs_provision_for_severance_allowances_annual_panel` | `self.data.fun_bs_provision_for_severance_allowances_annual_panel` |
| `fun_bs_provision_for_st_liabilities_annual_panel` | `self.data.fun_bs_provision_for_st_liabilities_annual_panel` |
| `fun_bs_receivable_from_insurance_contract_annual_panel` | `self.data.fun_bs_receivable_from_insurance_contract_annual_panel` |
| `fun_bs_reinsurance_assets_annual_panel` | `self.data.fun_bs_reinsurance_assets_annual_panel` |
| `fun_bs_short_term_financial_investments_annual_panel` | `self.data.fun_bs_short_term_financial_investments_annual_panel` |
| `fun_bs_short_term_investments_annual_panel` | `self.data.fun_bs_short_term_investments_annual_panel` |
| `fun_bs_short_term_loans_annual_panel` | `self.data.fun_bs_short_term_loans_annual_panel` |
| `fun_bs_short_term_loans_receivables_annual_panel` | `self.data.fun_bs_short_term_loans_receivables_annual_panel` |
| `fun_bs_short_term_prepayments_annual_panel` | `self.data.fun_bs_short_term_prepayments_annual_panel` |
| `fun_bs_short_term_unrealized_revenue_annual_panel` | `self.data.fun_bs_short_term_unrealized_revenue_annual_panel` |
| `fun_bs_shortage_of_current_assets_waiting_for_solution_annual_panel` | `self.data.fun_bs_shortage_of_current_assets_waiting_for_solution_annual_panel` |
| `fun_bs_statutory_reserve_annual_panel` | `self.data.fun_bs_statutory_reserve_annual_panel` |
| `fun_bs_tangible_assets_accum_depreciation_annual_panel` | `self.data.fun_bs_tangible_assets_accum_depreciation_annual_panel` |
| `fun_bs_tangible_fixed_assets_annual_panel` | `self.data.fun_bs_tangible_fixed_assets_annual_panel` |
| `fun_bs_taxes_and_other_payable_to_state_budget_annual_panel` | `self.data.fun_bs_taxes_and_other_payable_to_state_budget_annual_panel` |
| `fun_bs_technology_science_development_fund_annual_panel` | `self.data.fun_bs_technology_science_development_fund_annual_panel` |
| `fun_bs_total_assets_annual_panel` | `self.data.fun_bs_total_assets_annual_panel` |
| `fun_bs_total_resources_annual_panel` | `self.data.fun_bs_total_resources_annual_panel` |
| `fun_bs_trade_accounts_payable_annual_panel` | `self.data.fun_bs_trade_accounts_payable_annual_panel` |
| `fun_bs_trade_accounts_receivable_annual_panel` | `self.data.fun_bs_trade_accounts_receivable_annual_panel` |
| `fun_bs_treasury_shares_annual_panel` | `self.data.fun_bs_treasury_shares_annual_panel` |
| `fun_bs_undistributed_commission_expenses_annual_panel` | `self.data.fun_bs_undistributed_commission_expenses_annual_panel` |
| `fun_bs_undistributed_earnings_annual_panel` | `self.data.fun_bs_undistributed_earnings_annual_panel` |
| `fun_bs_unearned_commission_income_annual_panel` | `self.data.fun_bs_unearned_commission_income_annual_panel` |
| `fun_bs_unearned_premium_reserve_annual_panel` | `self.data.fun_bs_unearned_premium_reserve_annual_panel` |

## Cash Flow (Quarterly)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_cf_amortisation_of_goodwill_quarterly_panel` | `self.data.fun_cf_amortisation_of_goodwill_quarterly_panel` |
| `fun_cf_business_income_tax_paid_quarterly_panel` | `self.data.fun_cf_business_income_tax_paid_quarterly_panel` |
| `fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_quarterly_panel` | `self.data.fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_quarterly_panel` |
| `fun_cf_cash_and_cash_equivalents_at_the_end_of_period_quarterly_panel` | `self.data.fun_cf_cash_and_cash_equivalents_at_the_end_of_period_quarterly_panel` |
| `fun_cf_cash_returned_for_investors_and_mof_from_additional_paid_in_cap_quarterly_panel` | `self.data.fun_cf_cash_returned_for_investors_and_mof_from_additional_paid_in_cap_quarterly_panel` |
| `fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_quarterly_panel` | `self.data.fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_quarterly_panel` |
| `fun_cf_depreciation_and_amortisation_quarterly_panel` | `self.data.fun_cf_depreciation_and_amortisation_quarterly_panel` |
| `fun_cf_dividends_and_interest_received_quarterly_panel` | `self.data.fun_cf_dividends_and_interest_received_quarterly_panel` |
| `fun_cf_dividends_paid_quarterly_panel` | `self.data.fun_cf_dividends_paid_quarterly_panel` |
| `fun_cf_effect_of_foreign_exchange_differences_quarterly_panel` | `self.data.fun_cf_effect_of_foreign_exchange_differences_quarterly_panel` |
| `fun_cf_finance_lease_principal_payments_quarterly_panel` | `self.data.fun_cf_finance_lease_principal_payments_quarterly_panel` |
| `fun_cf_increase_decrease_in_inventories_quarterly_panel` | `self.data.fun_cf_increase_decrease_in_inventories_quarterly_panel` |
| `fun_cf_increase_decrease_in_payables_quarterly_panel` | `self.data.fun_cf_increase_decrease_in_payables_quarterly_panel` |
| `fun_cf_increase_decrease_in_prepaid_expenses_quarterly_panel` | `self.data.fun_cf_increase_decrease_in_prepaid_expenses_quarterly_panel` |
| `fun_cf_increase_decrease_in_receivables_quarterly_panel` | `self.data.fun_cf_increase_decrease_in_receivables_quarterly_panel` |
| `fun_cf_increase_decrease_in_trading_securities_quarterly_panel` | `self.data.fun_cf_increase_decrease_in_trading_securities_quarterly_panel` |
| `fun_cf_interest_expense_quarterly_panel` | `self.data.fun_cf_interest_expense_quarterly_panel` |
| `fun_cf_interest_income_and_dividend_quarterly_panel` | `self.data.fun_cf_interest_income_and_dividend_quarterly_panel` |
| `fun_cf_interest_paid_quarterly_panel` | `self.data.fun_cf_interest_paid_quarterly_panel` |
| `fun_cf_investments_in_other_entities_quarterly_panel` | `self.data.fun_cf_investments_in_other_entities_quarterly_panel` |
| `fun_cf_loans_granted_purchases_of_debt_instruments_quarterly_panel` | `self.data.fun_cf_loans_granted_purchases_of_debt_instruments_quarterly_panel` |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_quarterly_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_financing_activities_quarterly_panel` |
| `fun_cf_net_cash_inflows_outflows_from_investing_activities_quarterly_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_investing_activities_quarterly_panel` |
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_quarterly_panel` |
| `fun_cf_net_increase_in_cash_and_cash_equivalents_quarterly_panel` | `self.data.fun_cf_net_increase_in_cash_and_cash_equivalents_quarterly_panel` |
| `fun_cf_net_profit_loss_before_tax_quarterly_panel` | `self.data.fun_cf_net_profit_loss_before_tax_quarterly_panel` |
| `fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel` | `self.data.fun_cf_operating_profit_loss_before_changes_in_wc_quarterly_panel` |
| `fun_cf_other_adjustments_quarterly_panel` | `self.data.fun_cf_other_adjustments_quarterly_panel` |
| `fun_cf_other_payments_on_operating_activities_quarterly_panel` | `self.data.fun_cf_other_payments_on_operating_activities_quarterly_panel` |
| `fun_cf_other_receipts_from_operating_activities_quarterly_panel` | `self.data.fun_cf_other_receipts_from_operating_activities_quarterly_panel` |
| `fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel` | `self.data.fun_cf_payments_for_share_returns_and_repurchases_quarterly_panel` |
| `fun_cf_proceeds_from_borrowings_quarterly_panel` | `self.data.fun_cf_proceeds_from_borrowings_quarterly_panel` |
| `fun_cf_proceeds_from_disposal_of_fixed_assets_quarterly_panel` | `self.data.fun_cf_proceeds_from_disposal_of_fixed_assets_quarterly_panel` |
| `fun_cf_proceeds_from_divestment_in_other_entities_quarterly_panel` | `self.data.fun_cf_proceeds_from_divestment_in_other_entities_quarterly_panel` |
| `fun_cf_proceeds_from_issue_of_shares_quarterly_panel` | `self.data.fun_cf_proceeds_from_issue_of_shares_quarterly_panel` |
| `fun_cf_profit_loss_from_investing_activities_quarterly_panel` | `self.data.fun_cf_profit_loss_from_investing_activities_quarterly_panel` |
| `fun_cf_profit_loss_from_liquidating_fixed_activities_quarterly_panel` | `self.data.fun_cf_profit_loss_from_liquidating_fixed_activities_quarterly_panel` |
| `fun_cf_profit_loss_from_liquidating_fixed_assets_quarterly_panel` | `self.data.fun_cf_profit_loss_from_liquidating_fixed_assets_quarterly_panel` |
| `fun_cf_provisions_quarterly_panel` | `self.data.fun_cf_provisions_quarterly_panel` |
| `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel` | `self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_quarterly_panel` |
| `fun_cf_repayment_of_borrowings_quarterly_panel` | `self.data.fun_cf_repayment_of_borrowings_quarterly_panel` |
| `fun_cf_sums_received_in_trust_quarterly_panel` | `self.data.fun_cf_sums_received_in_trust_quarterly_panel` |
| `fun_cf_unrealised_foreign_exchange_gain_loss_quarterly_panel` | `self.data.fun_cf_unrealised_foreign_exchange_gain_loss_quarterly_panel` |

## Cash Flow (Annual)

| Field | Usage (cross_sectional) |
|---|---|
| `fun_cf_amortisation_of_goodwill_annual_panel` | `self.data.fun_cf_amortisation_of_goodwill_annual_panel` |
| `fun_cf_business_income_tax_paid_annual_panel` | `self.data.fun_cf_business_income_tax_paid_annual_panel` |
| `fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_annual_panel` | `self.data.fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_annual_panel` |
| `fun_cf_cash_and_cash_equivalents_at_the_end_of_period_annual_panel` | `self.data.fun_cf_cash_and_cash_equivalents_at_the_end_of_period_annual_panel` |
| `fun_cf_cash_returned_for_investors_and_mof_from_additional_paid_in_cap_annual_panel` | `self.data.fun_cf_cash_returned_for_investors_and_mof_from_additional_paid_in_cap_annual_panel` |
| `fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_annual_panel` | `self.data.fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_annual_panel` |
| `fun_cf_depreciation_and_amortisation_annual_panel` | `self.data.fun_cf_depreciation_and_amortisation_annual_panel` |
| `fun_cf_dividends_and_interest_received_annual_panel` | `self.data.fun_cf_dividends_and_interest_received_annual_panel` |
| `fun_cf_dividends_paid_annual_panel` | `self.data.fun_cf_dividends_paid_annual_panel` |
| `fun_cf_effect_of_foreign_exchange_differences_annual_panel` | `self.data.fun_cf_effect_of_foreign_exchange_differences_annual_panel` |
| `fun_cf_finance_lease_principal_payments_annual_panel` | `self.data.fun_cf_finance_lease_principal_payments_annual_panel` |
| `fun_cf_increase_decrease_in_inventories_annual_panel` | `self.data.fun_cf_increase_decrease_in_inventories_annual_panel` |
| `fun_cf_increase_decrease_in_payables_annual_panel` | `self.data.fun_cf_increase_decrease_in_payables_annual_panel` |
| `fun_cf_increase_decrease_in_prepaid_expenses_annual_panel` | `self.data.fun_cf_increase_decrease_in_prepaid_expenses_annual_panel` |
| `fun_cf_increase_decrease_in_receivables_annual_panel` | `self.data.fun_cf_increase_decrease_in_receivables_annual_panel` |
| `fun_cf_increase_decrease_in_trading_securities_annual_panel` | `self.data.fun_cf_increase_decrease_in_trading_securities_annual_panel` |
| `fun_cf_interest_expense_annual_panel` | `self.data.fun_cf_interest_expense_annual_panel` |
| `fun_cf_interest_income_and_dividend_annual_panel` | `self.data.fun_cf_interest_income_and_dividend_annual_panel` |
| `fun_cf_interest_paid_annual_panel` | `self.data.fun_cf_interest_paid_annual_panel` |
| `fun_cf_investments_in_other_entities_annual_panel` | `self.data.fun_cf_investments_in_other_entities_annual_panel` |
| `fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel` | `self.data.fun_cf_loans_granted_purchases_of_debt_instruments_annual_panel` |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_annual_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_financing_activities_annual_panel` |
| `fun_cf_net_cash_inflows_outflows_from_investing_activities_annual_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_investing_activities_annual_panel` |
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel` | `self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel` |
| `fun_cf_net_increase_in_cash_and_cash_equivalents_annual_panel` | `self.data.fun_cf_net_increase_in_cash_and_cash_equivalents_annual_panel` |
| `fun_cf_net_profit_loss_before_tax_annual_panel` | `self.data.fun_cf_net_profit_loss_before_tax_annual_panel` |
| `fun_cf_operating_profit_loss_before_changes_in_wc_annual_panel` | `self.data.fun_cf_operating_profit_loss_before_changes_in_wc_annual_panel` |
| `fun_cf_other_adjustments_annual_panel` | `self.data.fun_cf_other_adjustments_annual_panel` |
| `fun_cf_other_payments_on_operating_activities_annual_panel` | `self.data.fun_cf_other_payments_on_operating_activities_annual_panel` |
| `fun_cf_other_receipts_from_operating_activities_annual_panel` | `self.data.fun_cf_other_receipts_from_operating_activities_annual_panel` |
| `fun_cf_payments_for_share_returns_and_repurchases_annual_panel` | `self.data.fun_cf_payments_for_share_returns_and_repurchases_annual_panel` |
| `fun_cf_proceeds_from_borrowings_annual_panel` | `self.data.fun_cf_proceeds_from_borrowings_annual_panel` |
| `fun_cf_proceeds_from_disposal_of_fixed_assets_annual_panel` | `self.data.fun_cf_proceeds_from_disposal_of_fixed_assets_annual_panel` |
| `fun_cf_proceeds_from_divestment_in_other_entities_annual_panel` | `self.data.fun_cf_proceeds_from_divestment_in_other_entities_annual_panel` |
| `fun_cf_proceeds_from_issue_of_shares_annual_panel` | `self.data.fun_cf_proceeds_from_issue_of_shares_annual_panel` |
| `fun_cf_profit_loss_from_investing_activities_annual_panel` | `self.data.fun_cf_profit_loss_from_investing_activities_annual_panel` |
| `fun_cf_profit_loss_from_liquidating_fixed_activities_annual_panel` | `self.data.fun_cf_profit_loss_from_liquidating_fixed_activities_annual_panel` |
| `fun_cf_profit_loss_from_liquidating_fixed_assets_annual_panel` | `self.data.fun_cf_profit_loss_from_liquidating_fixed_assets_annual_panel` |
| `fun_cf_provisions_annual_panel` | `self.data.fun_cf_provisions_annual_panel` |
| `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel` | `self.data.fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_annual_panel` |
| `fun_cf_repayment_of_borrowings_annual_panel` | `self.data.fun_cf_repayment_of_borrowings_annual_panel` |
| `fun_cf_sums_received_in_trust_annual_panel` | `self.data.fun_cf_sums_received_in_trust_annual_panel` |


## Usage Notes

- `self.data.*` is the raw data layer. Do not invent extra field names in generated code.
- In `time_series` mode use the suffix-less form; in `cross_sectional` mode use the `_panel` form. Never mix.
- Fundamentals are point-in-time: aligned to publication date, carried forward until a newer report.
- Treat missing fundamentals as unavailable (`.notna()`), not as zero.
- Use ratios when comparing companies of different sizes; require a positive denominator.
- Banks, insurers, securities firms, and non-financial firms use different accounting conventions — do not assume one raw ratio is comparable across industries.
