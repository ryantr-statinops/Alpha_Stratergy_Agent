class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["02:00-04:30", "06:00-07:20"]
    position_close_ranges = ["04:20-04:30", "07:20-07:30"]
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        natr = self.feat.natr(high, low, close, timeperiod=10)
        natr_sma = self.feat.sma(natr, timeperiod=10)
        adx = self.feat.adx(high, low, close, timeperiod=10)
        trend_sma = self.feat.sma(close, timeperiod=20)
        rsi = self.feat.rsi(close, timeperiod=14)
        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=20, nbdevup=2, nbdevdn=2)

        long_setup = (natr > natr_sma * 1.05) & (close > bb_mid) & (rsi > 50) & (adx > 22) & (close > trend_sma)
        short_setup = (natr > natr_sma * 1.05) & (close < bb_mid) & (rsi < 50) & (adx > 22) & (close < trend_sma)
        exit_setup = (natr < natr_sma) | (adx < 18)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
