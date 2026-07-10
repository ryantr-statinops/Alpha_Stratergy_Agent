"""
name:    T14-B
summary: BB Squeeze Detection
idea:    Same BB reversal core + BB width squeeze detection (bb_width < sma(bb_width,20)) to ensure entries only during/after a squeeze phase.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20
    squeeze_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        atr_val = self.feat.atr(high, low, close, timeperiod=self.bb_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        bb_width = (bb_upper - bb_lower) / bb_mid
        bb_width_ma = self.feat.sma(bb_width, timeperiod=self.squeeze_window)
        squeeze_phase = bb_width < bb_width_ma

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (volume > vol_sma) & squeeze_phase
        rally_short = (close < bb_lower) & (volume > vol_sma) & squeeze_phase

        long_signal = dip_long
        short_signal = rally_short

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(long_signal, position=1)

        self.set_positions(exit_short, position=0)
        self.set_positions(short_signal, position=-1)

