
"""
name:    BOVN30Fast_15min
summary: VN30 BO: BO(VN30+13) — 15min
thesis:  breakout | 15min
idea:    Dual-market breakout
"""
class CustomStrategy(SimpleAlgorithm):

    q_window = 13

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        fut_upper = self.feat.rolling_quantile(close, self.q_window, 0.80)
        fut_lower = self.feat.rolling_quantile(close, self.q_window, 0.20)
        vn30_upper = self.feat.rolling_quantile(vn30_close, self.q_window, 0.80)
        vn30_lower = self.feat.rolling_quantile(vn30_close, self.q_window, 0.20)

        long_setup = (close > fut_upper) & (vn30_close > vn30_upper)
        short_setup = (close < fut_lower) & (vn30_close < vn30_lower)
        exit_setup = self.op.crossed_below(close, fut_upper) | self.op.crossed_above(close, fut_lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
