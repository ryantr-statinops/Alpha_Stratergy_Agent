"""
name:    T16-A
summary: Velocity Divergence
idea:    Compare price velocity (roc) vs volume velocity (volume_z). Volume surges before price moves = accumulation. Price surges on fading volume = fake breakout. Exit via ADX fade + ATR stop + trailing.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20
    adx_entry = 15

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)

        volume_z = self.feat.rolling_zscore(volume, window=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        vol_push = (volume_z > 0.5) & (close > bb_mid) & (adx_val > self.adx_entry)
        price_fade = (volume_z < 0.0) & (close > bb_upper) & (adx_val > self.adx_entry)

        long_signal = vol_push
        short_signal = price_fade

        exit_long = atr_stop_long | trailing_long | (close < bb_mid)
        exit_short = atr_stop_short | trailing_short | (close > bb_mid)

        exit_action = (exit_long & (long_signal == 0)) | (exit_short & (short_signal == 0))

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_action, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

