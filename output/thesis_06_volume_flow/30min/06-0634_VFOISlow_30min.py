
"""
name:    VFOISlow_30min
summary: OI Trend: OI(50) — 30min
thesis:  volume_flow | 30min
idea:    Open Interest trend
"""
class CustomStrategy(SimpleAlgorithm):

    oi_window = 50
    ma_window = 40

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        oi = self.data.fut_open_interest_vn30f1m_1d
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        close_sma = self.feat.sma(close, timeperiod=self.ma_window)

        oi_trend = oi > oi_sma
        price_trend = close > close_sma

        long_setup = ((oi_trend & price_trend) & (return_roll > 0)) & (adx > 22)
        short_setup = ((oi_trend & (~price_trend)) & (return_roll < 0)) & (adx > 22)
        exit_setup = (((oi < oi_sma) | self.op.crossed_below(close, close_sma)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
