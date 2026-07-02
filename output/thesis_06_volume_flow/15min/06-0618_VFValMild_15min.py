
"""
name:    VFValMild_15min
summary: Val Spike: ValSpike(1.2x) — 15min
thesis:  volume_flow | 15min
idea:    Matched value spike
"""
class CustomStrategy(SimpleAlgorithm):

    val_window = 20
    value_mult = 1.2

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24
    adx_window = 10

    def __algorithm__(self):
        close = self.data.pv_close
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=10)

        val_sma = self.feat.sma(matched_val, timeperiod=self.val_window)
        val_q80 = self.feat.rolling_quantile(matched_val, self.val_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.val_window)

        flow = (matched_val > val_q80) & (matched_val > val_sma * self.value_mult)

        long_setup = ((flow & (close > close_sma)) & (return_roll > 0)) & (adx > 22)
        short_setup = ((flow & (close < close_sma)) & (return_roll < 0)) & (adx > 22)
        exit_setup = (((matched_val < val_sma) | self.op.crossed_below(close, close_sma)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
