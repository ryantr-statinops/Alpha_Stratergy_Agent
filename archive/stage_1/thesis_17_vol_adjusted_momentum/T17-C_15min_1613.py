"""
name:    T17-C
summary: Vol-Adj Momentum Regime
idea:    Adaptive adj_mom_z threshold (±2.0 in low vol, ±1.2 in high vol) and trailing mult (1.5/2.5) based on ATR ratio regime.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    adj_window = 14
    z_window = 20
    atr_mult_low = 1.5
    atr_mult_high = 2.5
    vol_window = 20

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

        vol_regime = atr_val / self.feat.sma(atr_val, timeperiod=self.z_window)
        low_vol = vol_regime < 0.8

        z_entry = self.op.where(low_vol, 2.0, 1.2)
        trailing_mult = self.op.where(low_vol, self.atr_mult_low, self.atr_mult_high)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop_long = close < (bb_mid - trailing_mult * atr_val)
        atr_stop_short = close > (bb_mid + trailing_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (adj_mom_z > z_entry) & (close > bb_mid) & (volume > vol_sma) & (return_roll > 0)
        short_signal = (adj_mom_z < -z_entry) & (close < bb_mid) & (volume > vol_sma) & (return_roll < 0)

        exit_setup = (adx_val < 18) | atr_stop_long | atr_stop_short | trailing_long | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

