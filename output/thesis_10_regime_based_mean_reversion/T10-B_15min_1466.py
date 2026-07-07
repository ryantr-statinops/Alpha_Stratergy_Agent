"""
name:    T10-B
summary: Confirmed Regime Entries
idea:    Same regime filter + ADX + volume confirmation for dip/rally entries; sideways uses RSI extremes with low volume.
"""
class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = 0.02
    adx_entry = 22
    adx_exit = 15
    atr_stop_mult = 2.5


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        ma200 = self.feat.sma(close, timeperiod=200)
        ma20 = self.feat.sma(close, timeperiod=20)
        ratio = close / ma200
        warmup = ma200 > 0

        bull = warmup & (ratio > 1 + self.sideways_buffer)
        bear = warmup & (ratio < 1 - self.sideways_buffer)
        sideways = warmup & ~bull & ~bear

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=14)
        volume_ok = volume > vol_sma
        rsi = self.feat.rsi(close, timeperiod=14)
        atr = self.feat.atr(high, low, close, timeperiod=14)

        trailing_high = self.feat.rolling_max(high, window=10)
        trailing_low = self.feat.rolling_min(low, window=10)
        no_long_stop = close >= trailing_high - self.atr_stop_mult * atr
        no_short_stop = close <= trailing_low + self.atr_stop_mult * atr
        trailing_stop = (
            (close < trailing_high - self.atr_stop_mult * atr) |
            (close > trailing_low + self.atr_stop_mult * atr)
        )

        dip_long = bull & (close < ma20) & (adx_val > self.adx_entry) & volume_ok & no_long_stop
        rally_short = bear & (close > ma20) & (adx_val > self.adx_entry) & volume_ok & no_short_stop
        mr_long = sideways & (close < lower_q) & (rsi < 30) & (volume < vol_sma) & no_long_stop
        mr_short = sideways & (close > upper_q) & (rsi > 70) & (volume < vol_sma) & no_short_stop

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (
            self.op.crossed_above(close, ma20) |
            self.op.crossed_below(close, ma20) |
            self.op.crossed_above(close, lower_q) |
            self.op.crossed_below(close, upper_q) |
            (adx_val < self.adx_exit) |
            trailing_stop
        )

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

