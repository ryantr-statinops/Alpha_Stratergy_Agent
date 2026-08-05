# DATA GROUP COMBINATIONS — 16 Nhom Hoan Chinh

> Date: 2026-08-05
> Reference: `syntax/data_syntax.md` (496 fields), `MASTER_alpha_planning.md`
> Mode: `cross_sectional` (`_panel`, `set_portfolio_positions`)

---

## 16 Nhom Hoan Chinh

### A — Price & Volume (daily)

| Field | Role |
|---|---|
| `pv_close_panel` | Price level, market value (x common_shares from K) |
| `pv_open_panel` | Gap signals |
| `pv_high_panel` | ATR, VWAP, range |
| `pv_low_panel` | ATR, VWAP, range |
| `pv_volume_panel` | Liquidity, Amihud, volume signals |
| `pv_vn30_close_panel` | Market reference, beta |
| `pv_vn30_open_panel` | VN30 gap |
| `pv_vn30_high_panel` | VN30 range |
| `pv_vn30_low_panel` | VN30 range |
| `pv_vn30_volume_panel` | Market volume reference |

**Role:** Signal + denominator chinh (market_value = close x common_shares). Moi alpha deu can A.

---

### B — Profitability (Income Q/A)

| Field | Role |
|---|---|
| `fun_is_net_profit_loss_after_tax_*_panel` | Core profit, ROA/ROE numerator |
| `fun_is_net_accounting_profit_loss_before_tax_*_panel` | Pre-tax profit, interest coverage |
| `fun_is_profit_from_financial_activities_*_panel` | Financial income decomposition |
| `fun_is_net_operating_income_from_other_activities_*_panel` | Non-core operating income |
| `fun_is_other_income_*_panel` | Other income |
| `fun_is_net_other_income_expenses_*_panel` | Net other income/expenses |
| `fun_is_gain_loss_from_joint_ventures_*_panel` | JV contribution |

**Role:** Tu so cho ROA/ROE, profit quality signal.

---

### C — Cost & Margin (Income Q)

| Field | Role |
|---|---|
| `fun_is_selling_expenses_quarterly_panel` | Selling cost discipline |
| `fun_is_general_and_admin_expenses_quarterly_panel` | G&A cost discipline |
| `fun_is_financial_income_quarterly_panel` | Interest income decomposition |
| `fun_is_financial_expenses_quarterly_panel` | Interest expense |
| `fun_is_total_compensation_quarterly_panel` | Labor cost |
| `fun_is_compensation_quarterly_panel` | Direct compensation |
| `fun_is_expenses_from_other_activities_quarterly_panel` | Non-core expenses |
| `fun_is_other_expenses_quarterly_panel` | Other expenses |
| `fun_is_other_deductions_quarterly_panel` | Other deductions |

**Role:** Cost discipline, interest coverage, core-margin signal. Q优先因为粒度细.

---

### D — EPS & Attribution (Income Q/A)

| Field | Role |
|---|---|
| `fun_is_eps_basis_*_panel` | EPS yield, EPS surprise |
| `fun_is_attributable_to_parent_company_*_panel` | Parent-company EPS |
| `fun_is_minority_interests_*_panel` | Minority drag |

**Role:** EPS yield, minority adjustment. Dung chung voi K (common_shares) de tinh EPS/market value.

---

### E — Tax & Reserves (Income Q/A)

| Field | Role |
|---|---|
| `fun_is_business_income_tax_current_*_panel` | Current tax |
| `fun_is_business_income_tax_deferred_*_panel` | Deferred tax |
| `fun_is_equalisation_reserve_*_panel` | Insurance tax smoothing |
| `fun_is_provision_for_catastrophe_reserve_*_panel` | Catastrophe reserve |
| `fun_is_other_deductions_*_panel` | Other deductions |

**Role:** Tax stability, effective tax, reserves quality.

---

