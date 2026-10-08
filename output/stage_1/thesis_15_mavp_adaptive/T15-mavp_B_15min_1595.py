"""
name:    T15-mavp_B
summary: MAVP Adaptive BBands
idea:    Same mavp core but use mavp as BBands mid band — bands adapt to market cycle. Entry at band touch with ADX + volume. Exit via ADX fade + ATR stop + trailing + band cross.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_nbdev = 2
    adx_entry = 22
    atr_mult = 2.0
    vol_window = 20
    minperiod = 8
    maxperiod = 30

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        dc_period = self.op.fillna(self.feat.dcperiod(close), 20)
        dc_smooth = self.feat.rolling_max(dc_period, 5)
        mavp_ma = self.feat.mavp(close, periods=dc_smooth, minperiod=self.minperiod, maxperiod=self.maxperiod, matype=0)

        bb_upper = mavp_ma + self.feat.rolling_std(close, 20) * self.bb_nbdev
        bb_lower = mavp_ma - self.feat.rolling_std(close, 20) * self.bb_nbdev

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop_long = close < (mavp_ma - self.atr_mult * atr_val)
        atr_stop_short = close > (mavp_ma + self.atr_mult * atr_val)
        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (close > bb_upper) & (adx_val > self.adx_entry) & (volume > vol_sma) & (return_roll > 0)
        short_signal = (close < bb_lower) & (adx_val > self.adx_entry) & (volume > vol_sma) & (return_roll < 0)

        adx_fade = self.op.crossed_below_value(adx_val, 18)
        exit_setup = self.op.hold_for(adx_fade | atr_stop_long | atr_stop_short | trailing_long | trailing_short, 1)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

