"""
Generate strategies batch from parameter grids.
Output: family subdirectories in output/ + index.csv
"""

import os
import csv
from itertools import product

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
INDEX_FILE = os.path.join(OUTPUT_DIR, "index.csv")

TEMPLATE_MEAN_LEVEL = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window={window})

        long_setup = close > mean
        short_setup = close < mean
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_MEAN_CROSSOVER = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        fast_mean = self.feat.rolling_mean(close, window={fast})
        slow_mean = self.feat.rolling_mean(close, window={slow})

        long_setup = self.op.crossed_above(fast_mean, slow_mean)
        short_setup = self.op.crossed_below(fast_mean, slow_mean)
        exit_setup = self.op.crossed_below(fast_mean, slow_mean) | self.op.crossed_above(fast_mean, slow_mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_MEAN_CONFIRM = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window={window})
        {confirm_feat}
        {confirm_var}

        long_setup = (close > mean) & ({confirm_cond_long})
        short_setup = (close < mean) & ({confirm_cond_short})
        exit_long = self.op.crossed_below(close, mean) | {exit_long_cond}
        exit_short = self.op.crossed_above(close, mean) | {exit_short_cond}
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_QUANTILE = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, {window}, {q_high})
        lower = self.feat.rolling_quantile(close, {window}, {q_low})

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_QUANTILE_CONFIRM = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper = self.feat.rolling_quantile(close, {window}, {q_high})
        lower = self.feat.rolling_quantile(close, {window}, {q_low})
        {confirm_feat}
        {confirm_var}

        long_setup = (close > upper) & ({confirm_cond_long})
        short_setup = (close < lower) & ({confirm_cond_short})
        exit_long = self.op.crossed_below(close, upper) | {exit_long_cond}
        exit_short = self.op.crossed_above(close, lower) | {exit_short_cond}
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_VNFUTURE = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        {data_extra}

        {feat_code}

        long_setup = ({long_cond})
        short_setup = ({short_cond})
        exit_setup = ({exit_cond})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''

TEMPLATE_COMBINED = '''\
"""
name:    {name}
summary: {summary}
idea:    {idea}
"""


class CustomStrategy(SimpleAlgorithm):

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mean = self.feat.rolling_mean(close, window={mean_window})
        upper = self.feat.rolling_quantile(close, {q_window}, {q_high})
        lower = self.feat.rolling_quantile(close, {q_window}, {q_low})
        {confirm_feat}
        {confirm_var}

        long_setup = (close > upper) & (close > mean) & ({confirm_cond_long})
        short_setup = (close < lower) & (close < mean) & ({confirm_cond_short})
        exit_long = self.op.crossed_below(close, mean) | {exit_long_cond}
        exit_short = self.op.crossed_above(close, mean) | {exit_short_cond}
        exit_setup = exit_long | exit_short

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
'''


# ============================================================
# PARAMETER GRIDS
# ============================================================

FAMILY_A = {
    "dir": "A_rolling_mean_level",
    "entries": [
        {"template": "mean_level", "alpha_id": "A-009", "window": 14, "name": "MeanLevel14", "summary": "Long when close > rolling_mean(14)", "idea": "Basic mean reversion with 14-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-010", "window": 14, "name": "MeanLevel14", "summary": "Short when close < rolling_mean(14)", "idea": "Basic mean reversion with 14-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-005", "window": 8, "name": "MeanLevel8", "summary": "Long when close > rolling_mean(8)", "idea": "Fast mean reversion with 8-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-006", "window": 8, "name": "MeanLevel8", "summary": "Short when close < rolling_mean(8)", "idea": "Fast mean reversion with 8-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-013", "window": 30, "name": "MeanLevel30", "summary": "Long when close > rolling_mean(30)", "idea": "Medium-term trend following with 30-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-014", "window": 30, "name": "MeanLevel30", "summary": "Short when close < rolling_mean(30)", "idea": "Medium-term trend following with 30-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-017", "window": 100, "name": "MeanLevel100", "summary": "Long when close > rolling_mean(100)", "idea": "Long-term trend following with 100-period rolling average"},
        {"template": "mean_level", "alpha_id": "A-018", "window": 100, "name": "MeanLevel100", "summary": "Short when close < rolling_mean(100)", "idea": "Long-term trend following with 100-period rolling average"},
    ]
}

