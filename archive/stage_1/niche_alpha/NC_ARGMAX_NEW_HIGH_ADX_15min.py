class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        argmax = self.feat.rolling_argmax(close, window=10)
        roc = self.feat.roc(close, timeperiod=5)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        price_z = self.feat.price_z(close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)
        roll_max = self.feat.rolling_max(close, window=10)
        roll_min = self.feat.rolling_min(close, window=10)

        long_setup = (argmax < 2) & (close >= roll_max) & (roc > 0) & (price_z > 0.3) & (adx > 20) & (volume > vol_sma)
        short_setup = (argmax > 7) & (close <= roll_min) & (roc < 0) & (price_z < -0.3) & (adx > 20) & (volume > vol_sma)
        exit_setup = (adx < 16) | self.op.crossed(close, roll_max) | self.op.crossed(close, roll_min)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
