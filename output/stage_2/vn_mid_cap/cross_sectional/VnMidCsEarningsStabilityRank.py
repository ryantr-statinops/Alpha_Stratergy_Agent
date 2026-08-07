"""
name:    VnMidCsEarningsStabilityRank
summary: Buy mid caps whose earnings become more stable against their own
         baseline while the uptrend holds. Low ROA volatility improvement
         vote plus trend vote. Retrofitted from success_alpha vote-basis.
idea:    H10 - Consistent earnings signal durable competitive advantage.
         Earnings Stability test. Success_alpha lesson: measure improvement
         vs. own history combined with an uptrend vote.
"""

class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        in_universe = self.data.in_universe_panel
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel
        net_profit = self.data.fun_is_net_profit_loss_after_tax_quarterly_panel
        total_assets = self.data.fun_bs_total_assets_quarterly_panel
        equity = self.data.fun_bs_owners_equity_quarterly_panel

        roa = self.feat.safe_divide_panel(net_profit, total_assets)
        roa_mean = self.feat.rolling_mean_panel(roa)
        roa_std = self.feat.rolling_std_panel(roa)
        stability = self.feat.safe_divide_panel(roa_std, roa_mean)
        low_vol = -stability
        capital_strength = self.feat.safe_divide_panel(equity, total_assets)
        base_eligible = (
            (in_universe == True) & (close > 0) & (volume > 0) & (total_assets > 0)
            & (equity > 0) & (capital_strength > 0.15)
        )
        traded_value = self.feat.rolling_value_panel(close, volume)
        liquidity_rank = self.op.rank_cs_panel(traded_value, mask=base_eligible)
        eligible = base_eligible & (liquidity_rank > 0.40)

        low_vol_baseline = self.feat.rolling_mean_panel(low_vol)
        low_vol_improve = low_vol - low_vol_baseline
        trend = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        improve_rank = self.op.rank_cs_panel(low_vol_improve, mask=eligible)
        trend_rank = self.op.rank_cs_panel(trend, mask=eligible)
        signal = improve_rank + trend_rank
        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)