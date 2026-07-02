"""
name:    T02-E_n34
summary: NATR Regime Switching
idea:    Normalized ATR regime detection; trade trend during high vol, mean-reversion during low vol.
"""
class CustomStrategy(SimpleAlgorithm):
    natr_window = 34
    thesis_group = "02"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        natr = self.feat.natr(high, low, close, timeperiod=self.natr_window)
        natr_sma = self.feat.sma(natr, timeperiod=self.natr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        high_vol = natr > natr_sma * 1.3
        low_vol = natr < natr_sma * 0.7

        roc_val = self.feat.roc(close, timeperiod=8)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_trend = high_vol & (roc_val > 0) & (adx_val > 18)
        short_trend = high_vol & (roc_val < 0) & (adx_val > 18)
        long_rev = low_vol & (rsi < 30) & (adx_val < 20)
        short_rev = low_vol & (rsi > 70) & (adx_val < 20)

        long_setup = long_trend | long_rev
        short_setup = short_trend | short_rev
        exit_setup = self.op.crossed_below(adx_val, 15) | (natr < natr_sma * 0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

