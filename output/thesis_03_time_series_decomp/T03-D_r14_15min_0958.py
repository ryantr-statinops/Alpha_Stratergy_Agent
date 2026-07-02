"""
name:    T03-D_r14
summary: Sine Crossover
idea:    Trade sine/leadsine crossovers as cycle entry signals, filtered by RSI and ADX.
"""
class CustomStrategy(SimpleAlgorithm):
    rsi_window = 14


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        sine, leadsine = self.feat.sine(close)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        cycle_up = self.op.crossed_above(sine, leadsine)
        cycle_down = self.op.crossed_below(sine, leadsine)

        long_setup = cycle_up & (rsi > 30) & (adx_val > 22)
        short_setup = cycle_down & (rsi < 70) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

