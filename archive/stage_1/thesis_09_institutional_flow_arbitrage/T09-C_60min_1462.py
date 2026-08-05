"""
name:    T09-C
summary: Composite Flow
idea:    OHLCV-based z-score composite (price+vn30+volume) + binary flow alignment (OI == matched volume direction).
"""
class CustomStrategy(SimpleAlgorithm):
    window = 20
    entry = 2.0
    adx_entry = 18
    adx_exit = 12
    atr_stop_mult = 4.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        fut_matched = self.data.fut_matched_volume_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        price_z = self.feat.rolling_zscore(close, window=self.window)
        vn30_z = self.feat.rolling_zscore(vn30_close, window=self.window)
        vol_z = self.feat.rolling_zscore(volume, window=self.window)

        oi_change = self.op.fillna(self.op.pct_change(fut_oi, periods=1), value=0)
        matched_change = self.op.fillna(self.op.pct_change(fut_matched, periods=1), value=0)

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Binary flow signals (safe: using pct_change, not z-score on daily fields)
        oi_flow_up = oi_change > 0
        matched_flow_up = matched_change > 0
        flow_align = oi_flow_up == matched_flow_up

        composite = price_z + vn30_z + vol_z

        long_setup = (composite > self.entry) & flow_align & (adx_val > self.adx_entry)
        short_setup = (composite < -self.entry) & flow_align & (adx_val > self.adx_entry)
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)

