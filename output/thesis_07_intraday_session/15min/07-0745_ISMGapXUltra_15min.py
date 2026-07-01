
"""
name:    ISMGapXUltra_15min
summary: Gap Fill: GapFill(3) — 15min
thesis:  intraday_session | 15min
idea:    Intraday gap fill
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 3

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        gap = (open_price / close - 1) * 100

        gap_up = gap > 0.3
        gap_down = gap < -0.3
        filling_down = gap_up & (close < open_price) & (rsi < 60)
        filling_up = gap_down & (close > open_price) & (rsi > 40)

        long_setup = filling_up
        short_setup = filling_down
        exit_setup = self.op.crossed_above(abs(gap), 0.1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
