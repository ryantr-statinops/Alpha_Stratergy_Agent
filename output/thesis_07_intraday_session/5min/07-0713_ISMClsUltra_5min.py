
"""
name:    ISMClsUltra_5min
summary: Close Sq: CloseSqz(3) — 5min
thesis:  intraday_session | 5min
idea:    Close window squeeze
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 72
    position_open_ranges = ['02:00-04:30', '06:00-07:45']
    position_close_ranges = ['04:20-04:30', '07:30-07:45']

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        roc = self.feat.roc(close, timeperiod=self.rsi_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        squeeze = (rsi > 50) & (rsi < 70) & (roc > 0) & (volume > vol_sma)

        long_setup = (squeeze) & (return_roll > 0)
        short_setup = ((rsi < 50) & (rsi > 30) & (roc < 0) & (volume > vol_sma)) & (return_roll < 0)
        exit_setup = (self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
