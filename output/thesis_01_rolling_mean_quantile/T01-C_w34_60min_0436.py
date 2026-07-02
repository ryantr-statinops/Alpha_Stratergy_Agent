"""
name:    T01-C_w34
summary: Mean + Multi-Confirmation
idea:    Enhanced mean reversion with RSI, volume, and ADX confirmation for higher signal reliability.
"""
class CustomStrategy(SimpleAlgorithm):
    mean_window = 34
    thesis_group = "01"

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        rsi = self.feat.rsi(close, timeperiod=21)
        vol_sma = self.feat.sma(volume, timeperiod=34)
        adx_val = self.feat.adx(high, low, close, timeperiod=21)

        long_setup = (close > mean) & (rsi > 50) & (volume > vol_sma) & (adx_val > 16)
        short_setup = (close < mean) & (rsi < 50) & (volume > vol_sma) & (adx_val > 16)
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean) | (adx_val < 10)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

