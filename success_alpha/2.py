"""
name:    T26-B
summary: CMF + RSI
idea:    Same CMF rank with RSI > 50 / < 50 directional filter.
"""
class CustomStrategy(SimpleAlgorithm):
    cmf_window = 20
    rank_window = 150
    entry_q = 0.9
    atr_mult = 2.0

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        rsi_val = self.feat.rsi(close, timeperiod=14)

        cmf_val = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        cmf_rank = self.feat.rolling_rank(cmf_val, window=self.rank_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 5) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 5) + atr_val)

        long_setup = (cmf_rank > self.entry_q) & (rsi_val > 55)
        short_setup = (cmf_rank < (1 - self.entry_q)) & (rsi_val < 45)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=0.5)
        self.set_positions(short_signal, position=-0.5)

