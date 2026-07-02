"""
name:    T04-A_c20
summary: BOP + CMF Flow Detection
idea:    Detect buying/selling pressure with Balance of Power and Chaikin Money Flow; enter on institutional flow + volume.
"""
class CustomStrategy(SimpleAlgorithm):
    cmf_window = 20


    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bop = self.feat.bop(open_price, high, low, close)
        cmf = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=7)
        vol_sma = self.feat.sma(volume, timeperiod=14)

        buying_pressure = (bop > 0) & (cmf > 0)
        selling_pressure = (bop < 0) & (cmf < 0)

        long_setup = buying_pressure & (adx_val > 22) & (volume > vol_sma)
        short_setup = selling_pressure & (adx_val > 22) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(cmf, 0) | self.op.crossed_above(cmf, 0) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

