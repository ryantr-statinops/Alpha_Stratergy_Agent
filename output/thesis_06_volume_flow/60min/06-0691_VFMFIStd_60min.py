
"""
name:    VFMFIStd_60min
summary: MFI: MFI(34) — 60min
thesis:  volume_flow | 60min
idea:    MFI overbought/oversold
"""
class CustomStrategy(SimpleAlgorithm):

    mfi_window = 34

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)

        long_setup = mfi < 30
        short_setup = mfi > 70
        exit_setup = self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
