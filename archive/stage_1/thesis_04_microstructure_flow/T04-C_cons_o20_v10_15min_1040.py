"""
name:    T04-C_cons_o20_v10
summary: OI + Volume Cascade
idea:    Detect margin-call cascades via OI drop + volume spike + price fall; counter-trade exhaustion patterns.
"""
class CustomStrategy(SimpleAlgorithm):
    oi_window = 20
    vol_window_val = 10


    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window_val)

        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        oi_drop = oi_change < -0.02
        vol_spike = matched_vol > vol_sma * 3.0
        price_fall = self.op.pct_change(close, periods=1) < -0.01

        cascade = oi_drop & vol_spike & price_fall

        vol_collapse = matched_vol < vol_sma * 0.5
        price_stable = self.op.abs(self.op.pct_change(close, periods=1)) < 0.01 * 0.2
        exhaustion = oi_drop & vol_collapse & price_stable

        long_setup = exhaustion
        short_setup = cascade
        exit_setup = self.op.crossed_below(close, oi_sma) | self.op.crossed_above(close, oi_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

