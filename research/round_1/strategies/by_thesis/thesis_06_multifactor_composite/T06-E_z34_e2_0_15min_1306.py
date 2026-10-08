"""
name:    T06-E_z34_e2.0
summary: Adaptive Regime-Weighted
idea:    Dynamically weight z-score factors based on ADX/ATR regime; trend weights momentum, high-vol weights volume.
"""
class CustomStrategy(SimpleAlgorithm):
    z_window = 34


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        adx_val = self.feat.adx(high, low, close, timeperiod=10)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        atr_sma = self.feat.sma(atr_val, timeperiod=20)

        strong_trend = adx_val > 25
        weak_trend = (adx_val > 20) & (adx_val <= 25)
        high_vol = atr_val > atr_sma * 1.3

        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)
        ratio = close / vn30_close
        ratio_z = self.feat.rolling_zscore(ratio, window=self.z_window)

        if strong_trend:
            composite = price_z * 1.5 + mom_z * 1.0 + vol_z * 0.5
        elif high_vol:
            composite = price_z * 1.0 + vol_z * 1.5 + ratio_z * 0.5
        else:
            composite = price_z * 0.5 + ratio_z * 1.0 + mom_z * 0.5

        rsi = self.feat.rsi(close, timeperiod=10)
        return_roll = self.feat.returns(close, periods=5)

        strong_long = (composite > 2.0) & (adx_val > 22) & (rsi > 40) & (return_roll > 0)
        weak_long = (composite > 2.0) & (adx_val > 18) & (return_roll > 0)
        strong_short = (composite < -2.0) & (adx_val > 22) & (rsi < 60) & (return_roll < 0)
        weak_short = (composite < -2.0) & (adx_val > 18) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)

