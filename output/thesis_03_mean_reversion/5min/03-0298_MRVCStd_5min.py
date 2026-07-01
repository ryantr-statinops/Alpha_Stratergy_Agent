
"""
name:    MRVCStd_5min
summary: Vol Climax: VolClimax(1.5x,RSI<25) — 5min
thesis:  mean_reversion | 5min
idea:    Volume climax reversal
"""
class CustomStrategy(SimpleAlgorithm):

    vol_window = 14
    rsi_window = 7

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        vol_spike = volume > vol_sma * 1.5
        downside_climax = vol_spike & (rsi < 25)
        upside_climax = vol_spike & (rsi > 75)

        long_setup = downside_climax
        short_setup = upside_climax
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
