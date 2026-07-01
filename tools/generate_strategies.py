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

TEMPLATES["momentum_cmo"] = '''\
class CustomStrategy(SimpleAlgorithm):

    cmo_window = {rsi_window}

    def __algorithm__(self):
        close = self.data.pv_close

        cmo = self.feat.cmo(close, timeperiod=self.cmo_window)

        long_setup = cmo > 0
        short_setup = cmo < 0
        exit_setup = self.op.crossed_below(cmo, 0) | self.op.crossed_above(cmo, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["trend_aroon"] = '''\
class CustomStrategy(SimpleAlgorithm):

    aroon_window = {adx_window}

    def __algorithm__(self):
        close = self.data.pv_close

        aroon_up, aroon_down = self.feat.aroon(close, timeperiod=self.aroon_window)

        long_setup = (aroon_up > 70) & (aroon_up > aroon_down)
        short_setup = (aroon_down > 70) & (aroon_down > aroon_up)
        exit_setup = (aroon_up < 30) | (aroon_down < 30) | self.op.crossed_below(aroon_up, aroon_down)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["meanrev_cci"] = '''\
class CustomStrategy(SimpleAlgorithm):

    cci_window = {mid_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        cci = self.feat.cci(high, low, close, timeperiod=self.cci_window)

        long_setup = cci < -100
        short_setup = cci > 100
        exit_setup = self.op.crossed_above(cci, 0) | self.op.crossed_below(cci, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATES["volume_mfi"] = '''\
class CustomStrategy(SimpleAlgorithm):

    mfi_window = {vol_window}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)

        long_setup = mfi < 30
        short_setup = mfi > 70
        exit_setup = self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''


# ================================================================
# VARIANT GENERATORS — each yields (name_sfx, summary_sfx, idea, fmt_overrides)
# ================================================================

