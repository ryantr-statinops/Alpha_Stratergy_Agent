
"""
name:    VFMFIVSlow_30min
summary: MFI: MFI(60) — 30min
thesis:  volume_flow | 30min
idea:    MFI overbought/oversold
"""
class CustomStrategy(SimpleAlgorithm):

    mfi_window = 60

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 12
    adx_window = 10
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)

        long_setup = ((mfi < 30) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((mfi > 70) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
