
"""
name:    XMConUltra_30min
summary: Consensus: Consensus(7) — 30min
thesis:  cross_market | 30min
idea:    3-market consensus signal
"""
class CustomStrategy(SimpleAlgorithm):

    roc_window = 7

    return_window = 8
    return_threshold = 0.0003
    position_close_after_n_candles = 12
    adx_window = 14

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close
        high = self.data.pv_high
        low = self.data.pv_low
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=self.return_window)
        adx = self.feat.adx(high, low, close, timeperiod=14)

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)
        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)

        bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
        bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)

        long_setup = ((bullish) & (return_roll > 0)) & (adx > 22)
        short_setup = ((bearish) & (return_roll < 0)) & (adx > 22)
        exit_setup = (((~bullish) & (~bearish)) | (abs(return_roll) < self.return_threshold)) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
