"""
name:    T05-A_b20_z2.0
summary: Futures-VN30 Spread Reversion
idea:    Trade futures vs VN30 basis via beta-adjusted spread z-score; mean-reversion with ADX trend filter.
"""
class CustomStrategy(SimpleAlgorithm):
    beta_window = 20
    thesis_group = "05"

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        beta_val = self.feat.beta(close, vn30_close, timeperiod=self.beta_window)
        spread = close - beta_val * vn30_close
        spread_z = self.feat.rolling_zscore(spread, window=self.beta_window)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        basis = close - vn30_close
        basis_sma = self.feat.sma(basis, timeperiod=self.beta_window)

        long_setup = (spread_z < -2.0) & (adx_val > 18)
        short_setup = (spread_z > 2.0) & (adx_val > 18)
        exit_setup = self.op.between(spread_z, -1, 1) | self.op.crossed_below(adx_val, 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

