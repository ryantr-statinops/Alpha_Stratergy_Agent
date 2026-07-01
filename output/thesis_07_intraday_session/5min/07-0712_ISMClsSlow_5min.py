
"""
name:    ISMClsSlow_5min
summary: Close Sq: CloseSqz(14) — 5min
thesis:  intraday_session | 5min
idea:    Close window squeeze
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        roc = self.feat.roc(close, timeperiod=self.rsi_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        squeeze = (rsi > 50) & (rsi < 70) & (roc > 0) & (volume > vol_sma)

        long_setup = squeeze
        short_setup = (rsi < 50) & (rsi > 30) & (roc < 0) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
