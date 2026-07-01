
"""
name:    MFMomFast_60min
summary: Momentum MF: MFMom(10) — 60min
thesis:  multifactor | 60min
idea:    Multi-layer momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 10
    roc_window = 30

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod=21)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        morning_momentum = (roc > 0) & (rsi > 50) & (rsi < 65)
        volume_confirm = volume > vol_sma
        trend_confirm = adx > 20

        long_setup = morning_momentum & volume_confirm & trend_confirm
        short_setup = (roc < 0) & (rsi < 50) & (rsi > 35) & volume_confirm & trend_confirm
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
