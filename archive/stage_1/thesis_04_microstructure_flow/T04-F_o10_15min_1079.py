"""
name:    T04-F_o10
summary: OBV Trend Confirmation
idea:    Confirm price trend with On-Balance Volume alignment; exit on OBV/price divergence.
"""
class CustomStrategy(SimpleAlgorithm):
    obv_window = 10


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (close > close_sma) & (obv > obv_sma) & (adx_val > 22)
        short_setup = (close < close_sma) & (obv < obv_sma) & (adx_val > 22)
        exit_setup = self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