### F — Capital Structure (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_total_assets_*_panel` | Size, ROA denominator, quality gate |
| `fun_bs_owners_equity_*_panel` | ROE denominator, leverage |
| `fun_bs_liabilities_*_panel` | Total debt |
| `fun_bs_total_resources_*_panel` | Total resources |
| `fun_bs_long_term_liabilities_*_panel` | Long-term debt |
| `fun_bs_capital_and_researves_*_panel` | Capital base |
| `fun_bs_minority_interests_*_panel` | Minority interests |

**Role:** Denominator chinh (ROA, ROE, leverage). Quality gate: equity/assets > 0.15.

---

### G — Cash & Liquidity (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_cash_*_panel` | Cash |
| `fun_bs_cash_equivalents_*_panel` | Cash equivalents |
| `fun_bs_cash_and_cash_equivalents_*_panel` | Total cash position |
| `fun_bs_short_term_investments_*_panel` | Liquid investments |
| `fun_bs_short_term_financial_investments_*_panel` | Short-term financial investments |
| `fun_bs_current_assets_*_panel` | Current assets |
| `fun_bs_current_liabilities_*_panel` | Current liabilities |

**Role:** Cash buffer, current ratio, net cash signal.

---

### H — Working Capital (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_inventories_*_panel` | Inventory |
| `fun_bs_inventories_net_*_panel` | Net inventory |
| `fun_bs_trade_accounts_receivable_*_panel` | Trade receivables |
| `fun_bs_trade_accounts_payable_*_panel` | Trade payables |
| `fun_bs_accounts_receivable_*_panel` | Other receivables |
| `fun_bs_advances_*_panel` | Advances |
| `fun_bs_advances_from_customers_*_panel` | Customer advances |
| `fun_bs_prepayments_to_suppliers_*_panel` | Prepayments |
| `fun_bs_other_receivables_*_panel` | Other receivables |
| `fun_bs_short_term_loans_*_panel` | Short-term loans (liability) |

**Role:** WC quality, inventory/receivables deterioration, supplier credit, lean-WC signal.

---

### I — Long-term Assets (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_tangible_fixed_assets_*_panel` | Tangible FA |
| `fun_bs_intangible_fixed_assets_*_panel` | Intangible FA |
| `fun_bs_construction_in_progress_*_panel` | CIP (idle capital risk) |
| `fun_bs_good_will_*_panel` | Goodwill |
| `fun_bs_investment_properties_*_panel` | Investment property |
| `fun_bs_finance_lease_assets_*_panel` | Finance lease assets |
| `fun_bs_ppe_tangible_cost_*_panel` | PPE cost |

**Role:** Capital productivity, CIP risk, intangible burden.

---

### J — Investments (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_long_term_investments_*_panel` | Long-term investments |
| `fun_bs_investments_in_subsidiaries_*_panel` | Subsidiary investments |
| `fun_bs_investments_in_associates_*_panel` | Associate investments |
| `fun_bs_held_to_maturity_investment_current_*_panel` | HTM (current) |
| `fun_bs_held_to_maturity_investment_non_current_*_panel` | HTM (non-current) |
| `fun_bs_long_term_loans_*_panel` | Long-term loans (receivable) |
| `fun_bs_short_term_loans_receivables_*_panel` | Short-term loans (receivable) |
| `fun_bs_long_term_receivables_*_panel` | Long-term receivables |

**Role:** Investment intensity, conglomerate structure, financial firm identification.

---

### K — Equity Structure (Balance Sheet Q/A)

| Field | Role |
|---|---|
| `fun_bs_paid_in_capital_*_panel` | Paid-in capital |
| `fun_bs_common_shares_*_panel` | Common shares (for market value) |
| `fun_bs_treasury_shares_*_panel` | Treasury shares (negative) |
| `fun_bs_undistributed_earnings_*_panel` | Retained earnings |
| `fun_bs_capital_surplus_*_panel` | Capital surplus |
| `fun_bs_preferred_shares_*_panel` | Preferred shares |
| `fun_bs_bonus_and_welfare_funds_*_panel` | Bonus/welfare funds |
| `fun_bs_statutory_reserve_*_panel` | Statutory reserve |
| `fun_bs_investment_and_development_funds_*_panel` | Investment/dev funds |

