
"""
name:    MRBBTight_5min
summary: BBands Rev: BBands(2.5STD) — 5min
thesis:  mean_reversion | 5min
idea:    Bollinger Band reversion
"""
class CustomStrategy(SimpleAlgorithm):

    bbands_window = 10
    nbdev = 2.5

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

        upper, mid_band, lower = self.feat.bbands(
            close, timeperiod=self.bbands_window, nbdevup=self.nbdev, nbdevdn=self.nbdev
        )

        long_setup = ((close < lower) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((close > upper) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(close, mid_band) | self.op.crossed_below(close, mid_band)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
