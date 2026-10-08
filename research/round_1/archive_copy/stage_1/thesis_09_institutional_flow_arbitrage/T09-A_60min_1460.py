"""
name:    T09-A
summary: OI Confirmation
idea:    Compare OI change direction vs futures return; genuine when aligned, fade when OI drops (weak conviction).
"""
class CustomStrategy(SimpleAlgorithm):
    adx_entry = 18
    adx_exit = 12
    atr_stop_mult = 4.0


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        oi_change = self.op.fillna(self.op.pct_change(fut_oi, periods=1), value=0)
        fut_ret = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        fut_bull = fut_ret > 0
        fut_bear = fut_ret < 0
        oi_up = oi_change > 0
        oi_down = oi_change < 0

        adx_val = self.feat.adx(high, low, close, timeperiod=21)
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Genuine: price + OI same direction
        genuine_long = fut_bull & oi_up & (adx_val > self.adx_entry)
        genuine_short = fut_bear & oi_up & (adx_val > self.adx_entry)

        # Fade: price moves but OI drops (weak conviction)
        fade_long = fut_bear & oi_down & (adx_val > 18)
        fade_short = fut_bull & oi_down & (adx_val > 18)

        long_setup = genuine_long | fade_long
        short_setup = genuine_short | fade_short
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)

