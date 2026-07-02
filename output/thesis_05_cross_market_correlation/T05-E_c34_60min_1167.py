"""
name:    T05-E_c34
summary: Rolling Correlation Trend Filter
idea:    Use rolling correlation between futures/VN30 and futures/DJI as a trend filter; avoid negative correlation regimes.
"""
class CustomStrategy(SimpleAlgorithm):
    correl_window = 34


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close
        high = self.data.pv_high
        low = self.data.pv_low

        fut_vn30_correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        fut_dji_correl = self.feat.rolling_correlation(close, dji_close, window=self.correl_window)

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        roc_val = self.feat.roc(close, timeperiod=14)

        correl_aligned = (fut_vn30_correl > 0.5) & (fut_dji_correl > 0)
        correl_negative = (fut_vn30_correl < -0.3) | (fut_dji_correl < -0.3)

        long_setup = correl_aligned & (roc_val > 0) & (adx_val > 16)
        short_setup = correl_aligned & (roc_val < 0) & (adx_val > 16)
        exit_setup = correl_negative | self.op.crossed_below(adx_val, 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

