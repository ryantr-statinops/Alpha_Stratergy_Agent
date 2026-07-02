"""
name:    T02-C_a20_v34
summary: 3-State Regime Proxy
idea:    Proxy Hidden Markov Model via ADX (trend) and vol regime (ATR std); switch between momentum and mean-reversion modes.
"""
class CustomStrategy(SimpleAlgorithm):
    adx_window = 20
    vol_window = 34


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vol_ratio = volume / vol_sma
        vol_regime = self.feat.rolling_std(atr_val, window=self.vol_window)
        vol_regime_sma = self.feat.sma(vol_regime, window=self.vol_window)

        roc_fast = self.feat.roc(close, timeperiod=3)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)
        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)

        momentum_mode = (adx_val > 25) & (vol_regime > vol_regime_sma)
        meanrev_mode = (adx_val < 22) & (vol_regime < vol_regime_sma)

        mom_long = momentum_mode & (roc_fast > 0) & (volume > vol_sma)
        mom_short = momentum_mode & (roc_fast < 0) & (volume > vol_sma)

        mr_long = meanrev_mode & (close < lower_q) & (volume < vol_sma)
        mr_short = meanrev_mode & (close > upper_q) & (volume < vol_sma)

        long_setup = mom_long | mr_long
        short_setup = mom_short | mr_short
        exit_setup = self.op.crossed_below(adx_val, 15) | (adx_val < 18)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

