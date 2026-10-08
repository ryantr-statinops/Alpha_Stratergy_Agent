"""
name:    VnMidQualityVoteSlowExit
summary: Long mid caps on quality votes, held through minor pullbacks.
idea:    The four-signal quality vote with the exit moved from the fast EMA to a
         63-day SMA trend floor. Riding the earnings-quality drift through short
         pullbacks captures the 40-60 trading-day post-report drift instead of
         being whipsawed out, while the SMA floor still cuts major trend breaks.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close

        undistributed_earnings = self.data.fun_bs_undistributed_earnings_quarterly
        owners_equity = self.data.fun_bs_owners_equity_quarterly
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly
        raw_retention = self.feat.safe_divide(undistributed_earnings, owners_equity)
        retention = raw_retention * raw_retention
        retention_baseline = self.feat.sma(retention, timeperiod=63)
        valid_retention = (self.op.notna(undistributed_earnings) & self.op.notna(owners_equity)
                           & self.op.notna(net_profit) & self.op.notna(retention)
                           & self.op.notna(retention_baseline)
                           & (owners_equity > 0) & ((owners_equity * owners_equity) > 0)
                           & (net_profit > 0) & (retention < 4.0))
        vote_retention = valid_retention & (retention > retention_baseline)

        other_receivables = self.data.fun_bs_other_receivables_quarterly
        total_assets = self.data.fun_bs_total_assets_quarterly
        raw_other = self.feat.safe_divide(other_receivables, total_assets)
        orec_burden = raw_other * raw_other
        orec_baseline = self.feat.sma(orec_burden, timeperiod=63)
        valid_orec = (self.op.notna(other_receivables) & self.op.notna(total_assets)
                      & self.op.notna(orec_burden) & self.op.notna(orec_baseline)
                      & (total_assets > 0) & ((total_assets * total_assets) > 0)
                      & (orec_burden < 1.0))
        vote_orec = valid_orec & (orec_burden < orec_baseline)

        tax_payable = self.data.fun_bs_taxes_and_other_payable_to_state_budget_quarterly
        current_liabilities = self.data.fun_bs_current_liabilities_quarterly
        raw_tax = self.feat.safe_divide(tax_payable, current_liabilities)
        tax_burden = raw_tax * raw_tax
        tax_baseline = self.feat.sma(tax_burden, timeperiod=40)
        valid_tax = (self.op.notna(tax_payable) & self.op.notna(current_liabilities)
                     & self.op.notna(tax_burden) & self.op.notna(tax_baseline)
                     & (current_liabilities > 0) & ((current_liabilities * current_liabilities) > 0)
                     & (tax_burden < 1.0))
        vote_tax = valid_tax & (tax_burden < tax_baseline)

        other_income = self.data.fun_is_net_other_income_expenses_quarterly
        raw_other_income = self.feat.safe_divide(other_income, net_profit)
        income_burden = raw_other_income * raw_other_income
        income_baseline = self.feat.sma(income_burden, timeperiod=63)
        valid_income = (self.op.notna(other_income) & self.op.notna(net_profit)
                        & self.op.notna(income_burden) & self.op.notna(income_baseline)
                        & (net_profit > 0) & ((net_profit * net_profit) > 0)
                        & (income_burden < 1.0))
        vote_income = valid_income & (income_burden < income_baseline)

        ema_slow = self.feat.ema(close, timeperiod=36)
        ema_fast = self.feat.ema(close, timeperiod=12)
        trend_floor = self.feat.sma(close, timeperiod=63)

        votes_any = (vote_retention | vote_orec | vote_tax | vote_income)
        votes_strong = ((vote_retention & vote_orec)
                        | (vote_retention & vote_tax)
                        | (vote_retention & vote_income)
                        | (vote_orec & vote_tax)
                        | (vote_orec & vote_income)
                        | (vote_tax & vote_income))

        flat = (~votes_any) | (close < trend_floor)
        weak = votes_any & (~votes_strong) & (close > ema_slow)
        strong = votes_strong & (close > ema_slow) & (ema_fast > ema_slow)

        self.set_positions(flat, position=0)
        self.set_positions(weak, position=0.5)
        self.set_positions(strong, position=1)
