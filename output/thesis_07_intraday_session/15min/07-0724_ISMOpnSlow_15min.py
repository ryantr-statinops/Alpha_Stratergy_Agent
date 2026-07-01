
"""
name:    ISMOpnSlow_15min
summary: Open Drive: OpenDrive(20) — 15min
thesis:  intraday_session | 15min
idea:    Morning session momentum
"""
class CustomStrategy(SimpleAlgorithm):

    rsi_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        open_range = (close - open_price) / open_price * 100
        candle_range = high - low
        avg_range = self.feat.sma(candle_range, timeperiod=self.rsi_window)

        expanding_range = candle_range > avg_range
        bullish_drive = (open_range > 0.3) & expanding_range & (rsi > 50) & (rsi < 70)
        bearish_drive = (open_range < -0.3) & expanding_range & (rsi < 50) & (rsi > 30)

        long_setup = bullish_drive
        short_setup = bearish_drive
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
