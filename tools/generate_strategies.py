"""
Multi-thesis strategy generator: 8 thesis groups x 4 timeframes (~800 strategies).
Output: thesis subdirectories in output/ + enhanced index.csv
"""

import os
import csv
from itertools import product

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE, "output")
INDEX_FILE = os.path.join(OUTPUT_DIR, "index.csv")

TIMEFRAMES = [
    ("5min", 5),
    ("15min", 15),
    ("30min", 30),
    ("60min", 60),
]

# Window sizing by timeframe
WINDOWS = {
    5:  {"fast": 8, "mid": 14, "slow": 20, "rsi": 7,  "adx": 7,  "vol": 14},
    15: {"fast": 13, "mid": 26, "slow": 34, "rsi": 10, "adx": 10, "vol": 20},
    30: {"fast": 20, "mid": 40, "slow": 50, "rsi": 14, "adx": 14, "vol": 26},
    60: {"fast": 30, "mid": 60, "slow": 100, "rsi": 21, "adx": 21, "vol": 34},
}

THESIS_IDS = {
    "momentum": 1, "trend": 2, "mean_reversion": 3, "breakout": 4,
    "cross_market": 5, "volume_flow": 6, "intraday_session": 7, "multifactor": 8,
}

DOCSTRING = '''
"""
name:    {name}
summary: {summary}
thesis:  {thesis} | {timeframe}
idea:    {idea}
"""
'''

TEMPLATES = {}


def render(name, summary, thesis, timeframe, idea, template_key, fmt):
    header = DOCSTRING.format(
        name=name, summary=summary, thesis=thesis,
        timeframe=timeframe, idea=idea
    )
    body = TEMPLATES[template_key].format(**fmt)
    return header + body


def filename(alpha_id, name):
    return f"{alpha_id}_{name}.py"


# ================================================================
# TEMPLATES
# ================================================================

