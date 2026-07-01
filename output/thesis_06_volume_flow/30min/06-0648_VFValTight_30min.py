
"""
name:    VFValTight_30min
summary: Val Spike: ValSpike(1.5x) — 30min
thesis:  volume_flow | 30min
idea:    Matched value spike
"""
class CustomStrategy(SimpleAlgorithm):

    val_window = 26

    def __algorithm__(self):
        close = self.data.pv_close
        matched_val = self.data.fut_matched_value_vn30f1m_1d

        val_sma = self.feat.sma(matched_val, timeperiod=self.val_window)
        val_q80 = self.feat.rolling_quantile(matched_val, self.val_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.val_window)

        flow = (matched_val > val_q80) & (matched_val > val_sma * 1.3)

        long_setup = flow & (close > close_sma)
        short_setup = flow & (close < close_sma)
        exit_setup = (matched_val < val_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
