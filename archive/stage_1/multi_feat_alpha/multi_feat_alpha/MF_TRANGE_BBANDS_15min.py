class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        trange = self.feat.trange(high, low, close)
        trange_sma = self.feat.sma(trange, timeperiod=10)
        bbands_upper, bbands_middle, bbands_lower = self.feat.bbands(close, timeperiod=10, nbdevup=2, nbdevdn=2)

        long_setup = (trange < trange_sma) & (close > bbands_middle)
        short_setup = (trange < trange_sma) & (close < bbands_middle)
        exit_setup = self.op.crossed(close, bbands_middle) | self.op.crossed_above_value(trange, trange_sma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
