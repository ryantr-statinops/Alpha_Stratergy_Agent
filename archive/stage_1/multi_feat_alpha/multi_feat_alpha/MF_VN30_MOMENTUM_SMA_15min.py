class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        volume = self.data.pv_volume
        roc_close = self.feat.roc(close, timeperiod=5)
        roc_vn30 = self.feat.roc(vn30_close, timeperiod=5)
        sma10 = self.feat.sma(close, timeperiod=10)
        volume_sma = self.feat.sma(volume, timeperiod=10)
        delta_roc = roc_close - roc_vn30
        delta_roc_sma = self.feat.sma(delta_roc, timeperiod=5)

        long_setup = (delta_roc > delta_roc_sma) & (close > sma10) & (volume > volume_sma)
        short_setup = (delta_roc < delta_roc_sma) & (close < sma10) & (volume > volume_sma)
        exit_setup = self.op.crossed(close, sma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
