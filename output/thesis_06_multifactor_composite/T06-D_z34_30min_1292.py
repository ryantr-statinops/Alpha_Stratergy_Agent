"""
name:    T06-D_z34
summary: Candlestick + Z-Score
idea:    Combine candlestick patterns (hammer, engulfing, morning/evening star) with z-score composite for reversal entries.
"""
class CustomStrategy(SimpleAlgorithm):
    z_window = 34
    thesis_group = "06"

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z

        hammer = self.feat.hammer(open_price, high, low, close)
        engulf = self.feat.engulfing_pattern(open_price, high, low, close)
        morning = self.feat.morning_star(open_price, high, low, close)
        evening = self.feat.evening_star(open_price, high, low, close)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        return_roll = self.feat.returns(close, periods=8)

        bullish_pattern = hammer | engulf | morning
        bearish_pattern = evening

        long_setup = (composite > 1.5) & bullish_pattern & (adx_val > 18) & (return_roll > 0)
        short_setup = (composite < -1.5) & bearish_pattern & (adx_val > 18) & (return_roll < 0)
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < 12)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

