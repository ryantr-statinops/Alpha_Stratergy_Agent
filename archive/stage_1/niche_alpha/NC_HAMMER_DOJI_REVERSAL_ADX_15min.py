class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        rsi = self.feat.rsi(close, timeperiod=14)
        price_z = self.feat.price_z(close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)

        long_setup = (close < bb_lower) & (rsi < 35) & (price_z < -0.7) & (volume > vol_sma)
        short_setup = (close > bb_upper) & (rsi > 65) & (price_z > 0.7) & (volume > vol_sma)
        exit_setup = self.op.crossed(close, bb_mid)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
