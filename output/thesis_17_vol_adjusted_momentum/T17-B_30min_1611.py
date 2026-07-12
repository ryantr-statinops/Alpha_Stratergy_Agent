"""
name:    T17-B
summary: Vol-Adj Momentum + SMA Filter
idea:    Same adj_mom_z logic with SMA13/SMA34 trend filter to avoid counter-trend entries; exit adds adj_mom_z < 0 for earlier profit protection.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    adj_window = 14
    z_window = 20
    z_entry = 1.5
    atr_mult = 2.0
    vol_window = 20
    sma_fast = 13
    sma_slow = 34

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adj_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.adj_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        roc_val = self.feat.roc(close, timeperiod=self.adj_window)
        adj_mom = roc_val / atr_val
        adj_mom_z = self.feat.rolling_zscore(adj_mom, window=self.z_window)

        sma_13 = self.feat.sma(close, timeperiod=self.sma_fast)
        sma_34 = self.feat.sma(close, timeperiod=self.sma_slow)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop = atr_val * self.atr_mult
        atr_stop_long = close < (bb_mid - atr_stop)
        atr_stop_short = close > (bb_mid + atr_stop)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (adj_mom_z > self.z_entry) & (close > bb_mid) & (volume > vol_sma) & (sma_13 > sma_34)
        short_signal = (adj_mom_z < -self.z_entry) & (close < bb_mid) & (volume > vol_sma) & (sma_13 < sma_34)

        exit_setup = (adx_val < 18) | atr_stop_long | atr_stop_short | trailing_long | trailing_short | (adj_mom_z < 0)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

