"""
name:    T15-mavp
summary: MAVP Adaptive Trend
idea:    Replace fixed SMA(20) with mavp(close, periods=dcperiod). Entry when price crosses adaptive MA with ADX + volume + return_roll confirmation. Exit via ADX fade + ATR stop + trailing.
"""
class CustomStrategy(SimpleAlgorithm):
    fast_limit = 0.5
    slow_limit = 0.05
    atr_mult = 1
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mama, fama = self.feat.mama(close, fastlimit=self.fast_limit, slowlimit=self.slow_limit)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=3)

        atr_stop_long = close < (fama - self.atr_mult * atr_val)
        atr_stop_short = close > (fama + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(high, 8) - (1.2 * atr_val))
        trailing_short = close > (self.feat.rolling_min(low, 8) + (1.2 * atr_val))

        long_setup = (close > fama) & (volume > vol_sma) & (adx_val > 18) & (return_roll > 0)
        short_setup = (close < fama) & (volume > vol_sma) & (adx_val > 18) & (return_roll < 0)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0.0)
        self.set_positions(exit_short, position=0.0)

        self.set_positions(long_signal, position=0.8)
        self.set_positions(short_signal, position=-0.8)

