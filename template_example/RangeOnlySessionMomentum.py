"""
name:    RangesOnlySessionMomentum
summary: Trade intraday momentum only inside the regular session windows
         and force flat near the lunch break and ATC/end window.
idea:    Session ranges keep signals away from thin or closing periods.
         Momentum and ADX decide direction, while range gates handle
         trading hours only.
"""


class CustomStrategy(SimpleAlgorithm):
    # Ranges-only example. Do not combine with exact times or candle-age exits.
    # VN local 09:00-11:30 and 13:00-14:45 are UTC 02:00-04:30 and 06:00-07:45.
    position_open_ranges = ["02:00-04:30", "06:00-07:45"]
    position_close_ranges = ["04:20-04:30", "07:30-07:45"]

    def __algorithm__(self):
        # self.data exposes aligned pandas Series such as futures OHLCV and VN30 OHLCV.
        # Assign each field to a short local name so later signal rules are readable.
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        # self.feat methods return causal indicator Series; use keyword args to match docs.
        adx = self.feat.adx(high, low, close, timeperiod=14)
        impulse = self.feat.roc(close, timeperiod=3)
        ema_fast = self.feat.ema(close, timeperiod=13)
        ema_slow = self.feat.ema(close, timeperiod=34)

        # Direction is allowed only when trend strength and EMA regime agree.
        long_setup = (impulse > 0) & (adx > 20) & (ema_fast > ema_slow)
        short_setup = (impulse < 0) & (adx > 20) & (ema_fast < ema_slow)
        exit_setup = adx < 16

        # set_positions writes target exposure where the condition is true.
        # Exit rules are usually called first so entries can override after filters.
        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=0.75)
        self.set_positions(short_setup, position=-1)