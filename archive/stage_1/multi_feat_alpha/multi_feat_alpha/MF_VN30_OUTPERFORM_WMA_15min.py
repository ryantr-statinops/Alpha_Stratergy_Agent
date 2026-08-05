class CustomStrategy(SimpleAlgorithm):
    position_close_after_n_candles = 12

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        volume = self.data.pv_volume
        wma10 = self.feat.wma(close, timeperiod=10)
        outperform = close / vn30_close
        roc_outperform = self.feat.roc(outperform, timeperiod=5)
        volume_sma = self.feat.sma(volume, timeperiod=10)

        roc_outperform_sma = self.feat.sma(roc_outperform, timeperiod=5)

        long_setup = (roc_outperform > roc_outperform_sma) & (close > wma10) & (volume > volume_sma)
        short_setup = (roc_outperform < roc_outperform_sma) & (close < wma10) & (volume > volume_sma)
        exit_setup = self.op.crossed(close, wma10)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