**Role:** Dilution signal, book quality, common_shares cho market value calculation.

---

### L — Financial Institution Identifiers (BS/CF — mask-only)

| Field | Source | Role |
|---|---|---|
| `fun_bs_insurance_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_unearned_premium_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_mathematical_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_claim_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_catastrophe_reserve_*_panel` | BS | Insurance intensity |
| `fun_bs_margin_deposits_*_panel` | BS | Securities intensity |
| `fun_bs_reinsurance_assets_*_panel` | BS | Reinsurance intensity |
| `fun_bs_insurance_deposits_*_panel` | BS | Insurance deposits |
| `fun_bs_payables_from_insurance_contract_*_panel` | BS | Insurance payables |
| `fun_bs_receivable_from_insurance_contract_*_panel` | BS | Insurance receivables |
| `fun_bs_government_bonds_purchased_for_resale_receivable_*_panel` | BS | Gov bond trading |
| `fun_bs_government_bonds_purchased_for_resale_payable_*_panel` | BS | Gov bond trading |
| `fun_bs_equalization_reserves_*_panel` | BS | Equalisation reserve |
| `fun_cf_loans_granted_purchases_of_debt_instruments_*_panel` | CF | Loans granted |
| `fun_cf_collection_of_loans_proceeds_from_sales_of_debts_instruments_*_panel` | CF | Loan collection |

**Role:** Chi dung cho MASK L2 (financial flag). Khong dung lam signal.

---

### M — Operating Cash Flow (Q/A)

| Field | Role |
|---|---|
| `fun_cf_net_cash_inflows_outflows_from_operating_activities_*_panel` | CFO |
| `fun_cf_operating_profit_loss_before_changes_in_wc_*_panel` | CFO before WC |
| `fun_cf_business_income_tax_paid_*_panel` | Tax paid |
| `fun_cf_interest_paid_*_panel` | Interest paid |
| `fun_cf_interest_income_and_dividend_*_panel` | Interest/dividend received |
| `fun_cf_dividends_and_interest_received_*_panel` | Dividends + interest received |
| `fun_cf_other_receipts_from_operating_activities_*_panel` | Other receipts |
| `fun_cf_other_payments_on_operating_activities_*_panel` | Other payments |
| `fun_cf_depreciation_and_amortisation_*_panel` | Depreciation (non-cash add-back) |
| `fun_cf_provisions_*_panel` | Provisions |

**Role:** CFO quality, cash conversion, FCF proxy.

---

### N — Investing Cash Flow (Q/A)

| Field | Role |
|---|---|
| `fun_cf_purchases_of_fixed_assets_and_other_long_term_assets_*_panel` | Capex |
| `fun_cf_proceeds_from_disposal_of_fixed_assets_*_panel` | Disposal proceeds |
| `fun_cf_investments_in_other_entities_*_panel` | Investments in others |
| `fun_cf_proceeds_from_divestment_in_other_entities_*_panel` | Divestment proceeds |
| `fun_cf_profit_loss_from_investing_activities_*_panel` | Investment P&L |
| `fun_cf_profit_loss_from_liquidating_fixed_activities_*_panel` | Liquidation P&L |
| `fun_cf_profit_loss_from_liquidating_fixed_assets_*_panel` | Asset liquidation |

**Role:** Capex intensity, investment discipline, FCF = CFO - capex.

---

### O — Financing Cash Flow (Q/A)

| Field | Role |
|---|---|
| `fun_cf_dividends_paid_*_panel` | Dividends (outflow <= 0) |
| `fun_cf_proceeds_from_issue_of_shares_*_panel` | Share issuance (inflow > 0) |
| `fun_cf_payments_for_share_returns_and_repurchases_*_panel` | Repurchases (outflow <= 0) |
| `fun_cf_proceeds_from_borrowings_*_panel` | Borrowings proceeds |
| `fun_cf_repayment_of_borrowings_*_panel` | Borrowings repayment |
| `fun_cf_finance_lease_principal_payments_*_panel` | Lease payments |
| `fun_cf_cash_returned_for_investors_and_mof_from_additional_paid_in_cap_*_panel` | Cash returned to investors |
| `fun_cf_net_cash_inflows_outflows_from_financing_activities_*_panel` | Net financing CF |

