
"""
name:    VFValStd_60min
summary: Val Spike: ValSpike(1.3x) — 60min
thesis:  volume_flow | 60min
idea:    Matched value spike
"""
class CustomStrategy(SimpleAlgorithm):

    val_window = 14
    value_mult = 1.3

    return_window = 3
    return_threshold = 0.0001
    position_close_after_n_candles = 6
    adx_window = 7
    adx_entry_threshold = 16
    adx_exit_threshold = 10

    def __algorithm__(self):
        close = self.data.pv_close
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=7)

        val_sma = self.feat.sma(matched_val, timeperiod=self.val_window)
        val_q80 = self.feat.rolling_quantile(matched_val, self.val_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.val_window)

        flow = (matched_val > val_q80) & (matched_val > val_sma * self.value_mult)

        long_setup = ((flow & (close > close_sma)) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((flow & (close < close_sma)) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = (((matched_val < val_sma) | self.op.crossed_below(close, close_sma)) | self.op.crossed_below(abs(return_roll), self.return_threshold)) | self.op.crossed_below(adx, self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
