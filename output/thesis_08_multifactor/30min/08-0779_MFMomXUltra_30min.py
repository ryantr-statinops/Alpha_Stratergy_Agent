
"""
name:    MFMomXUltra_30min
summary: Momentum MF: MFMom(3) — 30min
thesis:  multifactor | 30min
idea:    Multi-layer momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3
    roc_window = 13
    adx_window = 9

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        morning_momentum = (roc > 0) & (rsi > 50) & (rsi < 65)
        volume_confirm = volume > vol_sma

        core_long = morning_momentum
        core_short = (roc < 0) & (rsi < 50) & (rsi > 35)

        strong_long = core_long & volume_confirm & (adx > 22) & (return_roll > 0)
        weak_long = core_long & (adx > 18) & (return_roll > 0)
        strong_short = core_short & volume_confirm & (adx > 22) & (return_roll < 0)
        weak_short = core_short & (adx > 18) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