FAMILY_B = {
    "dir": "B_rolling_mean_crossover",
    "entries": [
        {"template": "mean_crossover", "alpha_id": "B2-001", "fast": 5, "slow": 20, "name": "MACross5_20", "summary": "Long when MA5 crosses above MA20", "idea": "Trend reversal capture with fast/slow moving average crossover"},
        {"template": "mean_crossover", "alpha_id": "B2-002", "fast": 5, "slow": 20, "name": "MACross5_20", "summary": "Short when MA5 crosses below MA20", "idea": "Trend reversal capture with fast/slow moving average crossover"},
        {"template": "mean_crossover", "alpha_id": "B2-009", "fast": 10, "slow": 30, "name": "MACross10_30", "summary": "Long when MA10 crosses above MA30", "idea": "Medium-term trend crossover system"},
        {"template": "mean_crossover", "alpha_id": "B2-010", "fast": 10, "slow": 30, "name": "MACross10_30", "summary": "Short when MA10 crosses below MA30", "idea": "Medium-term trend crossover system"},
        {"template": "mean_crossover", "alpha_id": "B2-015", "fast": 20, "slow": 100, "name": "MACross20_100", "summary": "Long when MA20 crosses above MA100", "idea": "Long-term trend reversal with wide MA spread"},
        {"template": "mean_crossover", "alpha_id": "B2-016", "fast": 20, "slow": 100, "name": "MACross20_100", "summary": "Short when MA20 crosses below MA100", "idea": "Long-term trend reversal with wide MA spread"},
    ]
}

