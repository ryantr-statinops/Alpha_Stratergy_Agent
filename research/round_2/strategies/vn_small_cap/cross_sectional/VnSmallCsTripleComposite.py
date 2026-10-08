"""
name:    VnSmallCsTripleComposite
summary: Quality + Value + Momentum triple composite for VN small caps.
idea:    H36 — three orthogonal economic pillars combined via cross-sectional
          z-scores with equal weighting. Quality (ROE + cash conversion + accrual)
          captures durable profitability. Value (earnings yield + book/market)
          captures mispricing. Momentum (price trend + ROE improvement) captures
          trend persistence. Each pillar is independently z-scored before
          combining to avoid factor dominance.
          Eligibility: universe gate, non-financial, liquidity top 60%.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        eps = self.data.fun_is_eps_basis_quarterly_panel
        equity_q = self.data.fun_bs_owners_equity_quarterly_panel
        total_assets_q = self.data.fun_bs_total_assets_quarterly_panel
        cfo = self.data.fun_cf_net_cash_inflows_outflows_from_operating_activities_annual_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_annual_panel
        total_assets = self.data.fun_bs_total_assets_annual_panel
        in_universe = self.data.in_universe_panel

        # --- Layer 1: Ratios ---
        roe = self.feat.safe_divide_panel(net_profit, equity_q)
        cash_conversion = self.feat.safe_divide_panel(cfo, net_profit)
        accrual_quality = self.feat.safe_divide_panel(cfo - net_profit, total_assets)
        earnings_yield = self.feat.safe_divide_panel(eps, close)
        market_value = close * self.data.fun_bs_common_shares_annual_panel
        book_market = self.feat.safe_divide_panel(equity_q, market_value)
        close_ema = self.feat.ema_panel(close)
        trend_ratio = self.feat.safe_divide_panel(close, close_ema)
        roe_improvement = self.feat.delta_panel(
            self.feat.rolling_mean_panel(
                self.feat.safe_divide_panel(
                    self.data.fun_is_net_profit_loss_after_tax_quarterly_panel,
                    equity_q
                ),
                4
            )
        )

        # --- Layer 2: Factor scores (equal weight within each pillar) ---
        quality_score = (roe + cash_conversion + accrual_quality) / 3
        value_score = (earnings_yield + book_market) / 2
        momentum_score = (trend_ratio + roe_improvement) / 2

        # --- Layer 4: Validation ---
        input_sum = (
            close + volume + eps + equity_q + total_assets_q
            + cfo + net_profit + total_assets
        )
        eligible = (
            in_universe
            & (input_sum == input_sum)
            & (eps > 0) & (close > 0) & (volume > 0)
            & (equity_q > 0) & (total_assets_q > 0)
            & (total_assets > 0) & (market_value > 0)
            & (close_ema > 0)
        )

        # Financial sector exclusion
        gw_premium = self.data.fun_is_gross_written_premium_quarterly_panel
        claim_expense = self.data.fun_is_claim_and_maturity_payment_expenses_quarterly_panel
        unearned_reserve = self.data.fun_bs_unearned_premium_reserve_quarterly_panel
        is_financial = (
            ((gw_premium >= 0) | (gw_premium < 0))
            | ((claim_expense >= 0) | (claim_expense < 0))
            | ((unearned_reserve >= 0) | (unearned_reserve < 0))
        )
        eligible = eligible & (~is_financial)

        # --- Layer 5: Liquidity eligibility ---
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=eligible)
        eligible = eligible & (liquidity_rank > 0.40)

        # --- Layer 6: Composite signal ---
        composite = (quality_score + value_score + momentum_score) / 3

        # --- OP: Portfolio construction ---
        weights = self.op.portfolio_weights_panel(
            composite, method='demean_l1', mask=eligible
        )
        self.set_portfolio_positions(weights)
