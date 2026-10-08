class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        macd_line, signal_line, histogram = self.feat.macdfix(close, signalperiod=9)
        hist_prev = self.feat.sma(histogram, timeperiod=2)
        hist_accel = histogram - hist_prev
        adx = self.feat.adx(high, low, close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)
        rsi = self.feat.rsi(close, timeperiod=14)

        long_setup = (macd_line > signal_line) & (hist_accel > 0) & (rsi > 50) & (adx > 20) & (volume > vol_sma)
        short_setup = (macd_line < signal_line) & (hist_accel < 0) & (rsi < 50) & (adx > 20) & (volume > vol_sma)
        exit_setup = self.op.crossed(macd_line, signal_line) | (adx < 16)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
