"""
name:    T04-B_m10
summary: MFI Volume-Weighted Reversal
idea:    Trade Money Flow Index extremes with ADX and volume confirmation for high-conviction reversals.
"""
class CustomStrategy(SimpleAlgorithm):
    mfi_window = 10
    thesis_group = "04"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=26)

        long_setup = (mfi < 30) & (adx_val > 18) & (volume > vol_sma * 0.5)
        short_setup = (mfi > 70) & (adx_val > 18) & (volume > vol_sma * 0.5)
        exit_setup = self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

