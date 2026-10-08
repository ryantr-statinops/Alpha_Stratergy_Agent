"""
name:    T12-C
summary: KF + ADX Confirmed
idea:    Kalman entries with ADX confirmation on both trend and MR modes; stricter filter for lower signal count but higher win rate.
"""
class CustomStrategy(SimpleAlgorithm):
    sideways_entry = 0.02
    kf_z_entry = 1.5
    kf_z_mr_entry = 2.0
    atr_stop_mult = 2.5
    adx_entry = 20
    adx_exit = 15

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kalman_state = self.feat.sma(close, timeperiod=10)
        kf_residual = close - kalman_state
        kf_dev = close / kalman_state - 1
        residual_std = self.feat.rolling_std(kf_residual, 20)
        kf_z = kf_residual / self.op.fillna(residual_std, 1.0)

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        kf_trend_up = kf_dev > self.sideways_entry
        kf_trend_down = kf_dev < -self.sideways_entry
        kf_sideways = ~kf_trend_up & ~kf_trend_down

        atr_stop_long = close < kalman_state - self.atr_stop_mult * atr_val
        atr_stop_short = close > kalman_state + self.atr_stop_mult * atr_val

        dip_long = kf_trend_up & (kf_z < -self.kf_z_entry) & (adx_val > self.adx_entry)
        rally_short = kf_trend_down & (kf_z > self.kf_z_entry) & (adx_val > self.adx_entry)
        mr_long = kf_sideways & (kf_z < -self.kf_z_mr_entry) & (adx_val < self.adx_entry)
        mr_short = kf_sideways & (kf_z > self.kf_z_mr_entry) & (adx_val < self.adx_entry)

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short

        exit_long = (kf_z > 0.2) | (adx_val < self.adx_exit) | atr_stop_long
        exit_short = (kf_z < -0.2) | (adx_val < self.adx_exit) | atr_stop_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

