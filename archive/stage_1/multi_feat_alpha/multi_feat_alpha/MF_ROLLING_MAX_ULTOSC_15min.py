class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        ultosc = self.feat.ultosc(high, low, close, timeperiod1=5, timeperiod2=10, timeperiod3=20)
        ultosc_sma = self.feat.sma(ultosc, timeperiod=10)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (ultosc > ultosc_sma) & (close > sma10)
        short_setup = (ultosc < ultosc_sma) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10) | self.op.crossed(ultosc, ultosc_sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
