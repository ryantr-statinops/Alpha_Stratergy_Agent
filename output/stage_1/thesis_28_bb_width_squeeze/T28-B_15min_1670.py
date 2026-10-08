"""
name:    T28-B
summary: Squeeze + Volume
idea:    Same squeeze breakout with volume confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    squeeze_q = 0.1
    quantile_window = 100
    atr_mult = 2.0
    adx_entry = 22
    rsi_entry = 50
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=2, nbdevdn=2)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        bb_width = (bb_upper - bb_lower) / bb_mid
        bb_width_q10 = self.feat.rolling_quantile(bb_width, window=self.quantile_window, q=self.squeeze_q)
        squeeze = bb_width < bb_width_q10
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)
        rsi_val = self.feat.rsi(close, timeperiod=10)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_setup = squeeze & self.op.crossed_above(close, bb_upper) & (volume > vol_sma) & (adx_val > self.adx_entry) & (return_roll > 0)
        short_setup = squeeze & self.op.crossed_below(close, bb_lower) & (volume > vol_sma) & (adx_val > self.adx_entry) & (return_roll < 0)

        exit_long = ((atr_stop_long | trailing_long) & (rsi_val < self.rsi_entry)) | (return_roll < 0)
        exit_short = ((atr_stop_short | trailing_short) & (rsi_val > self.rsi_entry)) | (return_roll > 0)

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)

