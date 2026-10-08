class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        roc_close = self.feat.roc(close, timeperiod=5)
        sma10 = self.feat.sma(close, timeperiod=10)
        oi_sma = self.feat.sma(fut_oi, timeperiod=5)

        long_setup = (fut_oi > oi_sma) & (roc_close > 0) & (close > sma10)
        short_setup = (fut_oi < oi_sma) & (roc_close < 0) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
