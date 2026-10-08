"""
name:    T14-A
summary: BB Squeeze Reversal
idea:    Bollinger squeeze reversal: trade when price touches outer band + volume confirmation; exit via ATR stop + trailing.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        atr_val = self.feat.atr(high, low, close, timeperiod=self.bb_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (volume > vol_sma)
        rally_short = (close < bb_lower) & (volume > vol_sma)

        long_signal = dip_long
        short_signal = rally_short

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(long_signal, position=1)

        self.set_positions(exit_short, position=0)
        self.set_positions(short_signal, position=-1)