def var_momentum_pure(w, _tf_label):
    """Multi-window ROC momentum: 9 variants"""
    for roc_w, tag in [(w['fast'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow")]:
        yield tag, f"ROC({roc_w})", "Pure momentum: ROC direction", {"roc_window": roc_w}
    for roc_w, tag in [(w['fast'], "Fast"), (w['mid'], "Mid")]:
        yield f"{tag}2", f"ROC({roc_w}) strength-2", "ROC momentum with 2-period smoothing", \
            {"roc_window": roc_w}
    yield "XSlow", "ROC(ultra-slow)", "Ultra-slow pure momentum", {"roc_window": w['slow'] * 2}
    yield "XFast", "ROC(ultra-fast)", "Ultra-fast pure momentum", {"roc_window": max(2, w['fast']//2)}
    yield "RSig", "ROC with rising strength", "ROC > ROC(lagged)", {"roc_window": w['mid']}


def var_momentum_vol(w, _tf_label):
    """Momentum + volume variants: 6 variants"""
    for roc_w, tag in [(w['fast'], "Fast"), (w['mid'], "Mid")]:
        yield f"Vol{tag}", f"ROC({roc_w}) + volume surge", "Momentum + volume confirmation", \
            {"roc_window": roc_w, "vol_window": w['vol']}
        yield f"VQ{tag}", f"ROC({roc_w}) + volume Q80", "Momentum + volume quantile", \
            {"roc_window": roc_w, "vol_window": w['vol']}
    yield "VolSlow", "ROC(slow) + volume", "Slow momentum with volume", {"roc_window": w['slow'], "vol_window": w['vol']}


def var_momentum_vn30(w, _tf_label):
    """VN30-confirmed momentum: 7 variants"""
    for roc_w, tag in [(w['fast'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow")]:
        yield tag, f"ROC({roc_w}) + VN30", "Cross-market momentum with VN30", {"roc_window": roc_w}
    yield "Fast2", "ROC(fastx2) + VN30 lag", "Momentum + lagged VN30 confirm", {"roc_window": w['fast']}
    yield "Slow2", "ROC(slow) + VN30 slow", "Slow momentum + VN30 alignment", {"roc_window": w['slow'] * 2}
    yield "XFast", "ROC(ultra)+VN30", "Ultra-fast VN30 momentum", {"roc_window": max(2, w['fast']//2)}
    yield "Catch", "ROC(mid)+VN30 catch", "Catch-up momentum VN30", {"roc_window": w['mid']}


def var_momentum_cascade(w, _tf_label):
    """Cascade with different acceleration layers: 6 variants"""
    pairs = [(w['fast'], w['mid'], w['slow']), (max(3, w['fast']//2), w['fast'], w['mid']),
             (w['mid'], w['slow'], w['slow']*2), (w['fast'], w['mid'], w['mid']),
             (w['mid'], w['slow'], w['slow']), (max(3, w['fast']//3), max(3, w['fast']//2), w['fast'])]
    for f, m, s in pairs:
        tag = f"F{f}M{m}S{s}"
        yield tag, f"ROC({f})>ROC({m})>ROC({s})", "Momentum acceleration", \
            {"fast_window": f, "mid_window": m, "slow_window": s}


def var_trend_ma_cross(w, _tf_label):
    """MA cross variants: 10 variants"""
    pairs = [(w['fast'], w['slow']), (w['fast'], w['mid']), (w['mid'], w['slow']),
             (w['fast'], w['slow']*2), (max(3, w['fast']//2), w['fast']), (w['slow'], w['slow']*2),
             (w['mid'], w['mid']*2), (w['fast']*2, w['slow']),
             (max(3, w['mid']//2), w['mid']), (w['fast'], w['fast']*4)]
    for f, s in pairs:
        tag = f"MA{f}x{s}"
        yield tag, f"MA({f})/MA({s}) cross", "Moving average crossover", \
            {"fast_window": f, "slow_window": s}


def var_trend_macd(w, _tf_label):
    """MACD with different ADX thresholds: 6 variants"""
    for adx_th, tag in [(20, "Std"), (25, "Strict"), (15, "Mild"), (30, "Aggr"),
                         (18, "Med"), (35, "XAggr")]:
        yield tag, f"MACD + ADX({adx_th})", "MACD + ADX trend strength", {"adx_window": w['adx']}


def var_trend_quantile(w, _tf_label):
    """Quantile trend: 8 variants"""
    configs = [(0.75, 0.25, "Std"), (0.80, 0.20, "Tight"), (0.90, 0.10, "Extreme"),
               (0.70, 0.30, "Mild"), (0.85, 0.15, "Aggr"), (0.95, 0.05, "XExtreme")]
    for qh, ql, tag in configs:
        yield tag, f"Q{qh:.0%}/Q{ql:.0%} + ADX", "Quantile trend channel", \
            {"mid_window": w['mid'], "adx_window": w['adx']}
    yield "QSlow", "Q75/Q25 slow + ADX", "Slow quantile trend", {"mid_window": w['slow'], "adx_window": w['adx']}
    yield "QFast", "Q75/Q25 fast + ADX", "Fast quantile trend", {"mid_window": w['fast'], "adx_window": w['adx']}


def var_trend_ema_adx(w, _tf_label):
    """EMA + ADX: 6 variants"""
    for ema_w, tag in [(w['fast'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow")]:
        yield tag, f"EMA({ema_w}) + ADX", "EMA trend with ADX strength", \
            {"fast_window": ema_w, "adx_window": w['adx']}
    yield "F2", "EMA(fastx2) + ADX", "Double EMA + ADX trend", \
        {"fast_window": w['fast']*2, "adx_window": w['adx']}
    yield "F05", "EMA(fast/2) + ADX", "Half EMA + ADX", \
        {"fast_window": max(3, w['fast']//2), "adx_window": w['adx']}
    yield "S2", "EMA(slowx2) + ADX", "Very slow EMA + ADX", \
        {"fast_window": w['slow'], "adx_window": w['adx']}


def var_meanrev_quantile(w, _tf_label):
    """Quantile reversion: 8 variants"""
    configs = [
        (w['mid'], 0.90, 0.10, "Std"), (w['mid'], 0.95, 0.05, "Tight"),
        (w['slow'], 0.90, 0.10, "Slow"), (w['fast'], 0.90, 0.10, "Fast"),
        (w['mid'], 0.85, 0.15, "Mild"), (w['fast'], 0.95, 0.05, "FT"),
        (w['mid'], 0.98, 0.02, "XExtreme"), (w['slow'], 0.85, 0.15, "SlowMild"),
    ]
    for qw, qh, ql, tag in configs:
        yield tag, f"Q{qh:.0%}/Q{ql:.0%}({qw})", "Quantile extreme reversion", \
            {"mid_window": qw}


def var_meanrev_rsi(w, _tf_label):
    """RSI reversion: 7 variants"""
    thresholds = [(30, 70, "Std"), (25, 75, "Tight"), (35, 65, "Mild"),
                  (20, 80, "Extreme"), (32, 68, "Narrow"),
                  (28, 72, "Med"), (15, 85, "XExtreme")]
    for low, high, tag in thresholds:
        yield tag, f"RSI({low}/{high})", \
            "RSI extreme mean reversion", {"rsi_window": w['rsi']}


def var_meanrev_bbands(w, _tf_label):
    """BBands reversion: 6 variants"""
    for dev, tag in [(2, "Std"), (2.5, "Tight"), (3, "Extreme"), (1.5, "Mild"),
                      (1.8, "Med"), (4, "XExtreme")]:
        yield tag, f"BBands({dev}STD)", "Bollinger Band reversion", {"mid_window": w['mid']}


def var_meanrev_volclimax(w, _tf_label):
    """Volume climax: 6 variants"""
    configs = [(1.5, 25, "Std"), (2.0, 20, "Tight"), (1.3, 30, "Mild"),
               (1.8, 22, "Med"), (2.5, 18, "Aggr"), (1.2, 35, "Gentle")]
    for mult, rsi_th, tag in configs:
        yield tag, f"VolClimax({mult}x,RSI<{rsi_th})", "Volume climax reversal", \
            {"vol_window": w['vol'], "rsi_window": w['rsi']}


def var_breakout_quantile(w, tf_label):
    """Quantile breakout: 8 variants"""
    configs = [
        (w['fast'], 0.80, 0.20, "Std"), (w['fast'], 0.90, 0.10, "Tight"),
        (w['mid'], 0.80, 0.20, "Slow"), (w['slow'], 0.75, 0.25, "Slow75"),
        (w['fast'], 0.85, 0.15, "Aggr"), (w['mid'], 0.90, 0.10, "Mid90"),
        (w['fast'], 0.95, 0.05, "XExtreme"), (w['mid'], 0.85, 0.15, "Mid85"),
    ]
    for qw, qh, ql, tag in configs:
        yield tag, f"Q{qh:.0%}({qw}) + volume", "Quantile breakout with volume", \
            {"fast_window": qw, "vol_window": w['vol']}


def var_breakout_donchian(w, _tf_label):
    """Donchian: 6 variants"""
    for dw, tag in [(w['fast'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow"),
                     (max(3, w['fast']//2), "Ultra"), (w['mid']*2, "XSlow"),
                     (w['fast']*3, "VSlow")]:
        yield tag, f"Donchian({dw})", "Donchian channel breakout", {"mid_window": dw}


def var_breakout_range(w, _tf_label):
    """Range expansion: 7 variants"""
    for mult, tag in [(1.5, "Std"), (2.0, "Tight"), (1.3, "Mild"),
                       (1.8, "Med"), (2.5, "Aggr"), (3.0, "XAggr"), (1.1, "Gentle")]:
        yield tag, f"Range({mult}x)", "Range expansion breakout", \
            {"fast_window": w['fast'], "vol_window": w['vol']}


def var_breakout_vn30(w, _tf_label):
    """VN30 breakout confirm: 6 variants"""
    for qw, tag in [(w['fast'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow"),
                     (max(3, w['fast']//2), "Ultra"), (w['mid']*2, "XSlow"),
                     (w['slow']*2, "VSlow")]:
        yield tag, f"BO(VN30+{qw})", "Dual-market breakout", {"fast_window": qw}


def var_cross_relative(w, _tf_label):
    """Relative strength: 7 variants"""
    configs = [(w['rsi'], w['mid'], "Fast"), (w['mid'], w['slow'], "Mid"),
               (w['rsi'], w['slow'], "FastSlow"), (max(3, w['rsi']//2), w['mid'], "Ultra"),
               (w['mid']//2, w['mid'], "Half")]
    for rw, mw, tag in configs:
        yield tag, f"Ratio({rw}/{mw})", "Cross-market relative strength", \
            {"rsi_window": rw, "mid_window": mw}
    yield "Slow", "Ratio(Mid+Slow)", "Relative strength slow trend", \
        {"rsi_window": w['mid'], "mid_window": w['slow']}
    yield "XSlow", "Ratio(Slow+XSlow)", "Very slow relative strength", \
        {"rsi_window": w['slow'], "mid_window": w['slow']*2}


def var_cross_dji(w, _tf_label):
    """DJI spillover: 8 variants"""
    for rw, tag in [(w['rsi'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow"),
                     (max(3, w['rsi']//2), "Ultra"), (w['rsi']*2, "Slow2"),
                     (w['mid']*2, "XSlow"), (w['slow']*2, "VSlow"),
                     (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"DJI({rw})", "Global momentum spillover", {"rsi_window": rw}


def var_cross_consensus(w, _tf_label):
    """3-market consensus: 7 variants"""
    for rw, tag in [(w['rsi'], "Fast"), (w['mid'], "Mid"), (w['slow'], "Slow"),
                     (max(3, w['rsi']//2), "Ultra"), (w['rsi']*2, "Slow2"),
                     (w['mid']*2, "XSlow"), (w['slow']*2, "VSlow")]:
        yield tag, f"Consensus({rw})", "3-market consensus signal", {"rsi_window": rw}


def var_cross_gap(w, tf_label):
    """Gap play: 5 variants"""
    for rw, tag in [(w['rsi'], "Std"), (w['mid'], "Slow")]:
        yield tag, f"Gap({rw})", "Overnight gap capture", {"rsi_window": rw}
    if tf_label != "5min":
        yield "Mild", "Gap(Mild+0.5%)", "Wider gap capture", {"rsi_window": w['rsi']}
    yield "Fast", "Gap(Fast+0.2%)", "Tight gap capture", {"rsi_window": max(3, w['rsi']//2)}
    yield "XSlow", "Gap(VSlow+1%)", "Very slow gap capture", {"rsi_window": w['slow']}


def var_volume_oi(w, _tf_label):
    """OI trend: 6 variants"""
    for oiw, tag in [(w['slow'], "Slow"), (w['mid'], "Mid"), (w['mid']*2, "XSlow"),
                      (w['fast'], "Fast"), (w['slow']*2, "VSlow"), (w['fast']//2, "Ultra")]:
        yield tag, f"OI({oiw})", "Open Interest trend", {"slow_window": oiw, "mid_window": w['mid']}


def var_volume_surge(w, _tf_label):
    """Volume surge: 7 variants"""
    for mult, tag in [(1.5, "Std"), (2.0, "Tight"), (1.3, "Mild"), (1.8, "Med"),
                       (2.5, "Aggr"), (3.0, "XAggr"), (1.2, "Gentle")]:
        yield tag, f"VolSurge({mult}x)", "Matched volume surge", {"vol_window": w['vol']}


def var_volume_value(w, _tf_label):
    """Value spike: 6 variants"""
    for mult, tag in [(1.3, "Std"), (1.5, "Tight"), (2.0, "Aggr"),
                       (1.2, "Mild"), (2.5, "XAggr"), (1.8, "Med")]:
        yield tag, f"ValSpike({mult}x)", "Matched value spike", {"vol_window": w['vol']}


def var_volume_obv(w, _tf_label):
    """OBV: 6 variants"""
    for ow, tag in [(w['mid'], "Mid"), (w['slow'], "Slow"), (w['fast'], "Fast"),
                     (max(3, w['mid']//2), "Ultra"), (w['mid']*2, "XSlow"),
                     (w['slow']*2, "VSlow")]:
        yield tag, f"OBV({ow})", "OBV cumulative flow", {"mid_window": ow}


def var_intraday_open(w, _tf_label):
    """Open drive: 6 variants"""
    for rw, tag in [(w['rsi'], "Std"), (max(3, w['rsi']//2), "Fast"),
                     (w['rsi']*2, "Slow"), (max(3, w['rsi']//3), "Ultra"),
                     (w['rsi']*3, "VSlow"), (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"OpenDrive({rw})", "Morning session momentum", {"rsi_window": rw}


def var_intraday_revert(w, _tf_label):
    """Lunch revert: 6 variants"""
    for rw, tag in [(w['rsi'], "Std"), (max(3, w['rsi']//2), "Fast"),
                     (w['rsi']*2, "Slow"), (max(3, w['rsi']//3), "Ultra"),
                     (w['rsi']*3, "VSlow"), (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"LunchRev({rw})", "Lunch mean reversion", {"rsi_window": rw}


def var_intraday_close(w, _tf_label):
    """Close squeeze: 6 variants"""
    for rw, tag in [(w['rsi'], "Std"), (max(3, w['rsi']//2), "Fast"),
                     (w['rsi']*2, "Slow"), (max(3, w['rsi']//3), "Ultra"),
                     (w['rsi']*3, "VSlow"), (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"CloseSqz({rw})", "Close window squeeze", {"rsi_window": rw}


def var_intraday_gap(w, _tf_label):
    """Gap fill: 6 variants"""
    for rw, tag in [(w['rsi'], "Std"), (max(3, w['rsi']//2), "Fast"),
                     (w['rsi']*2, "Slow"), (max(3, w['rsi']//3), "Ultra"),
                     (w['rsi']*3, "VSlow"), (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"GapFill({rw})", "Intraday gap fill", {"rsi_window": rw}


def var_multifactor_zscore(w, _tf_label):
    """Z-score: 8 variants"""
    for th, tag in [(1.5, "Std"), (2.0, "Tight"), (1.0, "Mild"), (1.2, "Med"),
                     (2.5, "Aggr"), (3.0, "XAggr"), (0.8, "Gentle"), (4.0, "XXAggr")]:
        yield tag, f"ZScore({th})", "Multi-factor z-score", \
            {"mid_window": w['mid'], "rsi_window": w['rsi'], "adx_window": w['adx']}


def var_multifactor_mom(w, _tf_label):
    """Momentum multi: 6 variants"""
    for rw, tag in [(w['rsi'], "Std"), (max(3, w['rsi']//2), "Fast"),
                     (w['rsi']*2, "Slow"), (max(3, w['rsi']//3), "Ultra"),
                     (w['rsi']*3, "VSlow"), (max(3, w['rsi']//4), "XUltra")]:
        yield tag, f"MFMom({rw})", "Multi-layer momentum", \
            {"rsi_window": rw, "fast_window": w['fast'], "adx_window": w['adx']}


def var_multifactor_trendvol(w, _tf_label):
    """Trend+Volume+VN30: 6 variants"""
    for mw, tag in [(w['mid'], "Mid"), (w['slow'], "Slow"), (w['fast'], "Fast"),
                     (w['mid']*2, "XSlow"), (w['slow']*2, "VSlow"),
                     (max(3, w['fast']//2), "Ultra")]:
        yield tag, f"MFTrendVol({mw})", "4-layer trend confirmation", \
            {"mid_window": mw, "vol_window": w['vol'], "adx_window": w['adx']}


# --- New templates variant generators ---

def var_momentum_cmo(w, _tf_label):
    """CMO momentum: 7 variants"""
    for cw, tag in [(w['rsi'], "Std"), (w['fast'], "Fast"), (w['mid'], "Mid"),
                     (w['slow'], "Slow"), (max(3, w['rsi']//2), "Ultra"),
                     (w['rsi']*2, "Slow2"), (max(3, w['rsi']//3), "XUltra")]:
        yield tag, f"CMO({cw})", "CMO momentum oscillator", {"rsi_window": cw}


def var_trend_aroon(w, _tf_label):
    """Aroon trend: 6 variants"""
    for aw, tag in [(w['adx'], "Std"), (w['fast'], "Fast"), (w['mid'], "Mid"),
                     (w['slow'], "Slow"), (w['adx']*2, "Slow2"),
                     (max(3, w['adx']//2), "Ultra")]:
        yield tag, f"Aroon({aw})", "Aroon trend strength", {"adx_window": aw}


def var_meanrev_cci(w, _tf_label):
    """CCI mean reversion: 7 variants"""
    for cw, tag in [(w['mid'], "Std"), (w['fast'], "Fast"), (w['slow'], "Slow"),
                     (max(3, w['mid']//2), "Ultra"), (w['mid']*2, "XSlow"),
                     (w['mid']*3, "VSlow"), (max(3, w['mid']//3), "XUltra")]:
        yield tag, f"CCI({cw})", "CCI extreme reversion", {"mid_window": cw}


def var_volume_mfi(w, _tf_label):
    """MFI volume flow: 7 variants"""
    for mw, tag in [(w['vol'], "Std"), (w['fast'], "Fast"), (w['mid'], "Mid"),
                     (max(3, w['vol']//2), "Ultra"), (w['vol']*2, "Slow"),
                     (w['vol']*3, "VSlow"), (max(3, w['vol']//3), "XUltra")]:
        yield tag, f"MFI({mw})", "MFI overbought/oversold", {"vol_window": mw}


# ================================================================
# THESIS CATALOG
# ================================================================

THESIS_CATALOG = {
    "momentum": {
        "id": 1, "timeframes": [5, 15, 30, 60],
        "templates": [
            ("momentum_pure", var_momentum_pure, "Mom", "Momentum"),
            ("momentum_vol", var_momentum_vol, "MomVol", "Momentum+Volume"),
            ("momentum_vn30", var_momentum_vn30, "MomVN30", "Momentum+VN30"),
            ("momentum_cascade", var_momentum_cascade, "MomCasc", "Cascade"),
            ("momentum_cmo", var_momentum_cmo, "MomCMO", "CMO"),
        ]
    },
    "trend": {
        "id": 2, "timeframes": [5, 15, 30, 60],
        "templates": [
            ("trend_ma_cross", var_trend_ma_cross, "TrendMAC", "MA Cross"),
            ("trend_macd", var_trend_macd, "TrendMACD", "MACD"),
            ("trend_quantile", var_trend_quantile, "TrendQ", "Quantile Trend"),
            ("trend_ema_adx", var_trend_ema_adx, "TrendEMA", "EMA Trend"),
            ("trend_aroon", var_trend_aroon, "TrendAroon", "Aroon"),
        ]
    },
    "mean_reversion": {
        "id": 3, "timeframes": [5, 15, 30, 60],
        "templates": [
            ("meanrev_quantile", var_meanrev_quantile, "MRQ", "Quantile Rev"),
            ("meanrev_rsi", var_meanrev_rsi, "MRRSI", "RSI Rev"),
            ("meanrev_bbands", var_meanrev_bbands, "MRBB", "BBands Rev"),
            ("meanrev_volclimax", var_meanrev_volclimax, "MRVC", "Vol Climax"),
            ("meanrev_cci", var_meanrev_cci, "MRCCI", "CCI"),
        ]
    },
    "breakout": {
        "id": 4, "timeframes": [5, 15, 30, 60],
        "templates": [
            ("breakout_quantile", var_breakout_quantile, "BOQ", "Quantile BO"),
            ("breakout_donchian", var_breakout_donchian, "BODon", "Donchian"),
            ("breakout_range", var_breakout_range, "BORng", "Range Exp"),
            ("breakout_vn30", var_breakout_vn30, "BOVN30", "VN30 BO"),
        ]
    },
    "cross_market": {
        "id": 5, "timeframes": [15, 30, 60],
        "templates": [
            ("cross_relative", var_cross_relative, "XMRel", "Relative"),
            ("cross_dji", var_cross_dji, "XMDJI", "DJI"),
            ("cross_consensus", var_cross_consensus, "XMCon", "Consensus"),
            ("cross_gap", var_cross_gap, "XMGap", "Gap"),
        ],
    },
    "volume_flow": {
        "id": 6, "timeframes": [15, 30, 60],
        "templates": [
            ("volume_oi", var_volume_oi, "VFOI", "OI Trend"),
            ("volume_matched_surge", var_volume_surge, "VFVol", "Vol Surge"),
            ("volume_value", var_volume_value, "VFVal", "Val Spike"),
            ("volume_obv", var_volume_obv, "VFOBV", "OBV Flow"),
            ("volume_mfi", var_volume_mfi, "VFMFI", "MFI"),
        ]
    },
    "intraday_session": {
        "id": 7, "timeframes": [5, 15],
        "templates": [
            ("intraday_open_drive", var_intraday_open, "ISMOpn", "Open Drive"),
            ("intraday_revert", var_intraday_revert, "ISMLun", "Lunch Rev"),
            ("intraday_close", var_intraday_close, "ISMCls", "Close Sq"),
            ("intraday_gapfill", var_intraday_gap, "ISMGap", "Gap Fill"),
        ]
    },
    "multifactor": {
        "id": 8, "timeframes": [15, 30, 60],
        "templates": [
            ("multifactor_zscore", var_multifactor_zscore, "MFZ", "Z-Score"),
            ("multifactor_momentum", var_multifactor_mom, "MFMom", "Momentum MF"),
            ("multifactor_trendvol", var_multifactor_trendvol, "MFTV", "Trend+Vol"),
        ]
    },
}


def build_strategies():
    """Yield (thesis, timeframe, alpha_id, name, summary, idea, template_key, fmt)."""
    alpha_counter = 0

    for thesis_name, cat in THESIS_CATALOG.items():
        t_id = cat["id"]
        for tf_label, tf_min in TIMEFRAMES:
            if tf_min not in cat["timeframes"]:
                continue
            w = WINDOWS[tf_min]

            for template_key, variant_fn, prefix, theme in cat["templates"]:
                for variant_tag, variant_summary, variant_idea, fmt_overrides in variant_fn(w, tf_label):
                    alpha_counter += 1
                    name = f"{prefix}{variant_tag}_{tf_label}"
                    summary = f"{theme}: {variant_summary} — {tf_label}"
                    idea = variant_idea

                    yield thesis_name, tf_label, f"{t_id:02d}-{alpha_counter:04d}", \
                        name, summary, idea, template_key, fmt_overrides


def main():
    index_rows = []

    for thesis, tf_label, alpha_id, name, summary, idea, template_key, fmt in build_strategies():
        t_id = THESIS_IDS[thesis]
        thesis_dir = f"thesis_{t_id:02d}_{thesis}"
        filepath = os.path.join(OUTPUT_DIR, thesis_dir, tf_label, filename(alpha_id, name))

        os.makedirs(os.path.join(OUTPUT_DIR, thesis_dir, tf_label), exist_ok=True)

        code = render(name, summary, thesis, tf_label, idea, template_key, fmt)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        index_rows.append({
            "alpha_id": alpha_id,
            "thesis_group": thesis_dir,
            "timeframe": tf_label,
            "direction": "BOTH",
            "thesis_id": t_id,
            "file": os.path.join(thesis_dir, tf_label, filename(alpha_id, name)),
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
