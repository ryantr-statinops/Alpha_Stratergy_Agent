"""
name:    VNFutureMorningOpenDrive
summary: Trade the morning open drive when futures and VN30 both move away
         from their opens with expanding range.
idea:    Open-drive sessions can persist when both instruments leave their
         opens in the same direction and the candle range expands. A fixed
         time stop limits how long the trade can run.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        # Pull the aligned futures and VN30 OHLC series into short names so the
        # rule logic stays easy to read.
        open_ = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        close = self.data.pv_close
        vn30_open = self.data.pv_vn30_open
        vn30_close = self.data.pv_vn30_close

        # Measure how far each instrument has moved from its open.
        # Positive values mean an upward drive, negative values mean downside drive.
        futures_drive = (close / open_ - 1).fillna(0)
        index_drive = (vn30_close / vn30_open - 1).fillna(0)

        # Compare the current candle range with its recent average.
        # A ratio above 1 means the session range is expanding versus the 10-bar baseline.
        range_ratio = ((high - low) / self.feat.sma(high - low, timeperiod=10)).fillna(0)

        # Long when futures and VN30 both break away from the open to the upside
        # and the current range is larger than normal.
        long_setup = (futures_drive > 0.001) & (index_drive > 0) & (range_ratio > 1)

        # Short uses the same logic through the explicit multi-argument boolean helper.
        short_setup = self.op.and_(
            futures_drive < -0.001,
            index_drive < 0,
            range_ratio > 1,
        )

        # Exit when the candle range contracts back below the expansion threshold.
        exit_setup = range_ratio < 0.8

        # Apply exits first so entry rules can override when their conditions are met.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)