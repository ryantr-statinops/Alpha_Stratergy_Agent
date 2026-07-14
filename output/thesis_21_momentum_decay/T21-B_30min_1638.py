"""
name:    T21-B
summary: Decay + Volume
idea:    Same slope decay with volume confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    ma_window = 20
    slope_window = 5
    smooth_window = 5
    atr_mult = 2.0
    adx_entry = 22
    rsi_entry = 50
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        mom_ma = self.feat.rolling_mean(close, window=self.ma_window)
        mom_slope = self.feat.linearreg_slope(mom_ma, timeperiod=self.slope_window)
        mom_slope_avg = self.feat.rolling_mean(mom_slope, window=self.smooth_window)
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)
        rsi_val = self.feat.rsi(close, timeperiod=14)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        decay_long = (mom_slope < 0) & self.op.crossed_above(mom_slope, mom_slope_avg) & (volume > vol_sma) & (adx_val > self.adx_entry) & (return_roll > 0)
        decay_short = (mom_slope > 0) & self.op.crossed_below(mom_slope, mom_slope_avg) & (volume > vol_sma) & (adx_val > self.adx_entry) & (return_roll < 0)

        exit_long = ((atr_stop_long | trailing_long) & (rsi_val < self.rsi_entry)) | (return_roll < 0)
        exit_short = ((atr_stop_short | trailing_short) & (rsi_val > self.rsi_entry)) | (return_roll > 0)

        long_signal = decay_long & (~exit_long)
        short_signal = decay_short & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

