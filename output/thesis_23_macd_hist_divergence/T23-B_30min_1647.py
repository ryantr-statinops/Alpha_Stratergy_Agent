"""
name:    T23-B
summary: Hist + Price Cross
idea:    Same hist slope entry with price relative to BB mid-band confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    slope_window = 5
    bb_window = 20
    atr_mult = 2.0
    adx_entry = 22
    rsi_entry = 50

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)

        macd, macd_signal_line, macd_hist = self.feat.macd(close, fastperiod=self.macd_fast, slowperiod=self.macd_slow, signalperiod=self.macd_signal)
        hist_slope = self.feat.linearreg_slope(macd_hist, timeperiod=self.slope_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)
        rsi_val = self.feat.rsi(close, timeperiod=14)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = self.op.crossed_above(hist_slope, 0) & (close > bb_mid) & (adx_val > self.adx_entry) & (return_roll > 0)
        short_setup = self.op.crossed_below(hist_slope, 0) & (close < bb_mid) & (adx_val > self.adx_entry) & (return_roll < 0)

        exit_long = ((atr_stop_long | trailing_long) & (rsi_val < self.rsi_entry)) | (return_roll < 0)
        exit_short = ((atr_stop_short | trailing_short) & (rsi_val > self.rsi_entry)) | (return_roll > 0)

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

