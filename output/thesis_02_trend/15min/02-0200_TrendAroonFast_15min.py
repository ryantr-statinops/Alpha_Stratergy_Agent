
"""
name:    TrendAroonFast_15min
summary: Aroon: Aroon(13) — 15min
thesis:  trend | 15min
idea:    Aroon trend strength
"""
class CustomStrategy(SimpleAlgorithm):

    aroon_window = 13

    return_window = 5
    return_threshold = 0.0002
    position_close_after_n_candles = 24

    def __algorithm__(self):
        close = self.data.pv_close
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)

        aroon_up, aroon_down = self.feat.aroon(close, timeperiod=self.aroon_window)

        long_setup = ((aroon_up > 70) & (aroon_up > aroon_down)) & (return_roll > 0)
        short_setup = ((aroon_down > 70) & (aroon_down > aroon_up)) & (return_roll < 0)
        exit_setup = ((aroon_up < 30) | (aroon_down < 30) | self.op.crossed_below(aroon_up, aroon_down)) | (abs(return_roll) < self.return_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
