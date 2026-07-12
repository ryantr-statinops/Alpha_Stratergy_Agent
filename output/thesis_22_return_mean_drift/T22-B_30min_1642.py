"""
name:    T22-B
summary: RetMean + ADX
idea:    Same return mean cross with ADX > threshold confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    ret_window = 20
    entry_threshold = 0.001
    adx_entry = 22
    atr_mult = 2.0

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        ret_mean = self.feat.rolling_mean(return_1, window=self.ret_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = self.op.crossed_above_value(ret_mean, self.entry_threshold) & (adx_val > self.adx_entry)
        short_setup = self.op.crossed_below_value(ret_mean, -self.entry_threshold) & (adx_val > self.adx_entry)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