TEMPLATES["momentum_pure"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {roc_window}

    def __algorithm__(self):
        close = self.data.pv_close

        roc = self.feat.roc(close, timeperiod=self.roc_window)

        long_setup = roc > 0
        short_setup = roc < 0
        exit_setup = self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["momentum_vol"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {roc_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (roc > 0) & (volume > vol_sma)
        short_setup = (roc < 0) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(roc, 0) | self.op.crossed_above(roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["momentum_vn30"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {roc_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        roc_fut = self.feat.roc(close, timeperiod=self.roc_window)
        roc_vn30 = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (roc_fut > 0) & (roc_vn30 > 0)
        short_setup = (roc_fut < 0) & (roc_vn30 < 0)
        exit_setup = self.op.crossed_below(roc_fut, 0) | self.op.crossed_above(roc_fut, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["momentum_cascade"] = '''\
class CustomStrategy(SimpleAlgorithm):

    fast_window = {fast_window}
    mid_window = {mid_window}
    slow_window = {slow_window}

    def __algorithm__(self):
        close = self.data.pv_close

        roc_fast = self.feat.roc(close, timeperiod=self.fast_window)
        roc_mid = self.feat.roc(close, timeperiod=self.mid_window)
        roc_slow = self.feat.roc(close, timeperiod=self.slow_window)

        long_setup = (roc_fast > roc_mid) & (roc_mid > roc_slow) & (roc_slow > 0)
        short_setup = (roc_fast < roc_mid) & (roc_mid < roc_slow) & (roc_slow < 0)
        exit_setup = self.op.crossed_below(roc_fast, 0) | self.op.crossed_above(roc_fast, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["trend_ma_cross"] = '''\
class CustomStrategy(SimpleAlgorithm):

    fast_window = {fast_window}
    slow_window = {slow_window}

    def __algorithm__(self):
        close = self.data.pv_close

        fast_ma = self.feat.sma(close, timeperiod=self.fast_window)
        slow_ma = self.feat.sma(close, timeperiod=self.slow_window)

        long_setup = self.op.crossed_above(fast_ma, slow_ma)
        short_setup = self.op.crossed_below(fast_ma, slow_ma)
        exit_setup = self.op.crossed_below(fast_ma, slow_ma) | self.op.crossed_above(fast_ma, slow_ma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["trend_macd"] = '''\
class CustomStrategy(SimpleAlgorithm):

    adx_window = {adx_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        macd_line, signal_line, _hist = self.feat.macd(
            close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (macd_line > signal_line) & (adx > 20)
        short_setup = (macd_line < signal_line) & (adx > 20)
        exit_setup = self.op.crossed_below(macd_line, signal_line) | self.op.crossed_above(macd_line, signal_line)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["trend_quantile"] = '''\
class CustomStrategy(SimpleAlgorithm):

    q_window = {mid_window}
    adx_window = {adx_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        upper = self.feat.rolling_quantile(close, self.q_window, 0.75)
        lower = self.feat.rolling_quantile(close, self.q_window, 0.25)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (close > upper) & (adx > 20)
        short_setup = (close < lower) & (adx > 20)
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["trend_ema_adx"] = '''\
class CustomStrategy(SimpleAlgorithm):

    fast_window = {fast_window}
    adx_window = {adx_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ema = self.feat.ema(close, timeperiod=self.fast_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)

        long_setup = (close > ema) & (adx > 20) & (adx < 40)
        short_setup = (close < ema) & (adx > 20) & (adx < 40)
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["meanrev_quantile"] = '''\
class CustomStrategy(SimpleAlgorithm):

    q_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, self.q_window, 0.90)
        lower = self.feat.rolling_quantile(close, self.q_window, 0.10)

        long_setup = close < lower
        short_setup = close > upper
        exit_setup = self.op.crossed_above(close, lower) | self.op.crossed_below(close, upper)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["meanrev_rsi"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        long_setup = rsi < 30
        short_setup = rsi > 70
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["meanrev_bbands"] = '''\
class CustomStrategy(SimpleAlgorithm):

    bbands_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close

        upper, mid_band, lower = self.feat.bbands(
            close, timeperiod=self.bbands_window, nbdevup=2, nbdevdn=2
        )

        long_setup = close < lower
        short_setup = close > upper
        exit_setup = self.op.crossed_above(close, mid_band) | self.op.crossed_below(close, mid_band)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["meanrev_volclimax"] = '''\
class CustomStrategy(SimpleAlgorithm):

    vol_window = {vol_window}
    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)

        vol_spike = volume > vol_sma * 1.5
        downside_climax = vol_spike & (rsi < 25)
        upside_climax = vol_spike & (rsi > 75)

        long_setup = downside_climax
        short_setup = upside_climax
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["breakout_quantile"] = '''\
class CustomStrategy(SimpleAlgorithm):

    q_window = {fast_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, self.q_window, 0.80)
        lower = self.feat.rolling_quantile(close, self.q_window, 0.20)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        long_setup = (close > upper) & (volume > vol_sma)
        short_setup = (close < lower) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["breakout_donchian"] = '''\
class CustomStrategy(SimpleAlgorithm):

    d_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        hh = self.feat.rolling_max(high, window=self.d_window)
        ll = self.feat.rolling_min(low, window=self.d_window)

        long_setup = close > hh
        short_setup = close < ll
        exit_setup = self.op.crossed_below(close, hh) | self.op.crossed_above(close, ll)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["breakout_range"] = '''\
class CustomStrategy(SimpleAlgorithm):

    range_window = {fast_window}
    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        daily_range = high - low
        avg_range = self.feat.sma(daily_range, timeperiod=self.range_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        range_expansion = daily_range > avg_range * 1.5
        vol_confirmation = volume > vol_sma

        long_setup = range_expansion & vol_confirmation & (close > (high + low) / 2)
        short_setup = range_expansion & vol_confirmation & (close < (high + low) / 2)
        exit_setup = (daily_range < avg_range) | (volume < vol_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["breakout_vn30"] = '''\
class CustomStrategy(SimpleAlgorithm):

    q_window = {fast_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        fut_upper = self.feat.rolling_quantile(close, self.q_window, 0.80)
        fut_lower = self.feat.rolling_quantile(close, self.q_window, 0.20)
        vn30_upper = self.feat.rolling_quantile(vn30_close, self.q_window, 0.80)
        vn30_lower = self.feat.rolling_quantile(vn30_close, self.q_window, 0.20)

        long_setup = (close > fut_upper) & (vn30_close > vn30_upper)
        short_setup = (close < fut_lower) & (vn30_close < vn30_lower)
        exit_setup = self.op.crossed_below(close, fut_upper) | self.op.crossed_above(close, fut_lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["cross_relative"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {rsi_window}
    sma_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.sma_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.roc_window)

        long_setup = (ratio > ratio_sma) & (ratio_roc > 0)
        short_setup = (ratio < ratio_sma) & (ratio_roc < 0)
        exit_setup = self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["cross_dji"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)

        long_setup = (dji_roc > 0) & (fut_roc > 0)
        short_setup = (dji_roc < 0) & (fut_roc < 0)
        exit_setup = self.op.crossed_below(fut_roc, 0) | self.op.crossed_above(fut_roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["cross_consensus"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)
        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)

        bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
        bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)

        long_setup = bullish
        short_setup = bearish
        exit_setup = (~bullish) & (~bearish)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["cross_gap"] = '''\
class CustomStrategy(SimpleAlgorithm):

    roc_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        dji_close = self.data.pv_dji_close

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        gap = (open_price / close - 1) * 100
        dji_direction = dji_roc > 0

        long_setup = dji_direction & (gap < 0.5)
        short_setup = (~dji_direction) & (gap > -0.5)
        exit_setup = self.op.crossed_above(gap, 0.5) | self.op.crossed_below(gap, -0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["volume_oi"] = '''\
class CustomStrategy(SimpleAlgorithm):

    oi_window = {slow_window}
    ma_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        close_sma = self.feat.sma(close, timeperiod=self.ma_window)

        oi_trend = oi > oi_sma
        price_trend = close > close_sma

        long_setup = oi_trend & price_trend
        short_setup = oi_trend & (~price_trend)
        exit_setup = (oi < oi_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["volume_matched_surge"] = '''\
class CustomStrategy(SimpleAlgorithm):

    vol_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window)
        vol_q80 = self.feat.rolling_quantile(matched_vol, self.vol_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.vol_window)

        surge = (matched_vol > vol_sma * 1.5) & (matched_vol > vol_q80)

        long_setup = surge & (close > close_sma)
        short_setup = surge & (close < close_sma)
        exit_setup = (matched_vol < vol_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["volume_value"] = '''\
class CustomStrategy(SimpleAlgorithm):

    val_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        matched_val = self.data.fut_matched_value_vn30f1m_1d

        val_sma = self.feat.sma(matched_val, timeperiod=self.val_window)
        val_q80 = self.feat.rolling_quantile(matched_val, self.val_window, 0.80)
        close_sma = self.feat.sma(close, timeperiod=self.val_window)

        flow = (matched_val > val_q80) & (matched_val > val_sma * 1.3)

        long_setup = flow & (close > close_sma)
        short_setup = flow & (close < close_sma)
        exit_setup = (matched_val < val_sma) | self.op.crossed_below(close, close_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["volume_obv"] = '''\
class CustomStrategy(SimpleAlgorithm):

    obv_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)

        long_setup = (obv > obv_sma) & (close > close_sma)
        short_setup = (obv < obv_sma) & (close < close_sma)
        exit_setup = self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["intraday_open_drive"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        open_range = (close - open_price) / open_price * 100
        candle_range = high - low
        avg_range = self.feat.sma(candle_range, timeperiod=self.rsi_window)

        expanding_range = candle_range > avg_range
        bullish_drive = (open_range > 0.3) & expanding_range & (rsi > 50) & (rsi < 70)
        bearish_drive = (open_range < -0.3) & expanding_range & (rsi < 50) & (rsi > 30)

        long_setup = bullish_drive
        short_setup = bearish_drive
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["intraday_revert"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        open_price = self.data.pv_open

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        mid_price = (high + low) / 2
        extreme_band = (high - low) * 0.8

        long_setup = (rsi < 30) & (close < (mid_price - extreme_band))
        short_setup = (rsi > 70) & (close > (mid_price + extreme_band))
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["intraday_close"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        roc = self.feat.roc(close, timeperiod=self.rsi_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        squeeze = (rsi > 50) & (rsi < 70) & (roc > 0) & (volume > vol_sma)

        long_setup = squeeze
        short_setup = (rsi < 50) & (rsi > 30) & (roc < 0) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["intraday_gapfill"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open

        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        gap = (open_price / close - 1) * 100

        gap_up = gap > 0.3
        gap_down = gap < -0.3
        filling_down = gap_up & (close < open_price) & (rsi < 60)
        filling_up = gap_down & (close > open_price) & (rsi > 40)

        long_setup = filling_up
        short_setup = filling_down
        exit_setup = self.op.crossed_above(abs(gap), 0.1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["multifactor_zscore"] = '''\
class CustomStrategy(SimpleAlgorithm):

    z_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.rolling_zscore(volume, window=self.z_window)
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        adx = self.feat.adx(high, low, close, timeperiod={adx_window})

        momentum = self.feat.roc(close, timeperiod={rsi_window})
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        trend_ok = adx > 20
        rsi_ok = (rsi > 30) & (rsi < 70)

        long_setup = (composite > 1.5) & trend_ok & rsi_ok
        short_setup = (composite < -1.5) & trend_ok & rsi_ok
        exit_setup = (abs(composite) < 0.5) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["multifactor_momentum"] = '''\
class CustomStrategy(SimpleAlgorithm):

    rsi_window = {rsi_window}
    roc_window = {fast_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        roc = self.feat.roc(close, timeperiod=self.roc_window)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        adx = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod=self.rsi_window)

        morning_momentum = (roc > 0) & (rsi > 50) & (rsi < 65)
        volume_confirm = volume > vol_sma
        trend_confirm = adx > 20

        long_setup = morning_momentum & volume_confirm & trend_confirm
        short_setup = (roc < 0) & (rsi < 50) & (rsi > 35) & volume_confirm & trend_confirm
        exit_setup = self.op.crossed_below(rsi, 50) | self.op.crossed_above(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["multifactor_trendvol"] = '''\
class CustomStrategy(SimpleAlgorithm):

    mid_window = {mid_window}
    vol_window = {vol_window}
    adx_window = {adx_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        ema = self.feat.ema(close, timeperiod=self.mid_window)
        adx = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.vol_window)

        trend_ok = close > ema
        strength_ok = (adx > 20) & (adx < 45)
        volume_ok = volume > vol_sma
        vn30_confirm = vn30_roc > 0

        long_setup = trend_ok & strength_ok & volume_ok & vn30_confirm
        short_setup = (~trend_ok) & strength_ok & volume_ok & (~vn30_confirm)
        exit_setup = self.op.crossed_below(close, ema) | (adx < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''


# ================================================================
# STRATEGY DEFINITIONS
# ================================================================

def build_strategies():
    """Yield (thesis, timeframe, alpha_id, name, summary, idea, template_key, fmt) for each strategy."""
    alpha_counter = 0

    for tf_label, tf_min in TIMEFRAMES:
        w = WINDOWS[tf_min]
        tf_subdir = tf_label

        # --- Thesis 01: Momentum ---
        thesis = "momentum"
        t = THESIS_IDS[thesis]

        # 1a: Pure Price Momentum
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MomPure_{tf_label}", \
            f"Long/short on momentum signal (ROC {w['fast']}) — {tf_label}", \
            "Pure price momentum: ROC signals direction", "momentum_pure", \
            {"roc_window": w['fast']}

        # 1b: Volume-Momentum
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MomVol_{tf_label}", \
            f"Momentum confirmed by volume — {tf_label}", \
            "Momentum with volume confirmation", "momentum_vol", \
            {"roc_window": w['fast'], "vol_window": w['vol']}

        # 1c: VN30 Momentum Confirm
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MomVN30_{tf_label}", \
            f"Futures + VN30 momentum alignment — {tf_label}", \
            "Cross-market momentum confirmation with VN30", "momentum_vn30", \
            {"roc_window": w['fast']}

        # 1d: Cascade Momentum
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MomCascade_{tf_label}", \
            f"Acceleration: short > mid > long ROC — {tf_label}", \
            "Cascade momentum: acceleration structure", "momentum_cascade", \
            {"fast_window": w['fast'], "mid_window": w['mid'], "slow_window": w['slow']}

        # --- Thesis 02: Trend Following ---
        thesis = "trend"
        t = THESIS_IDS[thesis]

        # 2a: MA Crossover
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"TrendMACross_{tf_label}", \
            f"MA crossover with timeframe-optimized windows — {tf_label}", \
            "Trend following with moving average crossover", "trend_ma_cross", \
            {"fast_window": w['fast'], "slow_window": w['slow']}

        # 2b: MACD + ADX
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"TrendMACD_{tf_label}", \
            f"MACD trend confirmation with ADX filter — {tf_label}", \
            "MACD + ADX trend trend strength filter", "trend_macd", \
            {"adx_window": w['adx']}

        # 2c: Quantile Trend
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"TrendQuantile_{tf_label}", \
            f"Price vs quantile trend channel with ADX — {tf_label}", \
            "Trend following using quantile channel + ADX", "trend_quantile", \
            {"mid_window": w['mid'], "adx_window": w['adx']}

        # 2d: EMA + ADX
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"TrendEMA_{tf_label}", \
            f"EMA trend filter with ADX strength band — {tf_label}", \
            "EMA trend with ADX non-exhaustion filter", "trend_ema_adx", \
            {"fast_window": w['fast'], "adx_window": w['adx']}

        # --- Thesis 03: Mean Reversion ---
        thesis = "mean_reversion"
        t = THESIS_IDS[thesis]

        # 3a: Quantile Reversion
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MRQuantile_{tf_label}", \
            f"Mean reversion at Q90/Q10 extremes — {tf_label}", \
            "Mean reversion using quantile extremes", "meanrev_quantile", \
            {"mid_window": w['mid']}

        # 3b: RSI Extreme
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MRRSI_{tf_label}", \
            f"RSI extreme reversion (30/70) — {tf_label}", \
            "RSI-based mean reversion at extremes", "meanrev_rsi", \
            {"rsi_window": w['rsi']}

        # 3c: BBands Reversion
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MRBBands_{tf_label}", \
            f"Bollinger Band reversion (2 STD) — {tf_label}", \
            "Mean reversion using Bollinger Bands", "meanrev_bbands", \
            {"mid_window": w['mid']}

        # 3d: Volume Climax Reversal
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MRVolClimax_{tf_label}", \
            f"Volume climax reversal at RSI extremes — {tf_label}", \
            "Volume climax + RSI extreme reversal", "meanrev_volclimax", \
            {"vol_window": w['vol'], "rsi_window": w['rsi']}

        # --- Thesis 04: Breakout ---
        thesis = "breakout"
        t = THESIS_IDS[thesis]

        # 4a: Quantile Breakout
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"BOQuantile_{tf_label}", \
            f"Quantile breakout (Q80/Q20) with volume confirm — {tf_label}", \
            "Breakout signal using quantile channel + volume", "breakout_quantile", \
            {"fast_window": w['fast'], "vol_window": w['vol']}

        # 4b: Donchian Breakout
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"BODonchian_{tf_label}", \
            f"Donchian channel breakout — {tf_label}", \
            "Breakout using Donchian channel (HH/LL)", "breakout_donchian", \
            {"mid_window": w['mid']}

        # 4c: Range Expansion
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"BORange_{tf_label}", \
            f"Range expansion breakout with volume — {tf_label}", \
            "Breakout detection via range expansion", "breakout_range", \
            {"fast_window": w['fast'], "vol_window": w['vol']}

        # 4d: VN30 Breakout Confirm
        alpha_counter += 1
        yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"BOVN30_{tf_label}", \
            f"Futures + VN30 simultaneous breakout — {tf_label}", \
            "Dual-market breakout confirmation", "breakout_vn30", \
            {"fast_window": w['fast']}

        # --- Thesis 05: Cross-Market (only 15, 30, 60 min) ---
        if tf_min >= 15:
            thesis = "cross_market"
            t = THESIS_IDS[thesis]

            # 5a: Relative Strength (futures vs VN30)
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"XMRelative_{tf_label}", \
                f"Futures/VN30 relative strength trend — {tf_label}", \
                "Cross-market relative strength", "cross_relative", \
                {"rsi_window": w['rsi'], "mid_window": w['mid']}

            # 5b: DJI Spillover
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"XMDJI_{tf_label}", \
                f"Dow Jones momentum spillover — {tf_label}", \
                "Global momentum spillover from DJI", "cross_dji", \
                {"rsi_window": w['rsi']}

            # 5c: Multi-Market Consensus
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"XMConsensus_{tf_label}", \
                f"3-market consensus (Futures+VN30+DJI) — {tf_label}", \
                "Multi-market consensus for high-confidence signals", "cross_consensus", \
                {"rsi_window": w['rsi']}

            # 5d: Overnight Gap
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"XMGap_{tf_label}", \
                f"Overnight gap play from DJI — {tf_label}", \
                "Overnight gap capture using DJI direction", "cross_gap", \
                {"rsi_window": w['rsi']}

        # --- Thesis 06: Volume & Flow (only 15, 30, 60 min) ---
        if tf_min >= 15:
            thesis = "volume_flow"
            t = THESIS_IDS[thesis]

            # 6a: Open Interest Trend
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"VFOI_{tf_label}", \
                f"Open Interest trend confirmation — {tf_label}", \
                "Institutional flow via Open Interest trend", "volume_oi", \
                {"slow_window": w['slow'], "mid_window": w['mid']}

            # 6b: Matched Volume Surge
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"VFVolSurge_{tf_label}", \
                f"Matched volume surge detection — {tf_label}", \
                "Volume surge from matched volume", "volume_matched_surge", \
                {"vol_window": w['vol']}

            # 6c: Matched Value Spike
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"VFValSpike_{tf_label}", \
                f"Matched value spike — {tf_label}", \
                "Institutional value flow spike detection", "volume_value", \
                {"vol_window": w['vol']}

            # 6d: OBV Flow
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"VFOBV_{tf_label}", \
                f"OBV cumulative flow trend — {tf_label}", \
                "On-Balance Volume cumulative flow", "volume_obv", \
                {"mid_window": w['mid']}

        # --- Thesis 07: Intraday Session (only 5, 15 min) ---
        if tf_min <= 15:
            thesis = "intraday_session"
            t = THESIS_IDS[thesis]

            # 7a: Morning Open Drive
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"ISMOpen_{tf_label}", \
                f"Morning open drive momentum — {tf_label}", \
                "Intraday morning session momentum", "intraday_open_drive", \
                {"rsi_window": w['rsi']}

            # 7b: Lunch Mean Reversion
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"ISMLunch_{tf_label}", \
                f"Mid-session mean reversion — {tf_label}", \
                "Intraday mean reversion during lunch session", "intraday_revert", \
                {"rsi_window": w['rsi']}

            # 7c: Close Window Squeeze
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"ISMClose_{tf_label}", \
                f"Close window momentum squeeze — {tf_label}", \
                "End-of-session position squeeze capture", "intraday_close", \
                {"rsi_window": w['rsi']}

            # 7d: Gap Fill
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"ISMGap_{tf_label}", \
                f"Intraday gap fill — {tf_label}", \
                "Intraday gap fill pattern trading", "intraday_gapfill", \
                {"rsi_window": w['rsi']}

        # --- Thesis 08: Multi-Factor (only 15, 30, 60 min) ---
        if tf_min >= 15:
            thesis = "multifactor"
            t = THESIS_IDS[thesis]

            # 8a: Z-score Composite
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MFZScore_{tf_label}", \
                f"Multi-factor z-score composite — {tf_label}", \
                "Composite multi-factor signal using z-scores", "multifactor_zscore", \
                {"mid_window": w['mid'], "rsi_window": w['rsi'], "adx_window": w['adx']}

            # 8b: Morning + Momentum
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MFMom_{tf_label}", \
                f"Momentum + volume + trend multi-layer — {tf_label}", \
                "Multi-factor momentum with confirmation layers", "multifactor_momentum", \
                {"rsi_window": w['rsi'], "fast_window": w['fast'], "adx_window": w['adx']}

            # 8c: Trend + Volume + VN30
            alpha_counter += 1
            yield thesis, tf_subdir, f"{t:02d}-{alpha_counter:03d}", f"MFTrendVol_{tf_label}", \
                f"4-layer: trend + strength + volume + VN30 — {tf_label}", \
                "Multi-factor trend with 4-layer confirmation", "multifactor_trendvol", \
                {"mid_window": w['mid'], "vol_window": w['vol'], "adx_window": w['adx']}


def main():
    index_rows = []

    for thesis, tf_subdir, alpha_id, name, summary, idea, template_key, fmt in build_strategies():
        t_id = THESIS_IDS[thesis]
        thesis_dir = f"thesis_{t_id:02d}_{thesis}"
        filepath = os.path.join(OUTPUT_DIR, thesis_dir, tf_subdir, filename(alpha_id, name))

        os.makedirs(os.path.join(OUTPUT_DIR, thesis_dir, tf_subdir), exist_ok=True)

        code = render(name, summary, thesis, tf_subdir, idea, template_key, fmt)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        direction = "BOTH"
        index_rows.append({
            "alpha_id": alpha_id,
            "thesis_group": thesis_dir,
            "timeframe": tf_subdir,
            "direction": direction,
            "thesis_id": t_id,
            "file": os.path.join(thesis_dir, tf_subdir, filename(alpha_id, name)),
            "name": name,
            "summary": summary,
        })

    # Write index.csv
    fieldnames = ["alpha_id", "thesis_group", "timeframe", "direction", "thesis_id", "file", "name", "summary"]
    with open(INDEX_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(index_rows)

    print(f"Generated {len(index_rows)} strategies.")
    print(f"Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
