class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        wma = self.feat.wma(close, timeperiod=10)
        trima = self.feat.trima(close, timeperiod=30)
        sma10 = self.feat.sma(close, timeperiod=10)
        wma_trima = wma - trima
        sign_wt = self.op.sign(wma_trima)
        prev_wt = self.op.previous(sign_wt)

        long_setup = (sign_wt > 0) & (prev_wt <= 0) & (close > wma) & (close > sma10)
        short_setup = (sign_wt < 0) & (prev_wt >= 0) & (close < wma) & (close < sma10)
        exit_setup = self.op.crossed(close, wma) | self.op.crossed(close, trima)
        exit_setup = self.op.crossed(close, wma)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
