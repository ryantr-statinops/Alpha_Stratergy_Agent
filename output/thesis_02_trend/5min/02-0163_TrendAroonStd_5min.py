
"""
name:    TrendAroonStd_5min
summary: Aroon: Aroon(7) — 5min
thesis:  trend | 5min
idea:    Aroon trend strength
"""
class CustomStrategy(SimpleAlgorithm):

    aroon_window = 7

    def __algorithm__(self):
        close = self.data.pv_close

        aroon_up, aroon_down = self.feat.aroon(close, timeperiod=self.aroon_window)

        long_setup = (aroon_up > 70) & (aroon_up > aroon_down)
        short_setup = (aroon_down > 70) & (aroon_down > aroon_up)
        exit_setup = (aroon_up < 30) | (aroon_down < 30) | self.op.crossed_below(aroon_up, aroon_down)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