**Role:** Net payout = -(dividends) - (repurchases) - issuance. External dependence. Dividend sustainability.

---

### P — Cash Reconciliation (Q/A)

| Field | Role |
|---|---|
| `fun_cf_net_increase_in_cash_and_cash_equivalents_*_panel` | Net cash change |
| `fun_cf_cash_and_cash_equivalents_at_the_beginning_of_period_*_panel` | Beginning cash |
| `fun_cf_cash_and_cash_equivalents_at_the_end_of_period_*_panel` | Ending cash |
| `fun_cf_effect_of_foreign_exchange_differences_*_panel` | FX effect |
| `fun_cf_unrealised_foreign_exchange_gain_loss_*_panel` | Unrealised FX |
| `fun_cf_amortisation_of_goodwill_*_panel` | Goodwill amortisation |
| `fun_cf_other_adjustments_*_panel` | Other adjustments |
| `fun_cf_increase_decrease_in_inventories_*_panel` | WC: inventories change |
| `fun_cf_increase_decrease_in_receivables_*_panel` | WC: receivables change |
| `fun_cf_increase_decrease_in_payables_*_panel` | WC: payables change |
| `fun_cf_increase_decrease_in_prepaid_expenses_*_panel` | WC: prepayments change |
| `fun_cf_increase_decrease_in_trading_securities_*_panel` | Trading securities change |
| `fun_cf_interest_expense_*_panel` | Interest expense (CF reconciliation) |
| `fun_cf_sums_received_in_trust_*_panel` | Trust receipts |

**Role:** Data quality validation, cash bridge, WC reconciliation. Khong dung lam signal truc tiep.

---

## Tier Roles

### Denominator providers
| Group | Provides |
|---|---|
| A (Price/Volume) | market_value = close x common_shares |
| F (Capital Structure) | total_assets, owners_equity (ROA/ROE denominator) |
| K (Equity Structure) | common_shares (share count for market value) |

### Signal providers
| Group | Typical signal |
|---|---|
| B (Profitability) | ROA, ROE, core profit |
| C (Cost & Margin) | Cost discipline, interest coverage |
| D (EPS & Attribution) | EPS yield, minority drag |
| E (Tax & Reserves) | Effective tax, tax stability |
| G (Cash & Liquidity) | Cash-to-assets, current ratio |
| H (Working Capital) | Lean WC, inventory/receivables quality |
| I (Long-term Assets) | Capital productivity, intangible burden |
| J (Investments) | Investment intensity, conglomerate |
| M (Operating CF) | CFO yield, cash conversion |
| N (Investing CF) | Capex intensity, FCF |
| O (Financing CF) | Net payout, external dependence |

### Mask-only
| Group | Mask role |
|---|---|
| L (Financial ID) | financial flag: insurance/unearned/loans/margin > threshold |

### Validation-only
| Group | Validation role |
|---|---|
| P (Cash Reconciliation) | Cash bridge, WC reconciliation, data quality check |

---

## 120 Pairs (C(16,2))

