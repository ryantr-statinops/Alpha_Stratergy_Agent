"""
name:    T19-C
summary: BB + Volume
idea:    Same BB distance entry with volume > SMA(20) confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    bb_entry = 0.05
    atr_mult = 2.0
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        bb_pos = (close - bb_lower) / (bb_upper - bb_lower)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = (bb_pos < self.bb_entry) & (volume > vol_sma)
        short_setup = (bb_pos > (1 - self.bb_entry)) & (volume > vol_sma)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

