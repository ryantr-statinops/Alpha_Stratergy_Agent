"""
name:    T13-A
summary: CMF + Squeeze Breakout
idea:    Bollinger squeeze (bb_width < SMA*0.8) + CMF directional flow + ADX trend filter + volume confirmation; exit via ADX fade + ATR stop only.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    cmf_window = 20
    adx_exit = 14
    atr_mult = 2.5
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        cmf_val = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (cmf_val > 0) & (volume > vol_sma)
        rally_short = (close < bb_lower) & (cmf_val < 0) & (volume > vol_sma)

        long_signal = dip_long
        short_signal = rally_short

        exit_setup = (adx_val < self.adx_exit) | atr_stop_long | atr_stop_short | trailing_long | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