| # | G1 | G2 | Economic Mechanism | Example Feature | Valid |
|---|---|---|---|---|---|
| 1 | A | B | Price x Profitability | ROA = NI/TA, EPS yield = NI/CS/Close | V |
| 2 | A | C | Price x Cost | Cost-to-market ratio | V |
| 3 | A | D | Price x EPS | EPS yield = EPS/Close, minority-adjusted yield | V |
| 4 | A | E | Price x Tax | After-tax earnings yield | V |
| 5 | A | F | Price x Capital Structure | P/B = Close/(Equity/CS), P/E = Close/EPS | V |
| 6 | A | G | Price x Cash & Liquidity | Cash-to-price, liquidity premium | V |
| 7 | A | H | Price x Working Capital | WC-to-market, lean-WC signal | V |
| 8 | A | I | Price x Long-term Assets | Capital productivity = NI/TA, asset-heavy signal | V |
| 9 | A | J | Price x Investments | Investment-to-market, conglomerate discount | V |
| 10 | A | K | Price x Equity Structure | market_value = close x common_shares | V |
| 11 | A | L | Price x Financial ID | Financial firm universe filter (mask) | C |
| 12 | A | M | Price x Operating CF | CFO yield = CFO/market_value | V |
| 13 | A | N | Price x Investing CF | Capex-to-market, investment intensity | V |
| 14 | A | O | Price x Financing CF | Net payout yield | V |
| 15 | A | P | Price x Cash Reconciliation | Cash bridge validation | C |
| 16 | B | C | Profitability x Cost | Core margin = (NI + FE - FI)/TA | V |
| 17 | B | D | Profitability x EPS | EPS quality = NI vs EPS attribution | V |
| 18 | B | E | Profitability x Tax | Effective tax rate = tax/PBT | V |
| 19 | B | F | Profitability x Capital Structure | ROA = NI/TA, ROE = NI/Equity | V |
| 20 | B | G | Profitability x Cash & Liquidity | Cash conversion = CFO/NI, earnings quality | V |
| 21 | B | H | Profitability x Working Capital | WC efficiency = NI/Receivables | V |
| 22 | B | I | Profitability x Long-term Assets | Fixed asset efficiency = NI/TA | V |
| 23 | B | J | Profitability x Investments | Investment return, subsidiary contribution | V |
| 24 | B | K | Profitability x Equity Structure | EPS = NI/common_shares | V |
| 25 | B | L | Profitability x Financial ID | Insurance profit quality, claims ratio | C |
| 26 | B | M | Profitability x Operating CF | Cash conversion = CFO/NI | V |
| 27 | B | N | Profitability x Investing CF | Investment return quality | V |
| 28 | B | O | Profitability x Financing CF | Dividend payout ratio = Div/NI | V |
| 29 | B | P | Profitability x Cash Reconciliation | Earnings reconciliation | C |
| 30 | C | D | Cost x EPS | Cost impact on EPS | V |
| 31 | C | E | Cost x Tax | Cost discipline vs tax burden | V |
| 32 | C | F | Cost x Capital Structure | Cost-to-assets, cost efficiency | V |
| 33 | C | G | Cost x Cash & Liquidity | Cash cost ratio | V |
| 34 | C | H | Cost x Working Capital | Operating cost vs WC efficiency | V |
| 35 | C | I | Cost x Long-term Assets | G&A to fixed assets, cost structure | V |
| 36 | C | J | Cost x Investments | Financial income vs investment holdings | V |
| 37 | C | K | Cost x Equity Structure | Cost per share impact | V |
| 38 | C | L | Cost x Financial ID | Insurance cost structure | C |
| 39 | C | M | Cost x Operating CF | Cost-to-CFO, interest paid | V |
| 40 | C | N | Cost x Investing CF | Cost vs capex | V |
| 41 | C | O | Cost x Financing CF | Financial expense vs borrowings | V |
| 42 | C | P | Cost x Cash Reconciliation | Cost reconciliation | C |
| 43 | D | E | EPS x Tax | After-tax EPS quality | V |
| 44 | D | F | EPS x Capital Structure | EPS = NI/CS, leverage impact | V |
| 45 | D | G | EPS x Cash & Liquidity | Cash-backed EPS | V |
| 46 | D | H | EPS x Working Capital | WC quality vs EPS persistence | V |
| 47 | D | I | EPS x Long-term Assets | EPS from asset efficiency | V |
| 48 | D | J | EPS x Investments | Investment contribution to EPS | V |
| 49 | D | K | EPS x Equity Structure | Dilution impact on EPS | V |
| 50 | D | L | EPS x Financial ID | Insurance EPS quality | C |
| 51 | D | M | EPS x Operating CF | Cash EPS = CFO/CS | V |
| 52 | D | N | EPS x Investing CF | Investment gains in EPS | V |
| 53 | D | O | EPS x Financing CF | EPS vs dividend payout | V |
| 54 | D | P | EPS x Cash Reconciliation | EPS reconciliation | C |
| 55 | E | F | Tax x Capital Structure | Tax-to-assets, tax burden | V |
| 56 | E | G | Tax x Cash & Liquidity | Tax paid vs cash buffer | V |
| 57 | E | H | Tax x Working Capital | Tax deferred vs WC | V |
| 58 | E | I | Tax x Long-term Assets | Tax shield (depreciation) | V |
| 59 | E | J | Tax x Investments | Tax efficiency of investments | V |
| 60 | E | K | Tax x Equity Structure | Tax per share | V |
| 61 | E | L | Tax x Financial ID | Insurance tax (equalisation, catastrophe) | C |
| 62 | E | M | Tax x Operating CF | Tax paid vs CFO | V |
| 63 | E | N | Tax x Investing CF | Tax on investment gains | V |
| 64 | E | O | Tax x Financing CF | Tax shield on debt | V |
| 65 | E | P | Tax x Cash Reconciliation | Tax reconciliation | C |
| 66 | F | G | Capital Structure x Cash & Liquidity | Cash-to-assets, net debt | V |
| 67 | F | H | Capital Structure x Working Capital | Leverage vs WC, debt coverage | V |
| 68 | F | I | Capital Structure x Long-term Assets | Fixed asset financing | V |
| 69 | F | J | Capital Structure x Investments | Investment financing | V |
| 70 | F | K | Capital Structure x Equity Structure | Equity composition, book value | V |
| 71 | F | L | Capital Structure x Financial ID | Insurance reserves vs equity | C |
| 72 | F | M | Capital Structure x Operating CF | Debt coverage = CFO/Debt | V |
| 73 | F | N | Capital Structure x Investing CF | Investment funded by debt | V |
| 74 | F | O | Capital Structure x Financing CF | Debt dynamics | V |
| 75 | F | P | Capital Structure x Cash Reconciliation | Balance sheet reconciliation | C |
| 76 | G | H | Cash & Liquidity x Working Capital | Cash vs WC, lean WC | V |
| 77 | G | I | Cash & Liquidity x Long-term Assets | Cash vs fixed assets | V |
| 78 | G | J | Cash & Liquidity x Investments | Cash vs investments | V |
| 79 | G | K | Cash & Liquidity x Equity Structure | Cash per share | V |
| 80 | G | L | Cash & Liquidity x Financial ID | Insurance cash vs reserves | C |
| 81 | G | M | Cash & Liquidity x Operating CF | Cash build from operations | V |
| 82 | G | N | Cash & Liquidity x Investing CF | Cash used in investments | V |
| 83 | G | O | Cash & Liquidity x Financing CF | Cash returned to investors | V |
| 84 | G | P | Cash & Liquidity x Cash Reconciliation | Cash bridge validation | C |
| 85 | H | I | Working Capital x Long-term Assets | Total asset efficiency | V |
| 86 | H | J | Working Capital x Investments | WC vs investment holdings | V |
| 87 | H | K | Working Capital x Equity Structure | WC per share | V |
| 88 | H | L | Working Capital x Financial ID | Insurance WC structure | C |
| 89 | H | M | Working Capital x Operating CF | WC changes in CFO | V |
| 90 | H | N | Working Capital x Investing CF | Receivables from investments | V |
| 91 | H | O | Working Capital x Financing CF | WC funded by borrowings | V |
| 92 | H | P | Working Capital x Cash Reconciliation | WC reconciliation | C |
| 93 | I | J | Long-term Assets x Investments | Total investment holdings | V |
| 94 | I | K | Long-term Assets x Equity Structure | Asset backing per share | V |
| 95 | I | L | Long-term Assets x Financial ID | Insurance assets vs reserves | C |
| 96 | I | M | Long-term Assets x Operating CF | Depreciation in CFO | V |
| 97 | I | N | Long-term Assets x Investing CF | Capex vs disposal | V |
| 98 | I | O | Long-term Assets x Financing CF | Asset acquisition via debt | V |
| 99 | I | P | Long-term Assets x Cash Reconciliation | Asset reconciliation | C |
| 100 | J | K | Investments x Equity Structure | Investment per share | V |
| 101 | J | L | Investments x Financial ID | Insurance investment vs reserves | C |
| 102 | J | M | Investments x Operating CF | Investment income in CFO | V |
| 103 | J | N | Investments x Investing CF | Investment flows | V |
| 104 | J | O | Investments x Financing CF | Investment funded by debt | V |
| 105 | J | P | Investments x Cash Reconciliation | Investment reconciliation | C |
| 106 | K | L | Equity Structure x Financial ID | Insurance equity composition | C |
| 107 | K | M | Equity Structure x Operating CF | Book value vs cash flow | V |
| 108 | K | N | Equity Structure x Investing CF | Equity vs capex | V |
| 109 | K | O | Equity Structure x Financing CF | Equity vs dividend | V |
| 110 | K | P | Equity Structure x Cash Reconciliation | Equity reconciliation | C |
| 111 | L | M | Financial ID x Operating CF | Insurance CF quality | C |
| 112 | L | N | Financial ID x Investing CF | Insurance investment flows | C |
| 113 | L | O | Financial ID x Financing CF | Insurance financing | C |
| 114 | L | P | Financial ID x Cash Reconciliation | Insurance cash reconciliation | C |
| 115 | M | N | Operating CF x Investing CF | Free cash flow = CFO - capex | V |
| 116 | M | O | Operating CF x Financing CF | Cash retained = CFO - dividends - debt | V |
| 117 | M | P | Operating CF x Cash Reconciliation | CF reconciliation | C |
| 118 | N | O | Investing CF x Financing CF | Investment vs financing balance | V |
| 119 | N | P | Investing CF x Cash Reconciliation | Investing CF reconciliation | C |
| 120 | O | P | Financing CF x Cash Reconciliation | Financing CF reconciliation | C |

