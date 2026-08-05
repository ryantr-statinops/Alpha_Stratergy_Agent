class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        fut_volume = self.data.fut_matched_volume_vn30f1m_1d
        sma10 = self.feat.sma(close, timeperiod=10)
        vol_sma = self.feat.sma(fut_volume, timeperiod=5)

        long_setup = (fut_volume > vol_sma) & (close > sma10)
        short_setup = (fut_volume < vol_sma) & (close < sma10)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
