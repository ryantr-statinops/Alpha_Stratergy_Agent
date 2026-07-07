"""
name:    T09-B
summary: Flow Divergence
idea:    Matched value flow + VN30 alignment + volume filter to detect institutional participation vs retail noise.
"""
class CustomStrategy(SimpleAlgorithm):
    adx_entry = 18
    adx_exit = 12
    atr_stop_mult = 4.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        fut_matched = self.data.fut_matched_value_vn30f1m_1d
        fut_total = self.data.fut_total_value_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        matched_change = self.op.fillna(self.op.pct_change(fut_matched, periods=1), value=0)
        total_change = self.op.fillna(self.op.pct_change(fut_total, periods=1), value=0)
        fut_ret = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        vn30_ret = self.op.fillna(self.op.pct_change(vn30_close, periods=1), value=0)

        flow_up = matched_change > 0
        fut_bull = fut_ret > 0
        fut_bear = fut_ret < 0
        vn30_align = (fut_ret > 0) == (vn30_ret > 0)

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        vol_sma = self.feat.sma(volume, timeperiod=14)
        volume_ok = volume > vol_sma
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Strong flow: matched value rising + VN30 confirms → genuine
        strong_long = fut_bull & flow_up & vn30_align & (adx_val > self.adx_entry) & volume_ok
        strong_short = fut_bear & flow_up & vn30_align & (adx_val > self.adx_entry) & volume_ok

        # Weak flow: matched value dropping → low conviction → fade
        flow_down = matched_change < 0
        fade_long = fut_bear & flow_down & (adx_val > 18)
        fade_short = fut_bull & flow_down & (adx_val > 18)

        long_setup = strong_long | fade_long
        short_setup = strong_short | fade_short
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)

