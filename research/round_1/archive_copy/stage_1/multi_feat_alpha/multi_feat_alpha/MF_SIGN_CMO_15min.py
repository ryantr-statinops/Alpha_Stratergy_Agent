class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        cmo = self.feat.cmo(close, timeperiod=10)
        trima = self.feat.trima(close, timeperiod=30)
        sma10 = self.feat.sma(close, timeperiod=10)
        sign_cmo = self.op.sign(cmo)

        long_setup = (sign_cmo > 0) & (close > trima) & (close > sma10)
        short_setup = (sign_cmo < 0) & (close < trima) & (close < sma10)
        exit_setup = self.op.crossed(close, trima) | self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
