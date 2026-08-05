class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close
        rsi_close = self.feat.rsi(close, timeperiod=10)
        rsi_dji = self.feat.rsi(dji_close, timeperiod=10)
        sma10 = self.feat.sma(close, timeperiod=10)

        long_setup = (rsi_close > rsi_dji) & (close > sma10)
        short_setup = (rsi_close < rsi_dji) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
