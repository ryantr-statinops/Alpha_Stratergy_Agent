"""
name:    T01-F_z10_e2.0
summary: Z-Score Mean Reversion
idea:    Bet on over-extensions via rolling z-score; long when deeply negative, short when deeply positive; exit near neutral.
"""
class CustomStrategy(SimpleAlgorithm):
    z_window = 10


    def __algorithm__(self):
        close = self.data.pv_close

        price_z = self.feat.rolling_zscore(close, window=self.z_window)

        long_setup = price_z < -2.0
        short_setup = price_z > 2.0
        exit_setup = self.op.between(price_z, -1, 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

