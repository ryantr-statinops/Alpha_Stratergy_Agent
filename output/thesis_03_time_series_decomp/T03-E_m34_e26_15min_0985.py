"""
name:    T03-E_m34_e26
summary: Dispersion Entropy Proxy
idea:    Use MAD/STD ratio to distinguish structured vs chaotic markets; trade only structured regimes.
"""
class CustomStrategy(SimpleAlgorithm):
    mad_window = 34
    thesis_group = "03"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        mad = self.feat.rolling_mad(close, window=self.mad_window)
        std = self.feat.rolling_std(close, window=self.mad_window)
        mad_ratio = mad / std
        mad_ratio_sma = self.feat.sma(mad_ratio, timeperiod=self.mad_window)

        structured = mad_ratio < mad_ratio_sma * 0.8
        chaotic = mad_ratio > mad_ratio_sma * 1.2

        ema = self.feat.ema(close, timeperiod=26)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        long_setup = (close > ema) & structured & (adx_val > 22)
        short_setup = (close < ema) & structured & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema) | chaotic | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

