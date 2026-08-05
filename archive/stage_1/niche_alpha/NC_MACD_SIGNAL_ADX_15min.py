class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        macd_line, signal_line, histogram = self.feat.macd(close, fastperiod=5, slowperiod=13, signalperiod=5)
        macd_slope = macd_line - self.feat.sma(macd_line, timeperiod=3)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        vol_sma = self.feat.sma(volume, timeperiod=10)
        trend_sma = self.feat.sma(close, timeperiod=20)
        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=1.5, nbdevdn=1.5)

        long_setup = (histogram > 0) & (macd_slope > 0) & (close > bb_lower) & (close > trend_sma) & (adx > 20) & (volume > vol_sma)
        short_setup = (histogram < 0) & (macd_slope < 0) & (close < bb_upper) & (close < trend_sma) & (adx > 20) & (volume > vol_sma)
        exit_setup = self.op.crossed(histogram, 0) | (adx < 16)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