FAMILY_C = {
    "dir": "C_mean_confirmation",
    "configs": [
        {"alpha_id": "C-007", "window": 14, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 14", "exit_short_cond": "adx < 14", "name": "Mean14ADX", "summary": "Long when close > mean(14) and ADX > 20", "idea": "Trend strength filter with ADX to avoid sideways markets"},
        {"alpha_id": "C-008", "window": 14, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 14", "exit_short_cond": "adx < 14", "name": "Mean14ADX", "summary": "Short when close < mean(14) and ADX > 20", "idea": "Trend strength filter with ADX to avoid sideways markets"},
        {"alpha_id": "C-013", "window": 14, "confirm_feat": "macd, macd_signal, _hist = self.feat.macd(close, fastperiod=12, slowperiod=26, signalperiod=9)", "confirm_var": "", "confirm_cond_long": "macd > macd_signal", "confirm_cond_short": "macd < macd_signal", "exit_long_cond": "macd < macd_signal", "exit_short_cond": "macd > macd_signal", "name": "Mean14MACD", "summary": "Long when close > mean(14) and MACD bullish", "idea": "MACD trend confirmation with mean filter"},
        {"alpha_id": "C-014", "window": 14, "confirm_feat": "macd, macd_signal, _hist = self.feat.macd(close, fastperiod=12, slowperiod=26, signalperiod=9)", "confirm_var": "", "confirm_cond_long": "macd > macd_signal", "confirm_cond_short": "macd < macd_signal", "exit_long_cond": "macd < macd_signal", "exit_short_cond": "macd > macd_signal", "name": "Mean14MACD", "summary": "Short when close < mean(14) and MACD bearish", "idea": "MACD trend confirmation with mean filter"},
        {"alpha_id": "C-019", "window": 20, "confirm_feat": "volume_sma = self.feat.sma(volume, timeperiod=20)", "confirm_var": "", "confirm_cond_long": "volume > volume_sma", "confirm_cond_short": "volume > volume_sma", "exit_long_cond": "volume < volume_sma", "exit_short_cond": "volume < volume_sma", "name": "Mean20Volume", "summary": "Long when close > mean(20) and volume above average", "idea": "Volume confirmation to validate breakouts"},
        {"alpha_id": "C-020", "window": 20, "confirm_feat": "volume_sma = self.feat.sma(volume, timeperiod=20)", "confirm_var": "", "confirm_cond_long": "volume > volume_sma", "confirm_cond_short": "volume > volume_sma", "exit_long_cond": "volume < volume_sma", "exit_short_cond": "volume < volume_sma", "name": "Mean20Volume", "summary": "Short when close < mean(20) and volume above average", "idea": "Volume confirmation to validate breakouts"},
        {"alpha_id": "C-005", "window": 50, "confirm_feat": "roc = self.feat.roc(close, timeperiod=10)", "confirm_var": "", "confirm_cond_long": "roc > 0", "confirm_cond_short": "roc < 0", "exit_long_cond": "roc < -2", "exit_short_cond": "roc > 2", "name": "Mean50ROC", "summary": "Long when close > mean(50) and ROC positive", "idea": "Momentum filter with ROC on long-term mean"},
        {"alpha_id": "C-006", "window": 50, "confirm_feat": "roc = self.feat.roc(close, timeperiod=10)", "confirm_var": "", "confirm_cond_long": "roc > 0", "confirm_cond_short": "roc < 0", "exit_long_cond": "roc < -2", "exit_short_cond": "roc > 2", "name": "Mean50ROC", "summary": "Short when close < mean(50) and ROC negative", "idea": "Momentum filter with ROC on long-term mean"},
    ]
}

FAMILY_D = {
    "dir": "D_rolling_quantile_level",
    "entries": [
        {"template": "quantile", "alpha_id": "D-001", "window": 10, "q_high": 0.8, "q_low": 0.2, "name": "QuantileChannel10_80", "summary": "Long when close > quantile(10, 0.8)", "idea": "Short-term quantile breakout channel"},
        {"template": "quantile", "alpha_id": "D-002", "window": 10, "q_high": 0.8, "q_low": 0.2, "name": "QuantileChannel10_80", "summary": "Short when close < quantile(10, 0.2)", "idea": "Short-term quantile breakout channel"},
        {"template": "quantile", "alpha_id": "D-019", "window": 30, "q_high": 0.9, "q_low": 0.1, "name": "QuantileChannel30_90", "summary": "Long when close > quantile(30, 0.9)", "idea": "Medium-term extreme breakout via high quantile"},
        {"template": "quantile", "alpha_id": "D-020", "window": 30, "q_high": 0.9, "q_low": 0.1, "name": "QuantileChannel30_90", "summary": "Short when close < quantile(30, 0.1)", "idea": "Medium-term extreme breakdown via low quantile"},
        {"template": "quantile", "alpha_id": "D-031", "window": 100, "q_high": 0.75, "q_low": 0.25, "name": "QuantileChannel100_75", "summary": "Long when close > quantile(100, 0.75)", "idea": "Long-term quantile channel with wider bands"},
        {"template": "quantile", "alpha_id": "D-032", "window": 100, "q_high": 0.75, "q_low": 0.25, "name": "QuantileChannel100_75", "summary": "Short when close < quantile(100, 0.25)", "idea": "Long-term quantile channel with wider bands"},
    ]
}

FAMILY_E = {
    "dir": "E_quantile_channel",
    "configs": [
        {"alpha_id": "E1-001", "window": 10, "q_high": 0.8, "q_low": 0.2, "name": "QChannel10_80_20", "summary": "Quantile breakout: long above Q80, short below Q20 (window=10)", "idea": "Dual-direction quantile breakout channel"},
        {"alpha_id": "E1-006", "window": 14, "q_high": 0.9, "q_low": 0.1, "name": "QChannel14_90_10", "summary": "Quantile breakout: long above Q90, short below Q10 (window=14)", "idea": "Tight quantile breakout with extreme thresholds"},
        {"alpha_id": "E1-003", "window": 20, "q_high": 0.8, "q_low": 0.2, "name": "QChannel20_80_20", "summary": "Quantile breakout: long above Q80, short below Q20 (window=20)", "idea": "Medium-term quantile breakout"},
        {"alpha_id": "E2-001", "window": 10, "q_high": 0.8, "q_low": 0.2, "name": "QRev10_80_20", "summary": "Quantile reversion: short at Q80, long at Q20 (window=10)", "idea": "Mean reversion using quantile extremes"},
        {"alpha_id": "E2-003", "window": 20, "q_high": 0.8, "q_low": 0.2, "name": "QRev20_80_20", "summary": "Quantile reversion: short at Q80, long at Q20 (window=20)", "idea": "Medium-term mean reversion using quantile extremes"},
    ]
}

FAMILY_F = {
    "dir": "F_quantile_confirmation",
    "configs": [
        {"alpha_id": "F-001", "window": 14, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "rsi = self.feat.rsi(close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "rsi > 50", "confirm_cond_short": "rsi < 50", "exit_long_cond": "rsi < 40", "exit_short_cond": "rsi > 60", "name": "Q14RSI", "summary": "Long when close > Q80(14) and RSI > 50", "idea": "Quantile breakout with RSI momentum confirmation"},
        {"alpha_id": "F-002", "window": 14, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "rsi = self.feat.rsi(close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "rsi > 50", "confirm_cond_short": "rsi < 50", "exit_long_cond": "rsi < 40", "exit_short_cond": "rsi > 60", "name": "Q14RSI", "summary": "Short when close < Q20(14) and RSI < 50", "idea": "Quantile breakdown with RSI momentum confirmation"},
        {"alpha_id": "F-005", "window": 20, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 15", "exit_short_cond": "adx < 15", "name": "Q20ADX", "summary": "Long when close > Q80(20) and ADX > 20", "idea": "Quantile breakout with trend strength filter"},
        {"alpha_id": "F-006", "window": 20, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 15", "exit_short_cond": "adx < 15", "name": "Q20ADX", "summary": "Short when close < Q20(20) and ADX > 20", "idea": "Quantile breakdown with trend strength filter"},
        {"alpha_id": "F-013", "window": 20, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "volume_sma = self.feat.sma(volume, timeperiod=20)", "confirm_var": "", "confirm_cond_long": "volume > volume_sma", "confirm_cond_short": "volume > volume_sma", "exit_long_cond": "volume < volume_sma", "exit_short_cond": "volume < volume_sma", "name": "Q20Volume", "summary": "Long when close > Q80(20) and volume above average", "idea": "Quantile breakout with volume confirmation"},
    ]
}

FAMILY_H = {
    "dir": "H_vnfuture_specific",
    "configs": [
        {"alpha_id": "H-001", "data_extra": "matched_vol = self.data.fut_matched_volume_vn30f1m_1d", "feat_code": "vol_mean = self.feat.rolling_mean(matched_vol, window=14)", "long_cond": "matched_vol > vol_mean", "short_cond": "matched_vol < vol_mean * 0.8", "exit_cond": "matched_vol < vol_mean * 0.7 | matched_vol > vol_mean * 1.3", "name": "MatchedVolMean14", "summary": "Trade when matched volume exceeds rolling mean", "idea": "Volume-based signal using VnFuture matched volume"},
        {"alpha_id": "H-005", "data_extra": "oi = self.data.fut_open_interest_vn30f1m_1d", "feat_code": "oi_mean = self.feat.rolling_mean(oi, window=14)\nclose = self.data.pv_close\nclose_mean = self.feat.rolling_mean(close, window=14)", "long_cond": "(oi > oi_mean) & (close > close_mean)", "short_cond": "(oi < oi_mean) & (close < close_mean)", "exit_cond": "(oi < oi_mean * 0.95) | (close < close_mean * 0.98)", "name": "OpenInterestMean14", "summary": "Trade when open interest and price align with trend", "idea": "Open interest confirmation for trend strength"},
        {"alpha_id": "H-009", "data_extra": "total_vol = self.data.fut_total_volume_vn30f1m_1d", "feat_code": "tv_mean = self.feat.rolling_mean(total_vol, window=20)\nclose = self.data.pv_close\nclose_mean = self.feat.rolling_mean(close, window=20)", "long_cond": "(total_vol > tv_mean) & (close > close_mean)", "short_cond": "(total_vol > tv_mean) & (close < close_mean)", "exit_cond": "total_vol < tv_mean * 0.8", "name": "TotalVolMean20", "summary": "Trade when total volume spikes confirm price direction", "idea": "Total volume confirmation for VnFuture breakouts"},
        {"alpha_id": "H-003", "data_extra": "oi = self.data.fut_open_interest_vn30f1m_1d", "feat_code": "oi_q80 = self.feat.rolling_quantile(oi, 20, 0.8)\nclose = self.data.pv_close\nclose_mean = self.feat.rolling_mean(close, window=20)", "long_cond": "(oi > oi_q80) & (close > close_mean)", "short_cond": "(oi > oi_q80) & (close < close_mean)", "exit_cond": "oi < self.feat.rolling_quantile(oi, 20, 0.5)", "name": "OpenInterestQ80", "summary": "Trade when open interest breaks quantile 0.8", "idea": "Open interest quantile breakout for institutional flow detection"},
        {"alpha_id": "H-021", "data_extra": "matched_val = self.data.fut_matched_value_vn30f1m_1d", "feat_code": "mv_mean = self.feat.rolling_mean(matched_val, window=14)\nclose = self.data.pv_close\nclose_mean = self.feat.rolling_mean(close, window=14)\nmv_q80 = self.feat.rolling_quantile(matched_val, 14, 0.8)", "long_cond": "(matched_val > mv_q80) & (close > close_mean)", "short_cond": "(matched_val > mv_q80) & (close < close_mean)", "exit_cond": "matched_val < mv_mean", "name": "MatchedValQ80", "summary": "Trade when matched value spikes above quantile 0.8", "idea": "Matched value breakout for large flow detection"},
    ]
}

FAMILY_I = {
    "dir": "I_combined_mean_quantile",
    "configs": [
        {"alpha_id": "I-001", "mean_window": 14, "q_window": 10, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "rsi = self.feat.rsi(close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "rsi > 50", "confirm_cond_short": "rsi < 50", "exit_long_cond": "rsi < 40", "exit_short_cond": "rsi > 60", "name": "Mean14Q10RSI", "summary": "Long when close > Q80(10) > mean(14) and RSI > 50", "idea": "Three-layer confirmation: quantile breakout + mean trend + RSI momentum"},
        {"alpha_id": "I-002", "mean_window": 14, "q_window": 10, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "rsi = self.feat.rsi(close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "rsi > 50", "confirm_cond_short": "rsi < 50", "exit_long_cond": "rsi < 40", "exit_short_cond": "rsi > 60", "name": "Mean14Q10RSI", "summary": "Short when close < Q20(10) < mean(14) and RSI < 50", "idea": "Three-layer confirmation: quantile breakdown + mean trend + RSI momentum"},
        {"alpha_id": "I-005", "mean_window": 50, "q_window": 20, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 15", "exit_short_cond": "adx < 15", "name": "Mean50Q20ADX", "summary": "Long when close > Q80(20) > mean(50) and ADX > 20", "idea": "Long-term mean + quantile breakout with ADX strength"},
        {"alpha_id": "I-006", "mean_window": 50, "q_window": 20, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "adx = self.feat.adx(high, low, close, timeperiod=14)", "confirm_var": "", "confirm_cond_long": "adx > 20", "confirm_cond_short": "adx > 20", "exit_long_cond": "adx < 15", "exit_short_cond": "adx < 15", "name": "Mean50Q20ADX", "summary": "Short when close < Q20(20) < mean(50) and ADX > 20", "idea": "Long-term mean + quantile breakdown with ADX strength"},
        {"alpha_id": "I-003", "mean_window": 20, "q_window": 14, "q_high": 0.8, "q_low": 0.2, "confirm_feat": "volume_sma = self.feat.sma(volume, timeperiod=20)", "confirm_var": "", "confirm_cond_long": "volume > volume_sma", "confirm_cond_short": "volume > volume_sma", "exit_long_cond": "volume < volume_sma * 0.8", "exit_short_cond": "volume < volume_sma * 0.8", "name": "Mean20Q14Volume", "summary": "Long when close > Q80(14) > mean(20) and volume above average", "idea": "Quantile breakout + mean trend + volume confirmation"},
    ]
}

TEMPLATES = {
    "mean_level": TEMPLATE_MEAN_LEVEL,
    "mean_crossover": TEMPLATE_MEAN_CROSSOVER,
    "quantile": TEMPLATE_QUANTILE,
}

FAMILY_MAP = {
    "A": (FAMILY_A, "mean_level"),
    "B": (FAMILY_B, "mean_crossover"),
    "D": (FAMILY_D, "quantile"),
}

FAMILIES_RAW = [
    ("A", "A_rolling_mean_level", FAMILY_A["entries"], "mean_level"),
    ("B", "B_rolling_mean_crossover", FAMILY_B["entries"], "mean_crossover"),
    ("C", "C_mean_confirmation", "mean_confirm"),
    ("D", "D_rolling_quantile_level", FAMILY_D["entries"], "quantile"),
    ("E", "E_quantile_channel", "quantile_channel"),
    ("F", "F_quantile_confirmation", "quantile_confirm"),
    ("H", "H_vnfuture_specific", "vnfuture"),
    ("I", "I_combined_mean_quantile", "combined"),
]


def make_filename(alpha_id, name, suffix=""):
    return f"{alpha_id}_{name}{suffix}.py"


def render_and_write(template_key, params, family_dir, filename):
    if template_key == "mean_level":
        code = TEMPLATE_MEAN_LEVEL.format(**params)
    elif template_key == "mean_crossover":
        code = TEMPLATE_MEAN_CROSSOVER.format(**params)
    elif template_key == "quantile":
        code = TEMPLATE_QUANTILE.format(**params)
    else:
        raise ValueError(f"Unknown template: {template_key}")

    filepath = os.path.join(OUTPUT_DIR, family_dir, filename)
    os.makedirs(os.path.join(OUTPUT_DIR, family_dir), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath


def main():
    index_rows = []

    # Family A: Mean Level
    for e in FAMILY_A["entries"]:
        p = e.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        fp = render_and_write("mean_level", p, FAMILY_A["dir"], fn)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_A["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family B: Mean Crossover
    for e in FAMILY_B["entries"]:
        p = e.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        fp = render_and_write("mean_crossover", p, FAMILY_B["dir"], fn)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_B["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family C: Mean + Confirmation
    for cfg in FAMILY_C["configs"]:
        p = cfg.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        code = TEMPLATE_MEAN_CONFIRM.format(**p)
        d = os.path.join(OUTPUT_DIR, FAMILY_C["dir"])
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(code)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_C["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family D: Quantile Level
    for e in FAMILY_D["entries"]:
        p = e.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        fp = render_and_write("quantile", p, FAMILY_D["dir"], fn)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_D["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family E: Quantile Channel
    for cfg in FAMILY_E["configs"]:
        p = cfg.copy()
        p["direction"] = "BOTH"
        fn = make_filename(p["alpha_id"], p["name"], "")
        code = TEMPLATE_QUANTILE.format(**p)
        d = os.path.join(OUTPUT_DIR, FAMILY_E["dir"])
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(code)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_E["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family F: Quantile + Confirmation
    for cfg in FAMILY_F["configs"]:
        p = cfg.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        code = TEMPLATE_QUANTILE_CONFIRM.format(**p)
        d = os.path.join(OUTPUT_DIR, FAMILY_F["dir"])
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(code)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_F["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family H: VnFuture-specific
    for cfg in FAMILY_H["configs"]:
        p = cfg.copy()
        p["direction"] = "BOTH"
        fn = make_filename(p["alpha_id"], p["name"], "")
        code = TEMPLATE_VNFUTURE.format(**p)
        d = os.path.join(OUTPUT_DIR, FAMILY_H["dir"])
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(code)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_H["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Family I: Combined Mean + Quantile
    for cfg in FAMILY_I["configs"]:
        p = cfg.copy()
        p["direction"] = "LONG" if "Long" in p["summary"] else "SHORT"
        fn = make_filename(p["alpha_id"], p["name"], "")
        code = TEMPLATE_COMBINED.format(**p)
        d = os.path.join(OUTPUT_DIR, FAMILY_I["dir"])
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, fn)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(code)
        index_rows.append({"alpha_id": p["alpha_id"], "family": FAMILY_I["dir"], "file": fn, "direction": p["direction"]})
        print(f"  {fp}")

    # Write index.csv
    with open(INDEX_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["alpha_id", "family", "file", "direction"])
        writer.writeheader()
        writer.writerows(index_rows)

    print(f"\nDone! Generated {len(index_rows)} strategies.")
    print(f"Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
