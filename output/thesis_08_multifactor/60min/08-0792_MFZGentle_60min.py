
"""
name:    MFZGentle_60min
summary: Z-Score: ZScore(0.8) — 60min
thesis:  multifactor | 60min
idea:    Multi-factor z-score
"""
class CustomStrategy(SimpleAlgorithm):

    z_window = 60
    z_threshold = 0.8
    rsi_window = 21
    adx_window = 21

    return_window = 14
    return_threshold = 0.0005
    position_close_after_n_candles = 6

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.rolling_zscore(volume, window=self.z_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        momentum = self.feat.roc(close, timeperiod=self.rsi_window)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        rsi_ok = (rsi > 30) & (rsi < 70)
        score_ok_long = (composite > self.z_threshold)
        score_ok_short = (composite < -self.z_threshold)

        core_long = score_ok_long & rsi_ok
        core_short = score_ok_short & rsi_ok

        strong_long = core_long & (adx > 22) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & (adx > 18) & (return_roll > 0)
        strong_short = core_short & (adx > 22) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & (adx > 18) & (return_roll < 0)
        exit_setup = ((abs(composite) < 0.5) | (adx < 15)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
