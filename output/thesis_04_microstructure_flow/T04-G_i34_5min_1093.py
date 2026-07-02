"""
name:    T04-G_i34
summary: Volume Flow Imbalance
idea:    Track smart money flow via OI change + avg trade size; long on accumulation, short on distribution.
"""
class CustomStrategy(SimpleAlgorithm):
    imbalance_window = 34


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        avg_trade = matched_val / matched_vol
        close_sma = self.feat.sma(close, timeperiod=self.imbalance_window)
        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        adx_val = self.feat.adx(high, low, close, timeperiod=7)

        smart_money_long = (oi_change > 0) & (avg_trade > self.feat.sma(avg_trade, self.imbalance_window))
        smart_money_short = (oi_change < -0.005) & (matched_vol > self.feat.sma(matched_vol, self.imbalance_window) * 1.5)

        long_setup = smart_money_long & (close > close_sma) & (adx_val > 22)
        short_setup = smart_money_short & (close < close_sma) & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, close_sma) | self.op.crossed_above(close, close_sma) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

