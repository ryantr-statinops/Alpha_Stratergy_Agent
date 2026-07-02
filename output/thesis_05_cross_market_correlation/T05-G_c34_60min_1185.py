"""
name:    T05-G_c34
summary: Correlation Breakdown Detection
idea:    Detect correlation breakdown between futures and VN30; trade the dislocation with volume confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    correl_window = 34


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        correl_sma = self.feat.sma(correl, window=self.correl_window)
        correl_std = self.feat.rolling_std(correl, window=self.correl_window)

        breakdown = correl < (correl_sma - 2 * correl_std)
        rebuilding = self.op.crossed_above(correl, correl_sma)

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        vol_sma = self.feat.sma(volume, timeperiod=34)

        long_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > 16)
        short_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > 16)
        exit_setup = rebuilding | self.op.crossed_below(adx_val, 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

