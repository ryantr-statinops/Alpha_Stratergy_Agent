"""
name:    T20-B
summary: MinMax + Trend
idea:    Same minmax entry with EMA(20)/EMA(50) trend filter.
"""
class CustomStrategy(SimpleAlgorithm):
    lookback = 200
    pos_entry = 0.05
    ema_fast = 20
    ema_slow = 50
    atr_mult = 2.0

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)

        min_val = self.feat.rolling_min(close, window=self.lookback)
        max_val = self.feat.rolling_max(close, window=self.lookback)
        pos = (close - min_val) / (max_val - min_val)

        ema_20 = self.feat.ema(close, timeperiod=self.ema_fast)
        ema_50 = self.feat.ema(close, timeperiod=self.ema_slow)
        trend_up = ema_20 > ema_50
        trend_down = ema_20 < ema_50

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = (pos < self.pos_entry) & trend_up
        short_setup = (pos > (1 - self.pos_entry)) & trend_down

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

