class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_price = self.data.pv_open
        three_methods = self.feat.rising_falling_three_methods(open_price, high, low, close)
        volume = self.data.pv_volume
        vol_sma = self.feat.sma(volume, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=14)
        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)
        roc = self.feat.roc(close, timeperiod=5)

        long_setup = (three_methods > 0) & (roc > 0) & (rsi > 50) & (close < bb_upper) & (volume > vol_sma)
        short_setup = (three_methods < 0) & (roc < 0) & (rsi < 50) & (close > bb_lower) & (volume > vol_sma)
        exit_setup = self.op.crossed(rsi, 50)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
