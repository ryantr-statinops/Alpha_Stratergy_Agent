
"""
name:    VFOIVSlow_60min
summary: OI Trend: OI(200) — 60min
thesis:  volume_flow | 60min
idea:    Open Interest trend
"""
class CustomStrategy(SimpleAlgorithm):

    oi_window = 200
    ma_window = 60

    def __algorithm__(self):
        close = self.data.pv_close
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        close_sma = self.feat.sma(close, timeperiod=self.ma_window)

        oi_trend = oi > oi_sma
        price_trend = close > close_sma

        long_setup = oi_trend & price_trend
        short_setup = oi_trend & (~price_trend)
        exit_setup = (oi < oi_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
