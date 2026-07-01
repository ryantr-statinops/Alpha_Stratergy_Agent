
"""
name:    VFOBVVSlow_60min
summary: OBV Flow: OBV(200) — 60min
thesis:  volume_flow | 60min
idea:    OBV cumulative flow
"""
class CustomStrategy(SimpleAlgorithm):

    obv_window = 200

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)

        long_setup = ((obv > obv_sma) & (close > close_sma)) & (return_roll > 0)
        short_setup = ((obv < obv_sma) & (close < close_sma)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