**Legend:** V = hop le (co the xay signal), C = co dieu kien (chi voi thesis cu the, mask, hoac validation)

---

## Constraints

1. **Point-in-time:** Fundamentals available only after publication date. Quy don vi: IS/BS/CF Q/A.
2. **No backfill/negative shift:** Missing = unavailable, khong fill backward.
3. **Q/A mix:** IS/BS Q can mix voi A neu co economic thesis (mode_contract SS6).
4. **Population mask:** Financial vs non-financial chi tach bang L2 flag tu nhom L.
5. **Sign convention CF:** Dividends <= 0 (outflow), issuance > 0 (inflow), borrowings > 0 (inflow).
6. **Denominator guards:** All ratios need (denominator > 0) mask.
7. **Group L is mask-only:** Khong dung L lam signal. Chi dung de tao financial flag.

---

## Top Pairs by Economic Strength

| Rank | Pair | Mechanism | Evidence |
|---|---|---|---|
| 1 | A+O | Net payout yield = -(div+rep)/CS/Close | Gate 1-3: 41 PASS/83 total |
| 2 | A+F | P/B, market-to-book | Classic value |
| 3 | B+F | ROE = NI/Equity | Classic quality |
| 4 | B+G | Cash conversion = CFO/NI | Earnings quality |
| 5 | F+G | Cash-to-assets, net debt | Liquidity quality |
| 6 | A+K | Market value = close x CS | Foundation for all market ratios |
| 7 | H+M | WC changes in CFO | Cash conversion driver |
| 8 | I+N | Capex vs disposal | Investment discipline |
| 9 | M+N | FCF = CFO - capex | Free cash flow |
| 10 | A+B | EPS yield, ROA yield | Value + quality |
