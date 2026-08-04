"""
name:    VnLargeMacdTrend
summary: Long large caps when the MACD line leads its signal over a rising
         8/24 EMA trend.
idea:    MACD on 8/21/5 confirms accelerating momentum while the EMA stack
         defines the trend regime. RSI9 and SMA10 volume only confirm full
         exposure, while the MACD signal-line cross controls momentum entry and
         exit according to the feature's multi-output contract.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        ema_fast = self.feat.ema(close, timeperiod=8)
        ema_slow = self.feat.ema(close, timeperiod=24)
        rsi = self.feat.rsi(close, timeperiod=9)
        volume_base = self.feat.sma(volume, timeperiod=10)
        macd, macd_signal, _hist = self.feat.macd(
            close,
            fastperiod=8,
            slowperiod=21,
            signalperiod=5,
        )

        base_entry = (macd > macd_signal) & (ema_fast > ema_slow)
        strong_entry = (
            base_entry
            & (close > ema_slow)
            & (rsi > 48)
            & (rsi < 75)
            & (volume > volume_base)
        )
        exit_setup = (macd < macd_signal) | (ema_fast < ema_slow)

        self.set_positions(exit_setup, position=0)
        self.set_positions(base_entry, position=0.5)
        self.set_positions(strong_entry, position=1)
