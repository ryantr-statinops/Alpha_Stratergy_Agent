"""
name:    T23-A
summary: Hist Slope
idea:    Entry when linearreg_slope(macd_hist, 5) crosses zero. Exit via ATR stop + trailing.
"""
class CustomStrategy(SimpleAlgorithm):
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    slope_window = 5
    atr_mult = 2.0

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)

        macd, macd_signal_line, macd_hist = self.feat.macd(close, fastperiod=self.macd_fast, slowperiod=self.macd_slow, signalperiod=self.macd_signal)
        hist_slope = self.feat.linearreg_slope(macd_hist, timeperiod=self.slope_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = self.op.crossed_above(hist_slope, 0)
        short_setup = self.op.crossed_below(hist_slope, 0)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

