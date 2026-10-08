class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_price = self.data.pv_open
        morning_star = self.feat.morning_star(open_price, high, low, close)
        evening_star = self.feat.evening_star(open_price, high, low, close)
        price_z = self.feat.price_z(close, timeperiod=10)
        volume = self.data.pv_volume
        vol_sma = self.feat.sma(volume, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_setup = (morning_star > 0) & (price_z < -0.5) & (rsi < 45) & (volume > vol_sma)
        short_setup = (evening_star < 0) & (price_z > 0.5) & (rsi > 55) & (volume > vol_sma)
        exit_setup = self.op.crossed(rsi, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
