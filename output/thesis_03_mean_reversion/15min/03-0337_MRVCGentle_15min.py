
"""
name:    MRVCGentle_15min
summary: Vol Climax: VolClimax(1.2x,RSI<35) — 15min
thesis:  mean_reversion | 15min
idea:    Volume climax reversal
"""
class CustomStrategy(SimpleAlgorithm):

    vol_window = 20
    rsi_window = 10
    vol_mult = 1.2
    rsi_low = 35
    rsi_high = 65

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        vol_spike = volume > vol_sma * self.vol_mult
        downside_climax = vol_spike & (rsi < self.rsi_low)
        upside_climax = vol_spike & (rsi > self.rsi_high)

        long_setup = downside_climax
        short_setup = upside_climax
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
