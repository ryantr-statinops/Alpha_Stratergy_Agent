"""
name:    VNFutureMeanQuantileRSI
summary: Trade VN30F1M when price breaks quantile channel with mean trend
         filter and RSI momentum confirmation.
idea:    Rolling quantile defines adaptive support/resistance, rolling mean
         provides trend context, and RSI confirms momentum direction.
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        # =====================================================
        # STEP 1: Raw Market Data
        # =====================================================

        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        # =====================================================
        # STEP 2: Feature Engineering
        # =====================================================

        mean_14 = self.feat.rolling_mean(close, window=14)

        upper_q = self.feat.rolling_quantile(close, 14, 0.8)
        lower_q = self.feat.rolling_quantile(close, 14, 0.2)

        rsi = self.feat.rsi(close, timeperiod=14)

        # =====================================================
        # STEP 3: Trading Logic
        # =====================================================

        long_setup = (
            (close > upper_q)
            & (close > mean_14)
            & (rsi > 50)
        )

        short_setup = (
            (close < lower_q)
            & (close < mean_14)
            & (rsi < 50)
        )

        exit_long = (close < mean_14) | (rsi < 40)
        exit_short = (close > mean_14) | (rsi > 60)
        exit_setup = exit_long | exit_short

        # =====================================================
        # STEP 4: Position Sizing
        # =====================================================

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
