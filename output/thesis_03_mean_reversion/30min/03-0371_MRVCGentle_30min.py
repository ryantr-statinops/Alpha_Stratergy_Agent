
"""
name:    MRVCGentle_30min
summary: Vol Climax: VolClimax(1.2x,RSI<35) — 30min
thesis:  mean_reversion | 30min
idea:    Volume climax reversal
"""
class CustomStrategy(SimpleAlgorithm):

    vol_window = 20
    rsi_window = 9
    vol_mult = 1.2
    rsi_low = 35
    rsi_high = 65

    return_window = 5
    return_threshold = 0.0006
    position_close_after_n_candles = 12
    adx_window = 9
    adx_entry_threshold = 18
    adx_exit_threshold = 12

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=9)

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        vol_spike = volume > vol_sma * self.vol_mult
        downside_climax = vol_spike & (rsi < self.rsi_low)
        upside_climax = vol_spike & (rsi > self.rsi_high)

        long_setup = ((downside_climax) & (return_roll > 0)) & (adx > self.adx_entry_threshold)
        short_setup = ((upside_climax) & (return_roll < 0)) & (adx > self.adx_entry_threshold)
        exit_setup = ((self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)) | (abs(return_roll) < self.return_threshold)) | (adx < self.adx_exit_threshold)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
