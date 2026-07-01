
"""
name:    VFOBVUltra_30min
summary: OBV Flow: OBV(20) — 30min
thesis:  volume_flow | 30min
idea:    OBV cumulative flow
"""
class CustomStrategy(SimpleAlgorithm):

    obv_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)

        long_setup = (obv > obv_sma) & (close > close_sma)
        short_setup = (obv < obv_sma) & (close < close_sma)
        exit_setup = self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
