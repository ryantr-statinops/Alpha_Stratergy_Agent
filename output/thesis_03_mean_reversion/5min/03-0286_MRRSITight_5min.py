
"""
name:    MRRSITight_5min
summary: RSI Rev: RSI(25/75) — 5min
thesis:  mean_reversion | 5min
idea:    RSI extreme mean reversion
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 5
    rsi_low = 25
    rsi_high = 75

    return_window = 2
    return_threshold = 0.0001
    position_close_after_n_candles = 72
    adx_window = 5
    adx_entry_threshold = 22
    adx_exit_threshold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=5)

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        long_setup = ((rsi < self.rsi_low) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((rsi > self.rsi_high) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
