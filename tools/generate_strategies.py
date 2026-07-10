"""
Alpha Bot — Strategy Generator
Reads from 6 thesis groups with 37 templates, generates ~677 variants.
"""

import os
import re
from itertools import product

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
INDEX_PATH = os.path.join(OUTPUT_DIR, "index.csv")

THESIS_FOLDERS = {
    "01": "thesis_01_rolling_mean_quantile",
    "02": "thesis_02_volatility_regime",
    "03": "thesis_03_time_series_decomp",
    "04": "thesis_04_microstructure_flow",
    "05": "thesis_05_cross_market_correlation",
    "06": "thesis_06_multifactor_composite",
    "07": "thesis_07_intraday_session",
    "08": "thesis_08_order_book_shadowing",
    "09": "thesis_09_institutional_flow_arbitrage",
    "10": "thesis_10_regime_based_mean_reversion",
    "11": "thesis_11_vwap_basis_reversion",
    "12": "thesis_12_kalman_regime_switching",
    "13": "thesis_13_cmf_squeeze_breakout",
    "14": "thesis_14_bb_squeeze_reversal",
    "15": "thesis_15_mavp_adaptive",
    "16": "thesis_16_velocity_divergence",
    "17": "thesis_17_vol_adjusted_momentum",
}
HEADER = '''"""
name:    {name}
summary: {summary}
idea:    {idea}
"""
'''

TEMPLATE_META = {
    # Thesis 01: Rolling Mean + Quantile
    "T01-A": ("Price vs Rolling Mean", "Compare price to rolling mean at multiple price sources (close, typical, weighted, median, OHLC4, high, low, volume, VWAP); long above, short below mean."),
    "T01-B": ("Fast/Slow MA Crossover", "Capture directional moves via SMA crossover; long on fast crossing above slow, short on cross below."),
    "T01-C": ("Mean + Multi-Confirmation", "Enhanced mean reversion with RSI, volume, and ADX confirmation for higher signal reliability."),
    "T01-D": ("Quantile Breakout Channel", "Trade breakouts beyond rolling quantile bands at multiple quantile thresholds; exit when price reverts to the band edge."),
    "T01-E": ("Mean + Quantile Fusion", "Combine mean and quantile filters: require price above both upper quantile and mean for long, below both for short."),
    "T01-F": ("Z-Score Mean Reversion", "Bet on over-extensions via rolling z-score; long when deeply negative, short when deeply positive; exit near neutral."),
    "T01-G": ("Adaptive MA (KAMA/MAMA)", "Use Kaufman Adaptive MA and Mesa MAMA for trend detection in varying market conditions."),
    # Thesis 02: Volatility Regime
    "T02-A": ("Volatility Breakout", "Enter on volatility expansion (ATR > SMA × multiplier) confirmed by ROC and ADX direction."),
    "T02-B": ("Low Vol Mean Reversion", "Trade mean reversion during volatility compression (ATR < SMA × 0.7) with RSI extremes."),
    "T02-C": ("3-State Regime Proxy", "Proxy Hidden Markov Model via ADX (trend) and vol regime (ATR std); switch between momentum and mean-reversion modes."),
    "T02-D": ("ATR Trailing Stop + Trend", "Trend following with ATR-based trailing stop and EMA/ADX directional filter."),
    "T02-E": ("NATR Regime Switching", "Normalized ATR regime detection; trade trend during high vol, mean-reversion during low vol."),
    "T02-F": ("KAMA Trend", "Adaptive trend following with Kaufman MA and ADX confirmation; exit on trend loss."),
    # Thesis 03: Time-Series Decomposition
    "T03-A": ("Hilbert Trendline + Sine Cycle", "Decompose price into trend and cycle components via Hilbert Transform; trade sine/leadsine phase alignment."),
    "T03-B": ("DCPeriod Adaptive Sizing", "Use Dominant Cycle Period to scale position sizes dynamically; larger cycles get larger positions."),
    "T03-C": ("LinReg Slope Trend", "Trade linear regression slope direction with angle filter and price-forecast gap for entry timing."),
    "T03-D": ("Sine Crossover", "Trade sine/leadsine crossovers as cycle entry signals, filtered by RSI and ADX."),
    "T03-E": ("Dispersion Entropy Proxy", "Use MAD/STD ratio to distinguish structured vs chaotic markets; trade only structured regimes."),
    # Thesis 04: Microstructure Flow
    "T04-A": ("BOP + CMF Flow Detection", "Detect buying/selling pressure with Balance of Power and Chaikin Money Flow; enter on institutional flow + volume."),
    "T04-B": ("MFI Volume-Weighted Reversal", "Trade Money Flow Index extremes with ADX and volume confirmation for high-conviction reversals."),
    "T04-C": ("OI + Volume Cascade", "Detect margin-call cascades via OI drop + volume spike + price fall; counter-trade exhaustion patterns."),
    "T04-D": ("Whale Footprint", "Detect institutional activity via avg trade size deviation; trade compression-breakout with whale presence."),
    "T04-E": ("A/D Oscillator Divergence", "Bullish/bearish divergence between price and Accumulation/Distribution Oscillator with RSI confirmation."),
    "T04-F": ("OBV Trend Confirmation", "Confirm price trend with On-Balance Volume alignment; exit on OBV/price divergence."),
    "T04-G": ("Volume Flow Imbalance", "Track smart money flow via OI change + avg trade size; long on accumulation, short on distribution."),
    # Thesis 05: Cross-Market Correlation
    "T05-A": ("Futures-VN30 Spread Reversion", "Trade futures vs VN30 basis via beta-adjusted spread z-score; mean-reversion with ADX trend filter."),
    "T05-B": ("VN30 Momentum Confirmation", "Require both futures and VN30 index momentum in the same direction for aligned entries."),
    "T05-C": ("Futures-Cash Basis Extreme", "Trade basis extreme z-score deviations; entry when basis diverges from its mean under low volume."),
    "T05-D": ("DJI Global Consensus", "Require futures, VN30, and Dow Jones momentum alignment for global trend confirmation."),
    "T05-E": ("Rolling Correlation Trend Filter", "Use rolling correlation between futures/VN30 and futures/DJI as a trend filter; avoid negative correlation regimes."),
    "T05-F": ("Relative Strength Ratio", "Trade futures-to-VN30 ratio trend via SMA, ROC, and linear regression slope."),
    "T05-G": ("Correlation Breakdown Detection", "Detect correlation breakdown between futures and VN30; trade the dislocation with volume confirmation."),
    # Thesis 06: Multi-Factor Composite
    "T06-A": ("3-Factor Z-Score Composite", "Composite z-score of price, momentum, and volume; strong/weak position sizing based on conviction levels."),
    "T06-B": ("4-Factor Z-Score Composite", "Extended composite adding volatility and cross-market ratio z-scores for broader signal coverage."),
    "T06-C": ("Multi-Layer Confirmation", "Stack trend, momentum, volume, volatility, and cross-market filters with graduated position sizing."),
    "T06-D": ("Candlestick + Z-Score", "Combine candlestick patterns (hammer, engulfing, morning/evening star) with z-score composite for reversal entries."),
    "T06-E": ("Adaptive Regime-Weighted", "Dynamically weight z-score factors based on ADX/ATR regime; trend weights momentum, high-vol weights volume."),
    # Thesis 07: Intraday Session Microstructure
    "T07-A": ("Open Drive", "Morning momentum continuation: close > SMA + volume spike + return_roll > 0 in first 30 min of session."),
    "T07-B": ("Lunch Revert", "Pre-lunch mean reversion: RSI > 70 (short) or RSI < 30 (long) before lunch close."),
    "T07-C": ("Close Squeeze", "Afternoon breakout: ROC > 0 + volume × mult spike + ADX > entry; exit before ATC."),
    "T07-D": ("Pre-ATC Mean Rev", "Late afternoon BBands extreme touch + volume confirm; mean revert before ATC close."),
    "T07-E": ("Session VWAP Bounce", "Price deviates ±z% from VWAP then bounces back with return_roll confirmation; exit on VWAP cross."),
    # Thesis 08: Key Level Absorption (OHLCV-only)
    "T08-A": ("Key Level Wick Rejection", "Detect rejection at resistance/support via candle midpoint; when close is in opposite half at key level = absorption, trade reversal."),
    "T08-B": ("Volume Climax Absorption", "Volume spike + tight range at key level + close in rejection half = climax absorption; trade the reversal with ADX + return_roll exit."),
    "T08-C": ("Range Compression Absorption", "Narrow range (NATR < SMA × 0.8) at key level = absorption complete, trade the impending breakout direction via return_roll."),
    "T08-D": ("VWAP Divergence at Key Level", "Price at key level AND beyond VWAP band = divergence from fair value; trade mean reversion with between-exit on VWAP cross."),
    "T08-E": ("Multi-Confirmation Composite", "OHLCV-only composite of price_z + vol_z + (-range_z) + mom_z; exit when composite decays or ADX fades."),
    # Thesis 09: Institutional Flow Arbitrage
    "T09-A": ("OI Confirmation", "Compare OI change direction vs futures return; genuine when aligned, fade when OI drops (weak conviction)."),
    "T09-B": ("Flow Divergence", "Matched value flow + VN30 alignment + volume filter to detect institutional participation vs retail noise."),
    "T09-C": ("Composite Flow", "OHLCV-based z-score composite (price+vn30+volume) + binary flow alignment (OI == matched volume direction)."),
    # Thesis 10: Regime-based Mean Reversion
    "T10-A": ("Regime Dip/Rally", "Bull (close>MA200): long on dips to MA20. Bear (close<MA200): short on rallies to MA20. Sideways: quantile mean reversion."),
    "T10-B": ("Confirmed Regime Entries", "Same regime filter + ADX + volume confirmation for dip/rally entries; sideways uses RSI extremes with low volume."),
    "T10-C": ("Regime Band Oscillator", "Same regime filter + Bollinger Bands; bull: buy lower band touch; bear: sell upper band touch; sideways: wider quantile extremes."),
    # Thesis 11: VWAP Basis Reversion
    "T11-A": ("VWAP Basis Dual Z-Score", "Mean-revert on dual z-score of VWAP distance and VN30 basis; long when both oversold, short when both overbought; exit on neutral reversion."),
    "T11-B": ("VWAP Basis with ADX Filter", "Same dual z-score logic + ADX trending filter: only enter when ADX < threshold to avoid mean-reverting against strong trends."),
    "T11-C": ("VWAP Basis with ATR Stop", "Same dual z-score logic + ATR trailing stop for capital-preserving exits when price breaks away from the 20-period MA."),
    "T11-D": ("VWAP Basis Regime Switching", "Dual-mode: mean-revert in ranging (ADX<exit) via dual z-score; trend-follow in trending (ADX>entry) via VWAP+basis+momentum alignment; regime crossover exits for clean transitions."),
    # Thesis 12: Kalman Filter Regime Switching
    "T12-A": ("KF Dip/Rally", "Kalman proxy (SMA+residual) regime detection; trend-follow when KF deviates above entry band, mean-revert within band; exit via KF z-cross + ADX fade + ATR stop."),
    "T12-B": ("KF Mean Reversion", "Kalman proxy with emphasis on sideways overshoot; higher MR threshold for high-conviction entries; same exit structure."),
    "T12-C": ("KF + ADX Confirmed", "Kalman entries with ADX confirmation on both trend and MR modes; stricter filter for lower signal count but higher win rate."),
    "T12-D": ("KF + Z Combo", "Kalman proxy with dual confirmation: KF z-score + residual z-score must both agree; requires deeper overshoot for entry."),
    # Thesis 13: CMF + Bollinger Squeeze Breakout
    "T13-A": ("CMF + Squeeze Breakout", "Bollinger squeeze (bb_width < SMA*0.8) + CMF directional flow + ADX trend filter + volume confirmation; exit via ADX fade + ATR stop only."),
    # Thesis 14: BB Squeeze Reversal
    "T14-A": ("BB Squeeze Reversal", "Bollinger squeeze reversal: trade when price touches outer band + volume confirmation; exit via ATR stop + trailing."),
    "T14-C": ("BB Squeeze TimeStop", "Same BB reversal core + time-based exit (bars_since > max_hold) to cut stale trades that haven't worked out."),
    # Thesis 15: MAVP Adaptive Momentum
    "T15-mavp": ("MAVP Adaptive Trend", "Replace fixed SMA(20) with mavp(close, periods=dcperiod). Entry when price crosses adaptive MA with ADX + volume + return_roll confirmation. Exit via ADX fade + ATR stop + trailing."),
    "T15-mavp_B": ("MAVP Adaptive BBands", "Same mavp core but use mavp as BBands mid band — bands adapt to market cycle. Entry at band touch with ADX + volume. Exit via ADX fade + ATR stop + trailing + band cross."),
    "T15-mavp_C": ("MAVP TrendMode Gate", "Same mavp core + trendmode == 1 gate for entry. Exit adds trendmode == 0 for earlier regime-based exit."),
    # Thesis 16: Price-Volume Velocity Divergence
    "T16-A": ("Velocity Divergence", "Compare price velocity (roc) vs volume velocity (volume_z). Volume surges before price moves = accumulation. Price surges on fading volume = fake breakout. Exit via ADX fade + ATR stop + trailing."),
    # Thesis 17: Volatility-Adjusted Momentum
    "T17-A": ("Vol-Adj Momentum Breakout", "ROC divided by ATR to normalize momentum by volatility; z-score extreme ±1.5 signals genuine breakout; exit via ADX fade + ATR stop + trailing."),
    "T17-B": ("Vol-Adj Momentum + SMA Filter", "Same adj_mom_z logic with SMA13/SMA34 trend filter to avoid counter-trend entries; exit adds adj_mom_z < 0 for earlier profit protection."),
    "T17-C": ("Vol-Adj Momentum Regime", "Adaptive adj_mom_z threshold (±2.0 in low vol, ±1.2 in high vol) and trailing mult (1.5/2.5) based on ATR ratio regime."),
}

def _base_template_name(name):
    m = re.match(r'(T\d\d-[A-Z])', name)
    return m.group(1) if m else name

TF_WINDOWS = {
    5:  dict(fast=8,  slow=20, rsi=7,  adx=7,  vol=14, roc=3,  mid=13, return_periods=3,  max_cycle=30, ema=8),
    15: dict(fast=13, slow=34, rsi=10, adx=10, vol=20, roc=5,  mid=26, return_periods=5,  max_cycle=50, ema=13),
    30: dict(fast=20, slow=50, rsi=14, adx=14, vol=26, roc=8,  mid=40, return_periods=8,  max_cycle=50, ema=20),
    60: dict(fast=30, slow=100,rsi=21, adx=21, vol=34, roc=14, mid=60, return_periods=14, max_cycle=50, ema=30),
}

ADX_ENTRY = {5:22, 15:22, 30:18, 60:16}
ADX_EXIT  = {5:15, 15:15, 30:12, 60:10}
ADX_ENTRY_WEAK = {5:18, 15:18, 30:15, 60:14}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _safe_name(s):
    return s.replace(" ", "_").replace(".", "_")


# ---------------------------------------------------------------------------
# Template definitions
# ---------------------------------------------------------------------------

TEMPLATES = []

# ============================================================
# THESIS 01: Rolling Mean + Quantile
# ============================================================

_PRICE_SOURCES = [
    ("close",   "close = self.data.pv_close",         "close"),
    ("typical", "typical = self.feat.typprice(high, low, close)", "typical"),
    ("weighted","weighted = self.feat.wclprice(high, low, close)", "weighted"),
    ("median",  "median = self.feat.medprice(high, low)",          "median"),
    ("ohlc4",   "ohlc4 = self.feat.ohlc4(open_price, high, low, close)", "ohlc4"),
    ("high",    "high_px = self.data.pv_high",         "high_px"),
    ("low",     "low_px = self.data.pv_low",           "low_px"),
    ("volume",  "volume_raw = self.data.pv_volume",    "volume_raw"),
    ("vwap_px", "vwap_px = self.feat.vwap(high, low, close, volume)", "vwap_px"),
]

# T01-A: Price vs Rolling Mean (Level)
T01_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        open_price = self.data.pv_open

        {price_source_def}

        mean = self.feat.rolling_mean({price_source_series}, window=self.mean_window)

        long_setup = {price_source_series} > mean
        short_setup = {price_source_series} < mean
        exit_setup = self.op.crossed_below({price_source_series}, mean) | self.op.crossed_above({price_source_series}, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for ps_name, ps_def, ps_series in _PRICE_SOURCES:
    TEMPLATES.append({
        "name":       f"T01-A_{ps_name}",
        "thesis":     "01",
        "descr":      f"Price vs Rolling Mean ({ps_name})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_A_CODE,
        "fixed":      {
            "price_source_def":    ps_def,
            "price_source_series": ps_series,
        },
        "params":     {"mean_window": [5, 8, 10, 14, 20, 30, 50, 100, 200]},
    })

# T01-B: Rolling Mean Crossover
T01_B_CODE = """class CustomStrategy(SimpleAlgorithm):
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
"""

TEMPLATES.append({
    "name":       "T01-B",
    "thesis":     "01",
    "descr":      "Rolling Mean Crossover",
    "timeframes": [5, 15, 30, 60],
    "code":       T01_B_CODE,
    "fixed":      {},
    "params":     {
        "fast_window": [5, 8, 10, 13, 20],
        "slow_window": [20, 34, 50, 100, 200],
    },
})

# T01-C: Mean + Confirmation
T01_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}


    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > mean) & (rsi > 50) & (volume > vol_sma) & (adx_val > {adx_entry})
        short_setup = (close < mean) & (rsi < 50) & (volume > vol_sma) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for mw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T01-C_w{mw}",
        "thesis":     "01",
        "descr":      f"Mean + Confirmation (w={mw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_C_CODE,
        "fixed":      {"mean_window": mw},
        "params":     {},  # windows injected per-TF
    })

# T01-D: Price vs Rolling Quantile (Breakout)
T01_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    q_window = {q_window}


    def __algorithm__(self):
        close = self.data.pv_close

        upper = self.feat.rolling_quantile(close, window=self.q_window, q={q_high})
        lower = self.feat.rolling_quantile(close, window=self.q_window, q={q_low})

        long_setup = close > upper
        short_setup = close < lower
        exit_setup = self.op.crossed_below(close, upper) | self.op.crossed_above(close, lower)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

_QUANTILE_PAIRS = [
    (0.80, 0.20), (0.90, 0.10), (0.95, 0.05), (0.75, 0.25), (0.85, 0.15)
]
for qh, ql in _QUANTILE_PAIRS:
    TEMPLATES.append({
        "name":       f"T01-D_q{qh}_{ql}",
        "thesis":     "01",
        "descr":      f"Quantile Breakout (q={qh}/{ql})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_D_CODE,
        "fixed":      {"q_high": qh, "q_low": ql},
        "params":     {"q_window": [10, 14, 20, 30, 50, 100]},
    })

# T01-E: Mean + Quantile Channel
T01_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    mean_window = {mean_window}
    q_window = {q_window}


    def __algorithm__(self):
        close = self.data.pv_close

        mean = self.feat.rolling_mean(close, window=self.mean_window)
        upper = self.feat.rolling_quantile(close, window=self.q_window, q=0.8)
        lower = self.feat.rolling_quantile(close, window=self.q_window, q=0.2)

        long_setup = (close > upper) & (close > mean)
        short_setup = (close < lower) & (close < mean)
        exit_setup = self.op.crossed_below(close, mean) | self.op.crossed_above(close, mean)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for mw, qw in [(10, 10), (20, 14), (34, 20), (50, 30)]:
    TEMPLATES.append({
        "name":       f"T01-E_m{mw}_q{qw}",
        "thesis":     "01",
        "descr":      f"Mean+Quantile Channel (m={mw}, q={qw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_E_CODE,
        "fixed":      {"mean_window": mw, "q_window": qw},
        "params":     {},
    })

# T01-F: Rolling Z-Score Mean Reversion
T01_F_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}


    def __algorithm__(self):
        close = self.data.pv_close

        price_z = self.feat.rolling_zscore(close, window=self.z_window)

        long_setup = price_z < -{z_entry}
        short_setup = price_z > {z_entry}
        exit_setup = self.op.between(price_z, -1, 1)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for zw, ze in product([10, 14, 20, 34], [1.5, 2.0, 2.5, 3.0]):
    TEMPLATES.append({
        "name":       f"T01-F_z{zw}_e{ze}",
        "thesis":     "01",
        "descr":      f"Z-Score Reversion (z={zw}, entry={ze})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_F_CODE,
        "fixed":      {"z_window": zw, "z_entry": ze},
        "params":     {},
    })

# T01-G: Adaptive MA (KAMA/MAMA)
T01_G_CODE = """class CustomStrategy(SimpleAlgorithm):
    kama_window = {kama_window}


    def __algorithm__(self):
        close = self.data.pv_close

        mama, fama = self.feat.mama(close)
        kama = self.feat.kama(close, timeperiod=self.kama_window)

        long_setup = (close > kama) & (mama > fama)
        short_setup = (close < kama) & (mama < fama)
        exit_setup = self.op.crossed_below(close, kama) | self.op.crossed_above(close, kama)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for kw in [10, 20, 30, 50]:
    TEMPLATES.append({
        "name":       f"T01-G_k{kw}",
        "thesis":     "01",
        "descr":      f"Adaptive MA (kama={kw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T01_G_CODE,
        "fixed":      {"kama_window": kw},
        "params":     {},
    })

# ============================================================
# THESIS 02: Volatility Regime
# ============================================================

# T02-A: Volatility Breakout
T02_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        vol_expansion = atr_val > atr_sma * {vol_entry}
        roc_val = self.feat.roc(close, timeperiod={roc_window})

        long_setup = vol_expansion & (roc_val > 0) & (adx_val > {adx_entry})
        short_setup = vol_expansion & (roc_val < 0) & (adx_val > {adx_entry})
        exit_setup = (atr_val < atr_sma) | self.op.crossed_below(adx_val, {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for vw, ve in product([10, 14, 20, 34], [1.3, 1.5, 2.0]):
    TEMPLATES.append({
        "name":       f"T02-A_w{vw}_e{ve}",
        "thesis":     "02",
        "descr":      f"Vol Breakout (w={vw}, entry={ve})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_A_CODE,
        "fixed":      {"vol_window": vw, "vol_entry": ve},
        "params":     {},
    })

# T02-B: Low Vol Mean Reversion
T02_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        rsi = self.feat.rsi(close, timeperiod={rsi_window})

        vol_compression = atr_val < atr_sma * {vol_compress}

        long_setup = vol_compression & (rsi < 30)
        short_setup = vol_compression & (rsi > 70)
        exit_setup = self.op.crossed_above(rsi, 50) | self.op.crossed_below(rsi, 50)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for vw, vc, rw in product([10, 14, 20, 34], [0.5, 0.7], [14, 21]):
    TEMPLATES.append({
        "name":       f"T02-B_w{vw}_c{vc}_r{rw}",
        "thesis":     "02",
        "descr":      f"Low Vol MeanRev (w={vw}, c={vc}, rsi={rw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_B_CODE,
        "fixed":      {"vol_window": vw, "vol_compress": vc, "rsi_window": rw},
        "params":     {},
    })

# T02-C: HMM Proxy (3-state)
T02_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    adx_window = {adx_window}
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adx_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.vol_window)
        atr_sma = self.feat.sma(atr_val, timeperiod=self.vol_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        vol_ratio = volume / vol_sma
        vol_regime = self.feat.rolling_std(atr_val, window=self.vol_window)
        vol_regime_sma = self.feat.sma(vol_regime, window=self.vol_window)

        roc_fast = self.feat.roc(close, timeperiod={roc_window})
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)
        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)

        momentum_mode = (adx_val > 25) & (vol_regime > vol_regime_sma)
        meanrev_mode = (adx_val < 22) & (vol_regime < vol_regime_sma)

        mom_long = momentum_mode & (roc_fast > 0) & (volume > vol_sma)
        mom_short = momentum_mode & (roc_fast < 0) & (volume > vol_sma)

        mr_long = meanrev_mode & (close < lower_q) & (volume < vol_sma)
        mr_short = meanrev_mode & (close > upper_q) & (volume < vol_sma)

        long_setup = mom_long | mr_long
        short_setup = mom_short | mr_short
        exit_setup = self.op.crossed_below(adx_val, 15) | (adx_val < 18)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for aw, vw in product([10, 14, 20, 34], [10, 14, 20, 34]):
    TEMPLATES.append({
        "name":       f"T02-C_a{aw}_v{vw}",
        "thesis":     "02",
        "descr":      f"3-State Regime (adx={aw}, vol={vw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_C_CODE,
        "fixed":      {"adx_window": aw, "vol_window": vw},
        "params":     {},
    })

# T02-D: ATR Trailing Stop + Trend
T02_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    atr_window = {atr_window}
    atr_mult = {atr_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        atr_val = self.feat.atr(high, low, close, timeperiod=self.atr_window)
        ema = self.feat.ema(close, timeperiod={ema_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > ema) & (adx_val > {adx_entry}) & (close > (close - atr_val * self.atr_mult))
        short_setup = (close < ema) & (adx_val > {adx_entry}) & (close < (close + atr_val * self.atr_mult))
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for atw, atm, ew in product([10, 14, 20, 34], [2, 3], [13, 26]):
    TEMPLATES.append({
        "name":       f"T02-D_at{atw}_m{atm}_e{ew}",
        "thesis":     "02",
        "descr":      f"ATR Trailing (atr={atw}, mult={atm}, ema={ew})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_D_CODE,
        "fixed":      {"atr_window": atw, "atr_mult": atm, "ema_window": ew},
        "params":     {},
    })

# T02-E: NATR Regime Switching
T02_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    natr_window = {natr_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        natr = self.feat.natr(high, low, close, timeperiod=self.natr_window)
        natr_sma = self.feat.sma(natr, timeperiod=self.natr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        high_vol = natr > natr_sma * 1.3
        low_vol = natr < natr_sma * 0.7

        roc_val = self.feat.roc(close, timeperiod={roc_window})
        rsi = self.feat.rsi(close, timeperiod={rsi_window})

        long_trend = high_vol & (roc_val > 0) & (adx_val > {adx_entry})
        short_trend = high_vol & (roc_val < 0) & (adx_val > {adx_entry})
        long_rev = low_vol & (rsi < 30) & (adx_val < 20)
        short_rev = low_vol & (rsi > 70) & (adx_val < 20)

        long_setup = long_trend | long_rev
        short_setup = short_trend | short_rev
        exit_setup = self.op.crossed_below(adx_val, 15) | (natr < natr_sma * 0.5)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for nw in [10, 14, 20, 34]:
    TEMPLATES.append({
        "name":       f"T02-E_n{nw}",
        "thesis":     "02",
        "descr":      f"NATR Regime Switch (natr={nw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_E_CODE,
        "fixed":      {"natr_window": nw},
        "params":     {},
    })

# T02-F: Adaptive KAMA Trend
T02_F_CODE = """class CustomStrategy(SimpleAlgorithm):
    kama_window = {kama_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kama = self.feat.kama(close, timeperiod=self.kama_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > kama) & (adx_val > {adx_entry})
        short_setup = (close < kama) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, kama) | self.op.crossed_above(close, kama) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for kw in [10, 20, 30, 50]:
    TEMPLATES.append({
        "name":       f"T02-F_k{kw}",
        "thesis":     "02",
        "descr":      f"KAMA Trend (kama={kw})",
        "timeframes": [5, 15, 30, 60],
        "code":       T02_F_CODE,
        "fixed":      {"kama_window": kw},
        "params":     {},
    })

# ============================================================
# THESIS 03: Time-Series Decomposition
# ============================================================

# T03-A: Hilbert Trendline + Sine Cycle
T03_A_CODE = """class CustomStrategy(SimpleAlgorithm):


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        trend = self.feat.ht_trendline(close)
        sine, leadsine = self.feat.sine(close)
        cycle_mode = self.feat.trendmode(close) == 0
        trend_mode = self.feat.trendmode(close) == 1
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        cycle_long = (sine > leadsine) & cycle_mode & (close > trend)
        cycle_short = (sine < leadsine) & cycle_mode & (close < trend)

        trend_long = (close > trend) & trend_mode & (adx_val > {adx_entry})
        trend_short = (close < trend) & trend_mode & (adx_val > {adx_entry})

        long_setup = cycle_long | trend_long
        short_setup = cycle_short | trend_short
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

TEMPLATES.append({
    "name":       "T03-A",
    "thesis":     "03",
    "descr":      "Hilbert Trendline + Sine Cycle",
    "timeframes": [15, 30, 60],
    "code":       T03_A_CODE,
    "fixed":      {},
    "params":     {},
})

# T03-B: DCPeriod Adaptive Sizing
T03_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    base_window = {base_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        cycle_period = self.feat.dcperiod(close)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod=self.base_window)

        roc_val = self.feat.roc(close, timeperiod={roc_window})

        long_setup = (close > trend) & (roc_val > 0) & (adx_val > {adx_entry})
        short_setup = (close < trend) & (roc_val < 0) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for bw, mc in product([14, 20, 26], [30, 50]):
    TEMPLATES.append({
        "name":       f"T03-B_b{bw}_m{mc}",
        "thesis":     "03",
        "descr":      f"DCPeriod Adaptive (base={bw}, max={mc})",
        "timeframes": [15, 30, 60],
        "code":       T03_B_CODE,
        "fixed":      {"base_window": bw, "max_cycle": mc},
        "params":     {},
    })

# T03-C: LinReg Slope Trend
T03_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    lr_window = {lr_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        slope = self.feat.linearreg_slope(close, timeperiod=self.lr_window)
        angle = self.feat.linearreg_angle(close, timeperiod=self.lr_window)
        forecast = self.feat.tsf(close, timeperiod=self.lr_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (slope > 0) & (angle > 5) & (close < forecast) & (adx_val > {adx_entry})
        short_setup = (slope < 0) & (angle < -5) & (close > forecast) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(slope, 0) | self.op.crossed_above(slope, 0) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for lw in [10, 14, 20]:
    TEMPLATES.append({
        "name":       f"T03-C_l{lw}",
        "thesis":     "03",
        "descr":      f"LinReg Slope (lr={lw})",
        "timeframes": [15, 30, 60],
        "code":       T03_C_CODE,
        "fixed":      {"lr_window": lw},
        "params":     {},
    })

# T03-D: Sine Crossover
T03_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    rsi_window = {rsi_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        sine, leadsine = self.feat.sine(close)
        rsi = self.feat.rsi(close, timeperiod=self.rsi_window)
        trend = self.feat.ht_trendline(close)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        cycle_up = self.op.crossed_above(sine, leadsine)
        cycle_down = self.op.crossed_below(sine, leadsine)

        long_setup = cycle_up & (rsi > 30) & (adx_val > {adx_entry})
        short_setup = cycle_down & (rsi < 70) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, trend) | self.op.crossed_above(close, trend) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for rw in [10, 14, 21]:
    TEMPLATES.append({
        "name":       f"T03-D_r{rw}",
        "thesis":     "03",
        "descr":      f"Sine Crossover (rsi={rw})",
        "timeframes": [15, 30, 60],
        "code":       T03_D_CODE,
        "fixed":      {"rsi_window": rw},
        "params":     {},
    })

# T03-E: Dispersion Entropy Proxy
T03_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    mad_window = {mad_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        mad = self.feat.rolling_mad(close, window=self.mad_window)
        std = self.feat.rolling_std(close, window=self.mad_window)
        mad_ratio = mad / std
        mad_ratio_sma = self.feat.sma(mad_ratio, timeperiod=self.mad_window)

        structured = mad_ratio < mad_ratio_sma * 0.8
        chaotic = mad_ratio > mad_ratio_sma * 1.2

        ema = self.feat.ema(close, timeperiod={ema_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > ema) & structured & (adx_val > {adx_entry})
        short_setup = (close < ema) & structured & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, ema) | self.op.crossed_above(close, ema) | chaotic | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for mw, ew in product([14, 20, 34], [13, 26, 50]):
    TEMPLATES.append({
        "name":       f"T03-E_m{mw}_e{ew}",
        "thesis":     "03",
        "descr":      f"Entropy Proxy (mad={mw}, ema={ew})",
        "timeframes": [15, 30, 60],
        "code":       T03_E_CODE,
        "fixed":      {"mad_window": mw, "ema_window": ew},
        "params":     {},
    })

# ============================================================
# THESIS 04: Microstructure Flow
# ============================================================

# T04-A: BOP + CMF Flow Detection
T04_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    cmf_window = {cmf_window}


    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bop = self.feat.bop(open_price, high, low, close)
        cmf = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        buying_pressure = (bop > 0) & (cmf > 0)
        selling_pressure = (bop < 0) & (cmf < 0)

        long_setup = buying_pressure & (adx_val > {adx_entry}) & (volume > vol_sma)
        short_setup = selling_pressure & (adx_val > {adx_entry}) & (volume > vol_sma)
        exit_setup = self.op.crossed_below(cmf, 0) | self.op.crossed_above(cmf, 0) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for cw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T04-A_c{cw}",
        "thesis":     "04",
        "descr":      f"BOP+CMF Flow (cmf={cw})",
        "timeframes": [5, 15, 30],
        "code":       T04_A_CODE,
        "fixed":      {"cmf_window": cw},
        "params":     {},
    })

# T04-B: MFI Volume-Weighted Reversal
T04_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    mfi_window = {mfi_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mfi = self.feat.mfi(high, low, close, volume, timeperiod=self.mfi_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        long_setup = (mfi < 30) & (adx_val > {adx_entry}) & (volume > vol_sma * 0.5)
        short_setup = (mfi > 70) & (adx_val > {adx_entry}) & (volume > vol_sma * 0.5)
        exit_setup = self.op.crossed_above(mfi, 50) | self.op.crossed_below(mfi, 50) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for mw in [10, 14, 21]:
    TEMPLATES.append({
        "name":       f"T04-B_m{mw}",
        "thesis":     "04",
        "descr":      f"MFI Reversal (mfi={mw})",
        "timeframes": [5, 15, 30],
        "code":       T04_B_CODE,
        "fixed":      {"mfi_window": mw},
        "params":     {},
    })

# T04-C: OI + Volume Cascade (Margin Call Proxy)
T04_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    oi_window = {oi_window}
    vol_window_val = {vol_window_val}


    def __algorithm__(self):
        close = self.data.pv_close
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        oi_sma = self.feat.sma(oi, timeperiod=self.oi_window)
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.vol_window_val)

        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        oi_drop = oi_change < -{oi_drop_threshold}
        vol_spike = matched_vol > vol_sma * {vol_spike_mult}
        price_fall = self.op.pct_change(close, periods=1) < -{price_fall_threshold}

        cascade = oi_drop & vol_spike & price_fall

        vol_collapse = matched_vol < vol_sma * 0.5
        price_stable = self.op.abs(self.op.pct_change(close, periods=1)) < {price_fall_threshold} * 0.2
        exhaustion = oi_drop & vol_collapse & price_stable

        long_setup = exhaustion
        short_setup = cascade
        exit_setup = self.op.crossed_below(close, oi_sma) | self.op.crossed_above(close, oi_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

_OI_VARIANTS = [
    ("aggr", 0.005, 1.5, 0.003),
    ("std",  0.01,  2.0, 0.005),
    ("cons", 0.02,  3.0, 0.01),
]
for ov_name, oi_drop, vol_spike, price_fall in _OI_VARIANTS:
    for ow, vw in product([10, 20], [10, 20]):
        TEMPLATES.append({
            "name":       f"T04-C_{ov_name}_o{ow}_v{vw}",
            "thesis":     "04",
            "descr":      f"OI Cascade ({ov_name}, oi={ow}, vol={vw})",
            "timeframes": [5, 15, 30],
            "code":       T04_C_CODE,
            "fixed":      {
                "oi_window": ow,
                "vol_window_val": vw,
                "oi_drop_threshold": oi_drop,
                "vol_spike_mult": vol_spike,
                "price_fall_threshold": price_fall,
            },
            "params":     {},
        })

# T04-D: Whale Footprint
T04_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    whale_window = {whale_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d

        avg_trade = matched_val / matched_vol
        avg_trade_sma = self.feat.sma(avg_trade, timeperiod=self.whale_window)
        avg_trade_std = self.feat.rolling_std(avg_trade, window=self.whale_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        whale = avg_trade > avg_trade_sma + {whale_sigma} * avg_trade_std
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.whale_window)
        price_compression = (self.feat.rolling_max(close, 10) - self.feat.rolling_min(close, 10)) / self.feat.rolling_min(close, 10) < 0.01

        long_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > {adx_entry})
        short_setup = whale & price_compression & (matched_vol > vol_sma * 1.5) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, self.feat.sma(close, 20)) | self.op.crossed_above(close, self.feat.sma(close, 20)) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for ww, ws in product([10, 20, 34], [1.5, 2.0, 2.5]):
    TEMPLATES.append({
        "name":       f"T04-D_w{ww}_s{ws}",
        "thesis":     "04",
        "descr":      f"Whale Footprint (w={ww}, sigma={ws})",
        "timeframes": [5, 15, 30],
        "code":       T04_D_CODE,
        "fixed":      {"whale_window": ww, "whale_sigma": ws},
        "params":     {},
    })

# T04-E: A/D Oscillator Divergence
T04_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    adosc_fast = {adosc_fast}
    adosc_slow = {adosc_slow}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adosc = self.feat.adosc(high, low, close, volume, fastperiod=self.adosc_fast, slowperiod=self.adosc_slow)
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        price_rising = close > self.op.previous(close)
        price_falling = close < self.op.previous(close)

        bullish_div = price_falling & (adosc > self.op.previous(adosc)) & (rsi < 40)
        bearish_div = price_rising & (adosc < self.op.previous(adosc)) & (rsi > 60)

        long_setup = bullish_div & (adx_val > {adx_entry})
        short_setup = bearish_div & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, self.feat.sma(close, 14)) | self.op.crossed_above(close, self.feat.sma(close, 14)) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for af, as_val in [(3, 10), (5, 14)]:
    TEMPLATES.append({
        "name":       f"T04-E_f{af}_s{as_val}",
        "thesis":     "04",
        "descr":      f"AD Osc Divergence (fast={af}, slow={as_val})",
        "timeframes": [5, 15, 30],
        "code":       T04_E_CODE,
        "fixed":      {"adosc_fast": af, "adosc_slow": as_val},
        "params":     {},
    })

# T04-F: OBV Trend Confirmation
T04_F_CODE = """class CustomStrategy(SimpleAlgorithm):
    obv_window = {obv_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        obv = self.feat.obv(close, volume)
        obv_sma = self.feat.sma(obv, timeperiod=self.obv_window)
        close_sma = self.feat.sma(close, timeperiod=self.obv_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close > close_sma) & (obv > obv_sma) & (adx_val > {adx_entry})
        short_setup = (close < close_sma) & (obv < obv_sma) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(obv, obv_sma) | self.op.crossed_above(obv, obv_sma) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for ow in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T04-F_o{ow}",
        "thesis":     "04",
        "descr":      f"OBV Trend (obv={ow})",
        "timeframes": [5, 15, 30],
        "code":       T04_F_CODE,
        "fixed":      {"obv_window": ow},
        "params":     {},
    })

# T04-G: Volume Flow Imbalance
T04_G_CODE = """class CustomStrategy(SimpleAlgorithm):
    imbalance_window = {imbalance_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        matched_val = self.data.fut_matched_value_vn30f1m_1d
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        oi = self.data.fut_open_interest_vn30f1m_1d

        avg_trade = matched_val / matched_vol
        close_sma = self.feat.sma(close, timeperiod=self.imbalance_window)
        oi_change = self.op.fillna(self.op.pct_change(oi, periods=1), value=0)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        smart_money_long = (oi_change > 0) & (avg_trade > self.feat.sma(avg_trade, self.imbalance_window))
        smart_money_short = (oi_change < -0.005) & (matched_vol > self.feat.sma(matched_vol, self.imbalance_window) * 1.5)

        long_setup = smart_money_long & (close > close_sma) & (adx_val > {adx_entry})
        short_setup = smart_money_short & (close < close_sma) & (adx_val > {adx_entry})
        exit_setup = self.op.crossed_below(close, close_sma) | self.op.crossed_above(close, close_sma) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for iw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T04-G_i{iw}",
        "thesis":     "04",
        "descr":      f"Volume Flow Imbalance (w={iw})",
        "timeframes": [5, 15, 30],
        "code":       T04_G_CODE,
        "fixed":      {"imbalance_window": iw},
        "params":     {},
    })

# ============================================================
# THESIS 05: Cross-Market Correlation
# ============================================================

# T05-A: Futures-VN30 Spread Reversion
T05_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    beta_window = {beta_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        beta_val = self.feat.beta(close, vn30_close, timeperiod=self.beta_window)
        spread = close - beta_val * vn30_close
        spread_z = self.feat.rolling_zscore(spread, window=self.beta_window)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        basis = close - vn30_close
        basis_sma = self.feat.sma(basis, timeperiod=self.beta_window)

        long_setup = (spread_z < -{z_entry}) & (adx_val > {adx_entry})
        short_setup = (spread_z > {z_entry}) & (adx_val > {adx_entry})
        exit_setup = self.op.between(spread_z, -1, 1) | self.op.crossed_below(adx_val, {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for bw, ze in product([10, 20, 34], [2.0, 2.5, 3.0]):
    TEMPLATES.append({
        "name":       f"T05-A_b{bw}_z{ze}",
        "thesis":     "05",
        "descr":      f"Spread Z-score (beta={bw}, z={ze})",
        "timeframes": [15, 30, 60],
        "code":       T05_A_CODE,
        "fixed":      {"beta_window": bw, "z_entry": ze},
        "params":     {},
    })

# T05-B: VN30 Momentum Confirmation
T05_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    roc_window = {roc_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        long_setup = (fut_roc > 0) & (vn30_roc > 0)
        short_setup = (fut_roc < 0) & (vn30_roc < 0)
        exit_setup = self.op.crossed_below(fut_roc, 0) | self.op.crossed_above(fut_roc, 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for rw in [3, 5, 8]:
    TEMPLATES.append({
        "name":       f"T05-B_r{rw}",
        "thesis":     "05",
        "descr":      f"VN30 Confirm (roc={rw})",
        "timeframes": [15, 30, 60],
        "code":       T05_B_CODE,
        "fixed":      {"roc_window": rw},
        "params":     {},
    })

# T05-C: Futures-Cash Basis Extreme
T05_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    basis_window = {basis_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window=self.basis_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        matched_vol = self.data.fut_matched_volume_vn30f1m_1d
        vol_sma = self.feat.sma(matched_vol, timeperiod=self.basis_window)

        long_setup = (basis_z < -{basis_entry}) & (matched_vol < vol_sma) & (adx_val > {adx_entry})
        short_setup = (basis_z > {basis_entry}) & (matched_vol < vol_sma) & (adx_val > {adx_entry})
        exit_setup = self.op.between(basis_z, -1, 1) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for bw, be in product([10, 20, 34], [2.0, 2.5]):
    TEMPLATES.append({
        "name":       f"T05-C_b{bw}_e{be}",
        "thesis":     "05",
        "descr":      f"Basis Extreme (w={bw}, entry={be})",
        "timeframes": [15, 30, 60],
        "code":       T05_C_CODE,
        "fixed":      {"basis_window": bw, "basis_entry": be},
        "params":     {},
    })

# T05-D: DJI Global Spillover
T05_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    roc_window = {roc_window}


    def __algorithm__(self):
        close = self.data.pv_close
        dji_close = self.data.pv_dji_close
        vn30_close = self.data.pv_vn30_close

        dji_roc = self.feat.roc(dji_close, timeperiod=self.roc_window)
        fut_roc = self.feat.roc(close, timeperiod=self.roc_window)
        vn30_roc = self.feat.roc(vn30_close, timeperiod=self.roc_window)

        bullish = (fut_roc > 0) & (vn30_roc > 0) & (dji_roc > 0)
        bearish = (fut_roc < 0) & (vn30_roc < 0) & (dji_roc < 0)

        long_setup = bullish
        short_setup = bearish
        exit_setup = (~bullish) & (~bearish)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for rw in [3, 5, 8]:
    TEMPLATES.append({
        "name":       f"T05-D_r{rw}",
        "thesis":     "05",
        "descr":      f"DJI Consensus (roc={rw})",
        "timeframes": [15, 30, 60],
        "code":       T05_D_CODE,
        "fixed":      {"roc_window": rw},
        "params":     {},
    })

# T05-E: Rolling Correlation Trend Filter
T05_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    correl_window = {correl_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        dji_close = self.data.pv_dji_close
        high = self.data.pv_high
        low = self.data.pv_low

        fut_vn30_correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        fut_dji_correl = self.feat.rolling_correlation(close, dji_close, window=self.correl_window)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        roc_val = self.feat.roc(close, timeperiod={roc_window})

        correl_aligned = (fut_vn30_correl > 0.5) & (fut_dji_correl > 0)
        correl_negative = (fut_vn30_correl < -0.3) | (fut_dji_correl < -0.3)

        long_setup = correl_aligned & (roc_val > 0) & (adx_val > {adx_entry})
        short_setup = correl_aligned & (roc_val < 0) & (adx_val > {adx_entry})
        exit_setup = correl_negative | self.op.crossed_below(adx_val, {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for cw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T05-E_c{cw}",
        "thesis":     "05",
        "descr":      f"Rolling Correl Filter (correl={cw})",
        "timeframes": [15, 30, 60],
        "code":       T05_E_CODE,
        "fixed":      {"correl_window": cw},
        "params":     {},
    })

# T05-F: Relative Strength Ratio
T05_F_CODE = """class CustomStrategy(SimpleAlgorithm):
    rs_window = {rs_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close

        ratio = close / vn30_close
        ratio_sma = self.feat.sma(ratio, timeperiod=self.rs_window)
        ratio_roc = self.feat.roc(ratio, timeperiod=self.rs_window)
        ratio_slope = self.feat.linearreg_slope(ratio, timeperiod=self.rs_window)

        long_setup = (ratio > ratio_sma) & (ratio_roc > 0) & (ratio_slope > 0)
        short_setup = (ratio < ratio_sma) & (ratio_roc < 0) & (ratio_slope < 0)
        exit_setup = self.op.crossed_below(ratio, ratio_sma) | self.op.crossed_above(ratio, ratio_sma)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for rw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T05-F_r{rw}",
        "thesis":     "05",
        "descr":      f"RS Ratio (rs={rw})",
        "timeframes": [15, 30, 60],
        "code":       T05_F_CODE,
        "fixed":      {"rs_window": rw},
        "params":     {},
    })

# T05-G: Correlation Breakdown Detection
T05_G_CODE = """class CustomStrategy(SimpleAlgorithm):
    correl_window = {correl_window}


    def __algorithm__(self):
        close = self.data.pv_close
        vn30_close = self.data.pv_vn30_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        correl = self.feat.rolling_correlation(close, vn30_close, window=self.correl_window)
        correl_sma = self.feat.sma(correl, window=self.correl_window)
        correl_std = self.feat.rolling_std(correl, window=self.correl_window)

        breakdown = correl < (correl_sma - 2 * correl_std)
        rebuilding = self.op.crossed_above(correl, correl_sma)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})

        long_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > {adx_entry})
        short_setup = breakdown & (volume > vol_sma * 1.5) & (adx_val > {adx_entry})
        exit_setup = rebuilding | self.op.crossed_below(adx_val, {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for cw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T05-G_c{cw}",
        "thesis":     "05",
        "descr":      f"Correlation Breakdown (correl={cw})",
        "timeframes": [15, 30, 60],
        "code":       T05_G_CODE,
        "fixed":      {"correl_window": cw},
        "params":     {},
    })

# ============================================================
# THESIS 06: Multi-Factor Composite
# ============================================================

# T06-A: Z-Score Composite — 3-Factor
T06_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}
    z_threshold = {z_threshold}


    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low

        price_z = self.feat.rolling_zscore(close, window=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod={rsi_window})
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        rsi_ok = self.op.between(rsi, 30, 70)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        return_roll = self.feat.returns(close, periods={return_window})

        core_long = (composite > self.z_threshold)
        core_short = (composite < -self.z_threshold)

        strong_long = core_long & rsi_ok & (adx_val > {adx_entry}) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & rsi_ok & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        strong_short = core_short & rsi_ok & (adx_val > {adx_entry}) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & rsi_ok & (adx_val > {adx_entry_weak}) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
"""

_ADX_ENTRY_WEAK = {5:18, 15:18, 30:15, 60:14}

for zw, zt in product([10, 20, 34], [2.0, 3.0]):
    TEMPLATES.append({
        "name":       f"T06-A_z{zw}_t{zt}",
        "thesis":     "06",
        "descr":      f"3-Factor Z (z={zw}, thr={zt})",
        "timeframes": [15, 30, 60],
        "code":       T06_A_CODE,
        "fixed":      {"z_window": zw, "z_threshold": zt},
        "params":     {},
    })

# T06-B: 4-Factor Composite
T06_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}
    z_threshold = {z_threshold}


    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume
        high = self.data.pv_high
        low = self.data.pv_low
        vn30_close = self.data.pv_vn30_close

        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vola_z = self.feat.rolling_zscore(atr_val, window=self.z_window)
        ratio = close / vn30_close
        ratio_z = self.feat.rolling_zscore(ratio, window=self.z_window)

        composite = price_z + vol_z + vola_z + ratio_z

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        return_roll = self.feat.returns(close, periods={return_window})

        core_long = (composite > self.z_threshold) & (rsi > 30) & (rsi < 70)
        core_short = (composite < -self.z_threshold) & (rsi > 30) & (rsi < 70)

        strong_long = core_long & (adx_val > {adx_entry}) & (vol_z > 0) & (return_roll > 0)
        weak_long = core_long & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        strong_short = core_short & (adx_val > {adx_entry}) & (vol_z < 0) & (return_roll < 0)
        weak_short = core_short & (adx_val > {adx_entry_weak}) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 1.0) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
"""

for zw, zt in product([10, 20, 34], [2.0, 3.0, 4.0]):
    TEMPLATES.append({
        "name":       f"T06-B_z{zw}_t{zt}",
        "thesis":     "06",
        "descr":      f"4-Factor Z (z={zw}, thr={zt})",
        "timeframes": [15, 30, 60],
        "code":       T06_B_CODE,
        "fixed":      {"z_window": zw, "z_threshold": zt},
        "params":     {},
    })

# T06-C: Multi-Layer Confirmation
T06_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    mid_window = {mid_window}
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        ema = self.feat.ema(close, timeperiod=self.mid_window)
        trend_ok = close > ema

        roc_val = self.feat.roc(close, timeperiod={roc_window})
        momentum_ok = roc_val > 0

        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        volume_ok = volume > vol_sma

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        atr_trend = atr_val > self.feat.sma(atr_val, timeperiod=self.vol_window)

        vn30_roc = self.feat.roc(vn30_close, timeperiod={roc_window})
        vn30_ok = vn30_roc > 0

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        return_roll = self.feat.returns(close, periods={return_window})

        core_long = trend_ok & momentum_ok & vn30_ok
        core_short = (~trend_ok) & (~momentum_ok) & (~vn30_ok)

        strong_long = core_long & volume_ok & atr_trend & (adx_val > {adx_entry}) & (return_roll > 0)
        weak_long = core_long & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        strong_short = core_short & volume_ok & atr_trend & (adx_val > {adx_entry}) & (return_roll < 0)
        weak_short = core_short & (adx_val > {adx_entry_weak}) & (return_roll < 0)

        exit_setup = self.op.crossed_below(close, ema) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
"""

for mw, vw, rw in product([13, 26, 40], [10, 20, 34], [5, 8]):
    TEMPLATES.append({
        "name":       f"T06-C_m{mw}_v{vw}_r{rw}",
        "thesis":     "06",
        "descr":      f"Multi-Layer (mid={mw}, vol={vw}, roc={rw})",
        "timeframes": [15, 30, 60],
        "code":       T06_C_CODE,
        "fixed":      {"mid_window": mw, "vol_window": vw, "roc_window": rw},
        "params":     {},
    })

# T06-D: Z-Score + Candlestick Confirmation
T06_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}


    def __algorithm__(self):
        close = self.data.pv_close
        open_price = self.data.pv_open
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)

        composite = price_z + mom_z + vol_z

        hammer = self.feat.hammer(open_price, high, low, close)
        engulf = self.feat.engulfing_pattern(open_price, high, low, close)
        morning = self.feat.morning_star(open_price, high, low, close)
        evening = self.feat.evening_star(open_price, high, low, close)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        return_roll = self.feat.returns(close, periods={return_window})

        bullish_pattern = hammer | engulf | morning
        bearish_pattern = evening

        long_setup = (composite > 1.5) & bullish_pattern & (adx_val > {adx_entry}) & (return_roll > 0)
        short_setup = (composite < -1.5) & bearish_pattern & (adx_val > {adx_entry}) & (return_roll < 0)
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

for zw in [10, 20, 34]:
    TEMPLATES.append({
        "name":       f"T06-D_z{zw}",
        "thesis":     "06",
        "descr":      f"Candlestick+Z (z={zw})",
        "timeframes": [15, 30, 60],
        "code":       T06_D_CODE,
        "fixed":      {"z_window": zw},
        "params":     {},
    })

# T06-E: Adaptive Regime-Weighted Composite
T06_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_window = {z_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        atr_sma = self.feat.sma(atr_val, timeperiod=20)

        strong_trend = adx_val > 25
        weak_trend = (adx_val > 20) & (adx_val <= 25)
        high_vol = atr_val > atr_sma * 1.3

        price_z = self.feat.price_z(close, timeperiod=self.z_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.z_window)
        momentum = self.feat.roc(close, timeperiod=14)
        mom_z = self.feat.rolling_zscore(momentum, window=self.z_window)
        ratio = close / vn30_close
        ratio_z = self.feat.rolling_zscore(ratio, window=self.z_window)

        if strong_trend:
            composite = price_z * 1.5 + mom_z * 1.0 + vol_z * 0.5
        elif high_vol:
            composite = price_z * 1.0 + vol_z * 1.5 + ratio_z * 0.5
        else:
            composite = price_z * 0.5 + ratio_z * 1.0 + mom_z * 0.5

        rsi = self.feat.rsi(close, timeperiod={rsi_window})
        return_roll = self.feat.returns(close, periods={return_window})

        strong_long = (composite > {z_entry}) & (adx_val > {adx_entry}) & (rsi > 40) & (return_roll > 0)
        weak_long = (composite > {z_entry}) & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        strong_short = (composite < -{z_entry}) & (adx_val > {adx_entry}) & (rsi < 60) & (return_roll < 0)
        weak_short = (composite < -{z_entry}) & (adx_val > {adx_entry_weak}) & (return_roll < 0)

        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(weak_long, position=0.5)
        self.set_positions(strong_long, position=1)
        self.set_positions(weak_short, position=-0.5)
        self.set_positions(strong_short, position=-1)
"""

for zw, ze in product([10, 20, 34], [2.0, 3.0]):
    TEMPLATES.append({
        "name":       f"T06-E_z{zw}_e{ze}",
        "thesis":     "06",
        "descr":      f"Regime-Weighted (z={zw}, entry={ze})",
        "timeframes": [15, 30, 60],
        "code":       T06_E_CODE,
        "fixed":      {"z_window": zw, "z_entry": ze},
        "params":     {},
    })

# ============================================================
# THESIS 07: Intraday Session Microstructure
# ============================================================

T07_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["09:00-09:30"]
    position_close_ranges = ["11:20-11:30"]


    def __algorithm__(self):
        close = self.data.pv_close
        volume = self.data.pv_volume

        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        mean_val = self.feat.sma(close, timeperiod={fast_window})
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        long_setup = (close > mean_val) & (volume > vol_sma) & (return_roll > 0)
        short_setup = (close < mean_val) & (volume > vol_sma) & (return_roll < 0)
        exit_setup = (return_roll < 0) | (return_roll > 0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T07_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["10:30-11:15"]
    position_close_ranges = ["11:20-11:30"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        rsi_val = self.feat.rsi(close, timeperiod={rsi_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (rsi_val < 30) & (volume > vol_sma * 0.7) & (adx_val < 20)
        short_setup = (rsi_val > 70) & (volume > vol_sma * 0.7) & (adx_val < 20)
        exit_setup = self.op.crossed_above(rsi_val, 50) | self.op.crossed_below(rsi_val, 50) | (adx_val > 25)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T07_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["13:00-14:15"]
    position_close_ranges = ["14:30-14:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        roc_val = self.feat.roc(close, timeperiod={roc_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (roc_val > 0) & (volume > vol_sma * {vol_mult}) & (adx_val > {adx_entry})
        short_setup = (roc_val < 0) & (volume > vol_sma * {vol_mult}) & (adx_val > {adx_entry})
        exit_setup = (roc_val < 0) | (roc_val > 0) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T07_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["13:45-14:20"]
    position_close_ranges = ["14:20-14:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        upper, mid, lower = self.feat.bbands(close, timeperiod={bb_window}, nbdevup={bb_mult}, nbdevdn={bb_mult})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        mean_val = self.feat.sma(close, timeperiod={ema_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        long_setup = (close < lower) & (volume > vol_sma) & (adx_val < 20)
        short_setup = (close > upper) & (volume > vol_sma) & (adx_val < 20)
        exit_setup = self.op.crossed_above(close, mean_val) | self.op.crossed_below(close, mean_val) | (adx_val > 25)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T07_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    position_open_ranges = ["09:00-11:30", "13:00-14:15"]
    position_close_ranges = ["11:20-11:30", "14:30-14:45"]


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window={vwap_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        upper_band = vwap_val * (1 + {z_entry} / 100)
        lower_band = vwap_val * (1 - {z_entry} / 100)

        long_setup = (close < lower_band) & (return_roll > 0) & (volume > vol_sma * 0.7)
        short_setup = (close > upper_band) & (return_roll < 0) & (volume > vol_sma * 0.7)
        exit_setup = self.op.crossed_above(close, vwap_val) | self.op.crossed_below(close, vwap_val)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

# --- T07-A: Open Drive ---
for fw, vw in product([8, 13, 20], [14, 20]):
    TEMPLATES.append({
        "name":       f"T07-A_f{fw}_v{vw}",
        "thesis":     "07",
        "descr":      f"Open Drive (fast={fw}, vol={vw})",
        "timeframes": [5, 15],
        "code":       T07_A_CODE,
        "fixed":      {"fast_window": fw, "vol_window": vw},
        "params":     {},
    })

# --- T07-B: Lunch Revert ---
for rw, vw in product([7, 10, 14], [14, 20]):
    TEMPLATES.append({
        "name":       f"T07-B_r{rw}_v{vw}",
        "thesis":     "07",
        "descr":      f"Lunch Revert (rsi={rw}, vol={vw})",
        "timeframes": [5, 15],
        "code":       T07_B_CODE,
        "fixed":      {"rsi_window": rw, "vol_window": vw},
        "params":     {},
    })

# --- T07-C: Close Squeeze ---
for rw, vw, vm in product([3, 5], [14, 20], [1.5, 2.0]):
    TEMPLATES.append({
        "name":       f"T07-C_r{rw}_v{vw}_m{vm}",
        "thesis":     "07",
        "descr":      f"Close Squeeze (roc={rw}, vol={vw}, mult={vm})",
        "timeframes": [5, 15],
        "code":       T07_C_CODE,
        "fixed":      {"roc_window": rw, "vol_window": vw, "vol_mult": vm},
        "params":     {},
    })

# --- T07-D: Pre-ATC Mean Rev ---
for bw, bm, vw in product([14, 20], [2.0, 2.5], [14, 20]):
    TEMPLATES.append({
        "name":       f"T07-D_b{bw}_m{bm}_v{vw}",
        "thesis":     "07",
        "descr":      f"Pre-ATC Mean Rev (bb={bw}, mult={bm}, vol={vw})",
        "timeframes": [5, 15],
        "code":       T07_D_CODE,
        "fixed":      {"bb_window": bw, "bb_mult": bm, "vol_window": vw},
        "params":     {},
    })

# --- T07-E: VWAP Bounce ---
for vw, ze in product([14, 20], [1.0, 2.0]):
    TEMPLATES.append({
        "name":       f"T07-E_v{vw}_z{ze}",
        "thesis":     "07",
        "descr":      f"VWAP Bounce (vwap={vw}, z={ze})",
        "timeframes": [5, 15],
        "code":       T07_E_CODE,
        "fixed":      {"vwap_window": vw, "z_entry": ze, "vol_window": 14},
        "params":     {},
    })

# ============================================================
# THESIS 08: Order Book Shadowing — Institutional Footprint Proxy
# ============================================================

T08_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    level_window = {level_window}
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        midpoint = (high + low) * 0.5
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        close_lower_half = close < midpoint
        close_upper_half = close > midpoint

        rejected_resistance = at_resistance & close_lower_half
        rejected_support = at_support & close_upper_half

        long_setup = rejected_support & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        short_setup = rejected_resistance & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll < 0)
        exit_setup = (adx_val < {adx_exit}) | (return_roll < -0.001) | (return_roll > 0.001)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T08_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    level_window = {level_window}
    vol_window = {vol_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        midpoint = (high + low) * 0.5
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        natr_val = self.feat.natr(high, low, close, timeperiod=14)
        natr_ma = self.feat.sma(natr_val, timeperiod=14)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        close_lower_half = close < midpoint
        close_upper_half = close > midpoint
        vol_spike = volume > vol_sma * 1.5
        tight_range = (high - low) < natr_val * 0.8

        short_setup = at_resistance & vol_spike & tight_range & close_lower_half & (adx_val > {adx_entry_weak}) & (return_roll < 0)
        long_setup = at_support & vol_spike & tight_range & close_upper_half & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        exit_setup = (adx_val < {adx_exit}) | (return_roll < -0.001) | (return_roll > 0.001) | (natr_val > natr_ma * 2.0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T08_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    natr_window = {natr_window}
    level_window = {level_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        natr_val = self.feat.natr(high, low, close, timeperiod=self.natr_window)
        natr_sma = self.feat.sma(natr_val, timeperiod=self.natr_window)
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        tight_range = natr_val < natr_sma * 0.8

        short_setup = at_resistance & tight_range & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll < 0)
        long_setup = at_support & tight_range & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        exit_setup = (adx_val < {adx_exit}) | (return_roll < -0.001) | (return_roll > 0.001) | (natr_val > natr_sma * 2.0)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T08_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    level_window = {level_window}
    vwap_window = {vwap_window}
    vwap_mult = {vwap_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        res_level = self.feat.rolling_max(close, window=self.level_window)
        sup_level = self.feat.rolling_min(close, window=self.level_window)
        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window=self.vwap_window)
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        at_resistance = close >= res_level * 0.995
        at_support = close <= sup_level * 1.005
        over_extended_short = at_resistance & (close > vwap_val * (1 + self.vwap_mult / 100))
        over_extended_long = at_support & (close < vwap_val * (1 - self.vwap_mult / 100))

        short_setup = over_extended_short & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll < 0)
        long_setup = over_extended_long & (volume > vol_sma) & (adx_val > {adx_entry_weak}) & (return_roll > 0)
        exit_setup = (self.op.between(close, vwap_val * 0.999, vwap_val * 1.001)) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

T08_E_CODE = """class CustomStrategy(SimpleAlgorithm):
    composite_window = {composite_window}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        price_z = self.feat.rolling_zscore(close, window=self.composite_window)
        vol_z = self.feat.volume_z(volume, timeperiod=self.composite_window)
        natr_val = self.feat.natr(high, low, close, timeperiod=14)
        range_z = self.feat.rolling_zscore(natr_val, window=self.composite_window)
        mom = self.feat.roc(close, timeperiod={roc_window})
        mom_z = self.feat.rolling_zscore(mom, window=self.composite_window)

        composite = price_z + vol_z + (-range_z) + mom_z

        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        long_setup = (composite > {composite_entry}) & (volume > vol_sma) & (adx_val > {adx_entry}) & (return_roll > 0)
        short_setup = (composite < -{composite_entry}) & (volume > vol_sma) & (adx_val > {adx_entry}) & (return_roll < 0)
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < {adx_exit})

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
"""

# --- T08-A: Key Level Wick Rejection ---
for lw, vw in product([14, 20, 34], [14, 20]):
    TEMPLATES.append({
        "name":       f"T08-A_l{lw}_v{vw}",
        "thesis":     "08",
        "descr":      f"Key Level Wick Rejection (level={lw}, vol={vw})",
        "timeframes": [15, 30, 60],
        "code":       T08_A_CODE,
        "fixed":      {"level_window": lw, "vol_window": vw},
        "params":     {},
    })

# --- T08-B: Volume Climax Absorption ---
for lw, vw in product([14, 20], [14, 20]):
    TEMPLATES.append({
        "name":       f"T08-B_l{lw}_v{vw}",
        "thesis":     "08",
        "descr":      f"Volume Climax Absorption (level={lw}, vol={vw})",
        "timeframes": [15, 30, 60],
        "code":       T08_B_CODE,
        "fixed":      {"level_window": lw, "vol_window": vw},
        "params":     {},
    })

# --- T08-C: Range Compression Absorption ---
for nw, lw in product([10, 14], [14, 20]):
    TEMPLATES.append({
        "name":       f"T08-C_n{nw}_l{lw}",
        "thesis":     "08",
        "descr":      f"Range Compression Absorption (natr={nw}, level={lw})",
        "timeframes": [15, 30, 60],
        "code":       T08_C_CODE,
        "fixed":      {"natr_window": nw, "level_window": lw},
        "params":     {},
    })

# --- T08-D: VWAP Divergence at Key Level ---
for lw, vw, vm in product([14, 20], [14, 20], [1.0, 2.0]):
    TEMPLATES.append({
        "name":       f"T08-D_l{lw}_vw{vw}_m{vm}",
        "thesis":     "08",
        "descr":      f"VWAP Divergence (level={lw}, vwap={vw}, mult={vm})",
        "timeframes": [15, 30, 60],
        "code":       T08_D_CODE,
        "fixed":      {"level_window": lw, "vwap_window": vw, "vwap_mult": vm},
        "params":     {},
    })

# --- T08-E: Multi-Confirmation Composite ---
for cw, ce in product([14, 20], [2.0, 3.0, 4.0]):
    TEMPLATES.append({
        "name":       f"T08-E_c{cw}_e{ce}",
        "thesis":     "08",
        "descr":      f"Multi-Confirmation Composite (comp={cw}, entry={ce})",
        "timeframes": [15, 30, 60],
        "code":       T08_E_CODE,
        "fixed":      {"composite_window": cw, "composite_entry": ce},
        "params":     {},
    })

# ============================================================
# THESIS 09: Institutional Flow Arbitrage
# ============================================================
# Uses: pv_close, pv_high, pv_low, pv_volume (futures)
#       fut_open_interest_vn30f1m_1d, fut_matched_volume_vn30f1m_1d
#       fut_total_volume_vn30f1m_1d, fut_matched_value_vn30f1m_1d
#       pv_vn30_close (VN30 index)

# T09-A: OI Confirmation (continuous entry + ATR stop-loss + exit-called-last)
T09_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        oi_change = self.op.fillna(self.op.pct_change(fut_oi, periods=1), value=0)
        fut_ret = self.op.fillna(self.op.pct_change(close, periods=1), value=0)

        fut_bull = fut_ret > 0
        fut_bear = fut_ret < 0
        oi_up = oi_change > 0
        oi_down = oi_change < 0

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Genuine: price + OI same direction
        genuine_long = fut_bull & oi_up & (adx_val > self.adx_entry)
        genuine_short = fut_bear & oi_up & (adx_val > self.adx_entry)

        # Fade: price moves but OI drops (weak conviction)
        fade_long = fut_bear & oi_down & (adx_val > 18)
        fade_short = fut_bull & oi_down & (adx_val > 18)

        long_setup = genuine_long | fade_long
        short_setup = genuine_short | fade_short
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)
"""

TEMPLATES.append({
    "name":       "T09-A",
    "thesis":     "09",
    "descr":      "OI Confirmation",
    "timeframes": [60],
    "code":       T09_A_CODE,
    "fixed":      {"adx_entry": 18, "adx_exit": 12, "atr_stop_mult": 4.0},
    "params":     {},
})

# T09-B: Flow Divergence (continuous entry + ATR stop-loss + exit-called-last)
T09_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        fut_matched = self.data.fut_matched_value_vn30f1m_1d
        fut_total = self.data.fut_total_value_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        matched_change = self.op.fillna(self.op.pct_change(fut_matched, periods=1), value=0)
        total_change = self.op.fillna(self.op.pct_change(fut_total, periods=1), value=0)
        fut_ret = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        vn30_ret = self.op.fillna(self.op.pct_change(vn30_close, periods=1), value=0)

        flow_up = matched_change > 0
        fut_bull = fut_ret > 0
        fut_bear = fut_ret < 0
        vn30_align = (fut_ret > 0) == (vn30_ret > 0)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        vol_sma = self.feat.sma(volume, timeperiod={vol_window})
        volume_ok = volume > vol_sma
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Strong flow: matched value rising + VN30 confirms → genuine
        strong_long = fut_bull & flow_up & vn30_align & (adx_val > self.adx_entry) & volume_ok
        strong_short = fut_bear & flow_up & vn30_align & (adx_val > self.adx_entry) & volume_ok

        # Weak flow: matched value dropping → low conviction → fade
        flow_down = matched_change < 0
        fade_long = fut_bear & flow_down & (adx_val > 18)
        fade_short = fut_bull & flow_down & (adx_val > 18)

        long_setup = strong_long | fade_long
        short_setup = strong_short | fade_short
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)
"""

TEMPLATES.append({
    "name":       "T09-B",
    "thesis":     "09",
    "descr":      "Flow Divergence",
    "timeframes": [60],
    "code":       T09_B_CODE,
    "fixed":      {"adx_entry": 18, "adx_exit": 12, "vol_window": 14, "atr_stop_mult": 4.0},
    "params":     {},
})

# T09-C: Composite Flow (continuous entry + ATR stop-loss + exit-called-last)
T09_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    window = {window}
    entry = {entry}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        fut_oi = self.data.fut_open_interest_vn30f1m_1d
        fut_matched = self.data.fut_matched_volume_vn30f1m_1d
        vn30_close = self.data.pv_vn30_close

        price_z = self.feat.rolling_zscore(close, window=self.window)
        vn30_z = self.feat.rolling_zscore(vn30_close, window=self.window)
        vol_z = self.feat.rolling_zscore(volume, window=self.window)

        oi_change = self.op.fillna(self.op.pct_change(fut_oi, periods=1), value=0)
        matched_change = self.op.fillna(self.op.pct_change(fut_matched, periods=1), value=0)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)
        fast_ma = self.feat.sma(close, timeperiod=5)

        # Binary flow signals (safe: using pct_change, not z-score on daily fields)
        oi_flow_up = oi_change > 0
        matched_flow_up = matched_change > 0
        flow_align = oi_flow_up == matched_flow_up

        composite = price_z + vn30_z + vol_z

        long_setup = (composite > self.entry) & flow_align & (adx_val > self.adx_entry)
        short_setup = (composite < -self.entry) & flow_align & (adx_val > self.adx_entry)
        atr_stop = (
            (close < fast_ma - self.atr_stop_mult * atr) |
            (close > fast_ma + self.atr_stop_mult * atr)
        )
        exit_setup = (self.op.abs(composite) < 0.5) | (adx_val < self.adx_exit) | atr_stop

        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)
        self.set_positions(exit_setup, position=0)
"""

TEMPLATES.append({
    "name":       "T09-C",
    "thesis":     "09",
    "descr":      "Composite Flow",
    "timeframes": [60],
    "code":       T09_C_CODE,
    "fixed":      {"window": 20, "entry": 2.0, "adx_entry": 18, "adx_exit": 12, "atr_stop_mult": 4.0},
    "params":     {},
})

# ============================================================
# THESIS 10: Regime-based Mean Reversion
# ============================================================

# T10-A: Simple Regime Dip/Rally (separate stop for trend vs MR entries)
T10_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = {sideways_buffer}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ma200 = self.feat.sma(close, timeperiod={ma200_window})
        ma20 = self.feat.sma(close, timeperiod={ma20_window})
        ratio = close / ma200
        warmup = ma200 > 0

        bull = warmup & (ratio > 1 + self.sideways_buffer)
        bear = warmup & (ratio < 1 - self.sideways_buffer)
        sideways = warmup & ~bull & ~bear

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)

        no_long_trend = close >= ma20 - self.atr_stop_mult * atr
        no_short_trend = close <= ma20 + self.atr_stop_mult * atr
        no_long_mr = close >= lower_q - self.atr_stop_mult * atr
        no_short_mr = close <= upper_q + self.atr_stop_mult * atr
        atr_stop_long = close < ma20 - self.atr_stop_mult * atr
        atr_stop_short = close > ma20 + self.atr_stop_mult * atr

        dip_long = bull & (close < ma20) & (adx_val > self.adx_entry) & no_long_trend
        rally_short = bear & (close > ma20) & (adx_val > self.adx_entry) & no_short_trend
        mr_long = sideways & (close < lower_q) & (adx_val < self.adx_entry) & no_long_mr
        mr_short = sideways & (close > upper_q) & (adx_val < self.adx_entry) & no_short_mr

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (adx_val < self.adx_exit)

        long_signal = long_setup & (~atr_stop_long)
        short_signal = short_setup & (~atr_stop_short)

        self.set_positions(exit_setup | atr_stop_long | atr_stop_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T10-A",
    "thesis":     "10",
    "descr":      "Regime Dip/Rally",
    "timeframes": [15, 30, 60],
    "code":       T10_A_CODE,
    "fixed":      {"ma200_window": 200, "ma20_window": 20, "sideways_buffer": 0.02, "adx_window": 14, "adx_entry": 20, "adx_exit": 15, "atr_stop_mult": 2.5},
    "params":     {},
})

# T10-B: Confirmed Regime Entries (signal masking)
T10_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = {sideways_buffer}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ma200 = self.feat.sma(close, timeperiod={ma200_window})
        ma20 = self.feat.sma(close, timeperiod={ma20_window})
        ratio = close / ma200
        warmup = ma200 > 0

        bull = warmup & (ratio > 1 + self.sideways_buffer)
        bear = warmup & (ratio < 1 - self.sideways_buffer)
        sideways = warmup & ~bull & ~bear

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.2)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.8)

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)

        no_long_trend = close >= ma20 - self.atr_stop_mult * atr
        no_short_trend = close <= ma20 + self.atr_stop_mult * atr
        no_long_mr = close >= lower_q - self.atr_stop_mult * atr
        no_short_mr = close <= upper_q + self.atr_stop_mult * atr
        atr_stop_long = close < ma20 - self.atr_stop_mult * atr
        atr_stop_short = close > ma20 + self.atr_stop_mult * atr

        dip_long = bull & (close < ma20) & (adx_val > self.adx_entry) & no_long_trend
        rally_short = bear & (close > ma20) & (adx_val > self.adx_entry) & no_short_trend
        mr_long = sideways & (close < lower_q) & (adx_val < self.adx_entry) & no_long_mr
        mr_short = sideways & (close > upper_q) & (adx_val < self.adx_entry) & no_short_mr

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (adx_val < self.adx_exit)

        long_signal = long_setup & (~atr_stop_long)
        short_signal = short_setup & (~atr_stop_short)

        self.set_positions(exit_setup | atr_stop_long | atr_stop_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T10-B",
    "thesis":     "10",
    "descr":      "Confirmed Regime Entries",
    "timeframes": [15, 30],
    "code":       T10_B_CODE,
    "fixed":      {"ma200_window": 200, "ma20_window": 20, "sideways_buffer": 0.02, "adx_window": 14, "adx_entry": 22, "adx_exit": 15, "vol_window": 14, "atr_stop_mult": 2.5},
    "params":     {},
})

# T10-C: Regime Band Oscillator (signal masking)
T10_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_buffer = {sideways_buffer}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        ma200 = self.feat.sma(close, timeperiod={ma200_window})
        ratio = close / ma200
        warmup = ma200 > 0

        bull = warmup & (ratio > 1 + self.sideways_buffer)
        bear = warmup & (ratio < 1 - self.sideways_buffer)
        sideways = warmup & ~bull & ~bear

        ma20 = self.feat.sma(close, timeperiod=20)
        upper, mid, lower = self.feat.bbands(close, timeperiod={bb_window}, nbdevup={bb_mult}, nbdevdn={bb_mult})
        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        atr = self.feat.atr(high, low, close, timeperiod=14)

        lower_q = self.feat.rolling_quantile(close, window=20, q=0.1)
        upper_q = self.feat.rolling_quantile(close, window=20, q=0.9)

        no_long_trend = close >= ma20 - self.atr_stop_mult * atr
        no_short_trend = close <= ma20 + self.atr_stop_mult * atr
        no_long_mr = close >= lower_q - self.atr_stop_mult * atr
        no_short_mr = close <= upper_q + self.atr_stop_mult * atr
        atr_stop_long = close < ma20 - self.atr_stop_mult * atr
        atr_stop_short = close > ma20 + self.atr_stop_mult * atr

        dip_long = bull & (close < lower) & (adx_val > self.adx_entry) & no_long_trend
        rally_short = bear & (close > upper) & (adx_val > self.adx_entry) & no_short_trend
        mr_long = sideways & (close < lower_q) & (adx_val < self.adx_entry) & no_long_mr
        mr_short = sideways & (close > upper_q) & (adx_val < self.adx_entry) & no_short_mr

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short
        exit_setup = (adx_val < self.adx_exit)

        long_signal = long_setup & (~atr_stop_long)
        short_signal = short_setup & (~atr_stop_short)

        self.set_positions(exit_setup | atr_stop_long | atr_stop_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T10-C",
    "thesis":     "10",
    "descr":      "Regime Band Oscillator",
    "timeframes": [30, 60],
    "code":       T10_C_CODE,
    "fixed":      {"ma200_window": 200, "bb_window": 20, "bb_mult": 2.0, "sideways_buffer": 0.02, "adx_window": 14, "adx_entry": 20, "adx_exit": 15, "atr_stop_mult": 2.5},
    "params":     {},
})

# ============================================================
# THESIS 11: VWAP Basis Reversion
# ============================================================

# T11-A: VWAP Basis Dual Z-Score + Regime Switching (MR | TF)
T11_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_entry = {z_entry}
    z_exit = {z_exit}
    atr_stop_mult = 2.5


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window={vwap_window})
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window={vwap_window})

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window={vwap_window})

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = close > ma20 + self.atr_stop_mult * atr
        trend_down = close < ma20 - self.atr_stop_mult * atr

        mr_long = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (~trend_down)
        mr_short = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (~trend_up)
        tf_long = trend_up
        tf_short = trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_setup = exit_reversion & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

for vw, ze in product([14, 20, 34], [1.5, 2.0, 2.5]):
    TEMPLATES.append({
        "name":       f"T11-A_v{vw}_z{ze}",
        "thesis":     "11",
        "descr":      f"VWAP Basis Dual Z (vwap={vw}, entry={ze})",
        "timeframes": [15, 30],
        "code":       T11_A_CODE,
        "fixed":      {"vwap_window": vw, "z_entry": ze, "z_exit": 1.0},
        "params":     {},
    })

# T11-B: VWAP Basis + ADX Filter + Regime Switching
T11_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_entry = {z_entry}
    z_exit = {z_exit}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window={vwap_window})
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window={vwap_window})

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window={vwap_window})

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = (close > ma20 + 2.5 * atr) & (adx_val < {adx_max})
        trend_down = (close < ma20 - 2.5 * atr) & (adx_val < {adx_max})

        mr_long = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (adx_val < {adx_max}) & (~trend_down)
        mr_short = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (adx_val < {adx_max}) & (~trend_up)
        tf_long = trend_up
        tf_short = trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_adx = adx_val > {adx_exit}
        exit_setup = (exit_reversion | exit_adx) & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

for vw, ze, am in product([14, 20], [1.5, 2.0], [18, 22]):
    TEMPLATES.append({
        "name":       f"T11-B_v{vw}_z{ze}_a{am}",
        "thesis":     "11",
        "descr":      f"VWAP Basis + ADX (vwap={vw}, entry={ze}, adx_max={am})",
        "timeframes": [15],
        "code":       T11_B_CODE,
        "fixed":      {"vwap_window": vw, "z_entry": ze, "z_exit": 1.0, "adx_window": 14, "adx_max": am, "adx_exit": 15},
        "params":     {},
    })

# T11-C: VWAP Basis + ATR Regime Switching (MR | TF)
T11_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_entry = {z_entry}
    z_exit = {z_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window={vwap_window})
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window={vwap_window})

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window={vwap_window})

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = close > ma20 + self.atr_stop_mult * atr
        trend_down = close < ma20 - self.atr_stop_mult * atr

        mr_long = (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (~trend_down)
        mr_short = (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (~trend_up)
        tf_long = trend_up
        tf_short = trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_setup = exit_reversion & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

for vw, ze, am in product([14, 20], [1.5, 2.0], [2.0, 3.0]):
    TEMPLATES.append({
        "name":       f"T11-C_v{vw}_z{ze}_m{am}",
        "thesis":     "11",
        "descr":      f"VWAP Basis + ATR Stop (vwap={vw}, entry={ze}, mult={am})",
        "timeframes": [15, 30],
        "code":       T11_C_CODE,
        "fixed":      {"vwap_window": vw, "z_entry": ze, "z_exit": 1.0, "atr_stop_mult": am},
        "params":     {},
    })

# T11-D: VWAP Basis Regime Switching (ADX-based MR | TF)
T11_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    z_entry = {z_entry}
    z_exit = {z_exit}
    atr_stop_mult = {atr_stop_mult}


    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume
        vn30_close = self.data.pv_vn30_close

        vwap_val = self.feat.rolling_vwap(high, low, close, volume, window={vwap_window})
        vwap_dist = close - vwap_val
        vwap_dist_z = self.feat.rolling_zscore(vwap_dist, window={vwap_window})

        basis = close - vn30_close
        basis_z = self.feat.rolling_zscore(basis, window={vwap_window})

        adx_val = self.feat.adx(high, low, close, timeperiod={adx_window})
        ranging = adx_val < {adx_exit}
        trending = adx_val > {adx_entry}

        atr = self.feat.atr(high, low, close, timeperiod=14)
        ma20 = self.feat.sma(close, timeperiod=20)
        trend_up = close > ma20 + self.atr_stop_mult * atr
        trend_down = close < ma20 - self.atr_stop_mult * atr

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window={return_window})

        range_to_trend = self.op.crossed_above(adx_val, {adx_entry})
        trend_to_range = self.op.crossed_below(adx_val, {adx_exit})

        mr_long = ranging & (vwap_dist_z < -self.z_entry) & (basis_z < -self.z_entry) & (~trend_down)
        mr_short = ranging & (vwap_dist_z > self.z_entry) & (basis_z > self.z_entry) & (~trend_up)

        tf_long = trending & (close > vwap_val) & (basis > 0) & (return_roll > 0) & trend_up
        tf_short = trending & (close < vwap_val) & (basis < 0) & (return_roll < 0) & trend_down

        long_setup = mr_long | tf_long
        short_setup = mr_short | tf_short

        exit_reversion = (self.op.abs(vwap_dist_z) < self.z_exit) | (self.op.abs(basis_z) < self.z_exit)
        exit_regime = range_to_trend | trend_to_range
        exit_setup = (exit_reversion | exit_regime) & (~trend_up) & (~trend_down)

        long_signal = long_setup & (~exit_setup)
        short_signal = short_setup & (~exit_setup)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

for vw, ze, ae, ax, am in product([14, 20], [1.5, 2.0], [22, 25], [15, 18], [2.5, 3.5]):
    TEMPLATES.append({
        "name":       f"T11-D_v{vw}_z{ze}_ae{ae}_ax{ax}_m{am}",
        "thesis":     "11",
        "descr":      f"VWAP Basis Regime Switch (vwap={vw}, entry={ze}, adx_entry={ae}, adx_exit={ax}, atr={am})",
        "timeframes": [15, 30],
        "code":       T11_D_CODE,
        "fixed":      {"vwap_window": vw, "z_entry": ze, "z_exit": 1.0,
                       "adx_window": 14, "adx_entry": ae, "adx_exit": ax,
                       "return_window": 5, "atr_stop_mult": am},
        "params":     {},
    })

print(f"  OK Registered {len(TEMPLATES)} template definitions")


# ---------------------------------------------------------------------------
# Main Generation
# ---------------------------------------------------------------------------

def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = []
    seq = 0

    for tmpl in TEMPLATES:
        name = tmpl["name"]
        thesis = tmpl["thesis"]
        descr = tmpl["descr"]
        code_template = tmpl["code"]
        fixed = tmpl["fixed"]
        param_grid = tmpl["params"]
        timeframes = tmpl["timeframes"]

        param_keys = list(param_grid.keys())
        param_values = list(param_grid.values())

        # Build combinations
        if param_values:
            combinations = list(product(*param_values))
        else:
            combinations = [()]  # one combination with no extra params

        total_vars = len(timeframes) * len(combinations)
        print(f"  [{name}] {descr}: generating {total_vars} variants ({len(timeframes)} TFs x {len(combinations)} params)...")

        for tf in timeframes:
            tw = TF_WINDOWS[tf]
            adx_entry = ADX_ENTRY[tf]
            adx_exit = ADX_EXIT[tf]

            for combo in combinations:
                seq += 1
                params = dict(fixed)

                # Add combo params
                for i, k in enumerate(param_keys):
                    params[k] = combo[i]

                # Inject TF-specific windows (only as fallback if not set by template)
                tf_defaults = {
                    "rsi_window":    tw["rsi"],
                    "adx_window":    tw["adx"],
                    "vol_window":    tw["vol"],
                    "roc_window":    tw["roc"],
                    "ema_window":    tw["ema"],
                    "return_window": tw["return_periods"],
                    "max_cycle":     tw["max_cycle"],
                    "adx_entry":     adx_entry,
                    "adx_exit":      adx_exit,
                    "adx_entry_weak": ADX_ENTRY_WEAK[tf],
                }
                for k, v in tf_defaults.items():
                    if k not in params:
                        params[k] = v

                # Build code with substitutions
                code = code_template
                for k, v in params.items():
                    code = code.replace("{" + k + "}", str(v))

                # Check for unfilled placeholders
                unfilled = re.findall(r'\{(\w+)\}', code)
                if unfilled:
                    print(f"    ⚠ {name} tf={tf} seq={seq}: unfilled placeholders: {unfilled}")

                # Resolve summary/idea
                base = _base_template_name(name)
                summary, idea = TEMPLATE_META.get(base, (descr, descr))

                # Write file into thesis subfolder
                folder = THESIS_FOLDERS.get(thesis, "other")
                os.makedirs(os.path.join(OUTPUT_DIR, folder), exist_ok=True)
                fname = f"{_safe_name(name)}_{tf}min_{seq:04d}.py"
                fpath = os.path.join(OUTPUT_DIR, folder, fname)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(HEADER.format(name=name, summary=summary, idea=idea))
                    f.write(code)
                    f.write("\n")

                # Build param str for index
                param_str = ";".join(f"{k}={v}" for k, v in sorted(params.items()))

                rows.append({
                    "filepath":     f"{folder}/{fname}",
                    "thesis_group": thesis,
                    "template":     name,
                    "timeframe":    f"{tf}min",
                    "description":  descr,
                    "params":       param_str,
                })

    # Write index.csv
    with open(INDEX_PATH, "w", encoding="utf-8", newline="") as f:
        f.write("filepath,thesis_group,template,timeframe,description,params\n")
        for r in rows:
            f.write(f"{r['filepath']},{r['thesis_group']},{r['template']},{r['timeframe']},\"{r['description']}\",\"{r['params']}\"\n")

    print(f"\nOK Generated {len(rows)} strategy variants")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Index:  {INDEX_PATH}")

    return rows


# ============================================================
# THESIS 12: Kalman Filter Regime Switching
# ============================================================

# T12-A: KF Dip/Rally — standard KF regime + ATR stop
T12_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_entry = {sideways_buffer}
    kf_z_entry = {kf_z_entry}
    kf_z_mr_entry = {kf_z_mr_entry}
    atr_stop_mult = {atr_stop_mult}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kalman_state = self.feat.sma(close, timeperiod=10)
        kf_residual = close - kalman_state
        kf_dev = close / kalman_state - 1
        residual_std = self.feat.rolling_std(kf_residual, 20)
        kf_z = kf_residual / self.op.fillna(residual_std, 1.0)

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        kf_trend_up = kf_dev > self.sideways_entry
        kf_trend_down = kf_dev < -self.sideways_entry
        kf_sideways = ~kf_trend_up & ~kf_trend_down

        atr_stop_long = close < kalman_state - self.atr_stop_mult * atr_val
        atr_stop_short = close > kalman_state + self.atr_stop_mult * atr_val

        dip_long = kf_trend_up & (kf_z < -self.kf_z_entry) & (adx_val > self.adx_entry)
        rally_short = kf_trend_down & (kf_z > self.kf_z_entry) & (adx_val > self.adx_entry)
        mr_long = kf_sideways & (kf_z < -self.kf_z_mr_entry)
        mr_short = kf_sideways & (kf_z > self.kf_z_mr_entry)

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short

        exit_long = (kf_z > 0.2) | (adx_val < self.adx_exit) | atr_stop_long
        exit_short = (kf_z < -0.2) | (adx_val < self.adx_exit) | atr_stop_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T12-A",
    "thesis":     "12",
    "descr":      "KF Dip/Rally",
    "timeframes": [15, 30, 60],
    "code":       T12_A_CODE,
    "fixed":      {"sideways_buffer": 0.02, "kf_z_entry": 1.5, "kf_z_mr_entry": 2.0, "atr_stop_mult": 2.5, "adx_entry": 20, "adx_exit": 15},
    "params":     {},
})

# T12-B: KF Mean Reversion
T12_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_entry = {sideways_buffer}
    kf_z_mr_entry = {kf_z_mr_entry}
    atr_stop_mult = {atr_stop_mult}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kalman_state = self.feat.sma(close, timeperiod=10)
        kf_residual = close - kalman_state
        kf_dev = close / kalman_state - 1
        residual_std = self.feat.rolling_std(kf_residual, 20)
        kf_z = kf_residual / self.op.fillna(residual_std, 1.0)

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        kf_trend_up = kf_dev > self.sideways_entry
        kf_trend_down = kf_dev < -self.sideways_entry
        kf_sideways = ~kf_trend_up & ~kf_trend_down

        atr_stop_long = close < kalman_state - self.atr_stop_mult * atr_val
        atr_stop_short = close > kalman_state + self.atr_stop_mult * atr_val

        dip_long = kf_trend_up & (kf_z < -1.0) & (adx_val > self.adx_entry)
        rally_short = kf_trend_down & (kf_z > 1.0) & (adx_val > self.adx_entry)
        mr_long = kf_sideways & (kf_z < -self.kf_z_mr_entry)
        mr_short = kf_sideways & (kf_z > self.kf_z_mr_entry)

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short

        exit_long = (kf_z > 0.2) | (adx_val < self.adx_exit) | atr_stop_long
        exit_short = (kf_z < -0.2) | (adx_val < self.adx_exit) | atr_stop_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T12-B",
    "thesis":     "12",
    "descr":      "KF Mean Reversion",
    "timeframes": [15, 30],
    "code":       T12_B_CODE,
    "fixed":      {"sideways_buffer": 0.02, "kf_z_mr_entry": 2.0, "atr_stop_mult": 2.5, "adx_entry": 20, "adx_exit": 15},
    "params":     {},
})

# T12-C: KF + ADX Confirmed
T12_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_entry = {sideways_buffer}
    kf_z_entry = {kf_z_entry}
    kf_z_mr_entry = {kf_z_mr_entry}
    atr_stop_mult = {atr_stop_mult}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kalman_state = self.feat.sma(close, timeperiod=10)
        kf_residual = close - kalman_state
        kf_dev = close / kalman_state - 1
        residual_std = self.feat.rolling_std(kf_residual, 20)
        kf_z = kf_residual / self.op.fillna(residual_std, 1.0)

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        kf_trend_up = kf_dev > self.sideways_entry
        kf_trend_down = kf_dev < -self.sideways_entry
        kf_sideways = ~kf_trend_up & ~kf_trend_down

        atr_stop_long = close < kalman_state - self.atr_stop_mult * atr_val
        atr_stop_short = close > kalman_state + self.atr_stop_mult * atr_val

        dip_long = kf_trend_up & (kf_z < -self.kf_z_entry) & (adx_val > self.adx_entry)
        rally_short = kf_trend_down & (kf_z > self.kf_z_entry) & (adx_val > self.adx_entry)
        mr_long = kf_sideways & (kf_z < -self.kf_z_mr_entry) & (adx_val < self.adx_entry)
        mr_short = kf_sideways & (kf_z > self.kf_z_mr_entry) & (adx_val < self.adx_entry)

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short

        exit_long = (kf_z > 0.2) | (adx_val < self.adx_exit) | atr_stop_long
        exit_short = (kf_z < -0.2) | (adx_val < self.adx_exit) | atr_stop_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T12-C",
    "thesis":     "12",
    "descr":      "KF + ADX Confirmed",
    "timeframes": [30, 60],
    "code":       T12_C_CODE,
    "fixed":      {"sideways_buffer": 0.02, "kf_z_entry": 1.5, "kf_z_mr_entry": 2.0, "atr_stop_mult": 2.5, "adx_entry": 20, "adx_exit": 15},
    "params":     {},
})

# T12-D: KF + Z Combo
T12_D_CODE = """class CustomStrategy(SimpleAlgorithm):
    sideways_entry = {sideways_buffer}
    kf_z_entry = {kf_z_entry}
    kf_z_mr_entry = {kf_z_mr_entry}
    atr_stop_mult = {atr_stop_mult}
    adx_entry = {adx_entry}
    adx_exit = {adx_exit}

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low

        kalman_state = self.feat.sma(close, timeperiod=10)
        kf_residual = close - kalman_state
        kf_dev = close / kalman_state - 1
        residual_std = self.feat.rolling_std(kf_residual, 20)
        kf_z = kf_residual / self.op.fillna(residual_std, 1.0)
        residual_z = self.feat.rolling_zscore(kf_residual, 20)

        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)

        kf_trend_up = kf_dev > self.sideways_entry
        kf_trend_down = kf_dev < -self.sideways_entry
        kf_sideways = ~kf_trend_up & ~kf_trend_down

        atr_stop_long = close < kalman_state - self.atr_stop_mult * atr_val
        atr_stop_short = close > kalman_state + self.atr_stop_mult * atr_val

        dip_long = kf_trend_up & (kf_z < -self.kf_z_entry) & (residual_z < -1.0) & (adx_val > self.adx_entry)
        rally_short = kf_trend_down & (kf_z > self.kf_z_entry) & (residual_z > 1.0) & (adx_val > self.adx_entry)
        mr_long = kf_sideways & (kf_z < -self.kf_z_mr_entry) & (residual_z < -1.5)
        mr_short = kf_sideways & (kf_z > self.kf_z_mr_entry) & (residual_z > 1.5)

        long_setup = dip_long | mr_long
        short_setup = rally_short | mr_short

        exit_long = (kf_z > 0.2) | (adx_val < self.adx_exit) | atr_stop_long
        exit_short = (kf_z < -0.2) | (adx_val < self.adx_exit) | atr_stop_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(exit_short, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T12-D",
    "thesis":     "12",
    "descr":      "KF + Z Combo",
    "timeframes": [15, 30, 60],
    "code":       T12_D_CODE,
    "fixed":      {"sideways_buffer": 0.02, "kf_z_entry": 1.5, "kf_z_mr_entry": 2.0, "atr_stop_mult": 2.5, "adx_entry": 20, "adx_exit": 15},
    "params":     {},
})

# ============================================================
# THESIS 13: CMF + Bollinger Squeeze Breakout
# ============================================================

T13_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    cmf_window = 20
    adx_exit = 14
    atr_mult = 2.5
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        cmf_val = self.feat.cmf(high, low, close, volume, timeperiod=self.cmf_window)
        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (cmf_val > 0) & (volume > vol_sma)
        rally_short = (close < bb_lower) & (cmf_val < 0) & (volume > vol_sma)

        long_signal = dip_long
        short_signal = rally_short

        exit_setup = (adx_val < self.adx_exit) | atr_stop_long | atr_stop_short | trailing_long | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T13-A",
    "thesis":     "13",
    "descr":      "CMF + Squeeze Breakout",
    "timeframes": [15, 30, 60],
    "code":       T13_A_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "cmf_window": 20, "adx_exit": 14, "atr_mult": 2.5, "vol_window": 20},
    "params":     {},
})

# ============================================================
# THESIS 14: BB Squeeze Reversal
# ============================================================

T14_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        atr_val = self.feat.atr(high, low, close, timeperiod=self.bb_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (volume > vol_sma)
        rally_short = (close < bb_lower) & (volume > vol_sma)

        long_signal = dip_long
        short_signal = rally_short

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(long_signal, position=1)

        self.set_positions(exit_short, position=0)
        self.set_positions(short_signal, position=-1)
"""

T14_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20
    max_hold = 15

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        atr_val = self.feat.atr(high, low, close, timeperiod=self.bb_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        dip_long = (close > bb_upper) & (volume > vol_sma)
        rally_short = (close < bb_lower) & (volume > vol_sma)

        long_signal = dip_long
        short_signal = rally_short

        bars_long = self.op.bars_since(long_signal)
        bars_short = self.op.bars_since(short_signal)
        timeout_long = bars_long > self.max_hold
        timeout_short = bars_short > self.max_hold

        exit_long = atr_stop_long | trailing_long | timeout_long
        exit_short = atr_stop_short | trailing_short | timeout_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0)
        self.set_positions(long_signal, position=1)

        self.set_positions(exit_short, position=0)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T14-A",
    "thesis":     "14",
    "descr":      "BB Squeeze Reversal",
    "timeframes": [15, 30, 60],
    "code":       T14_A_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "atr_mult": 2.0, "vol_window": 20},
    "params":     {},
})
TEMPLATES.append({
    "name":       "T14-C",
    "thesis":     "14",
    "descr":      "BB Squeeze TimeStop",
    "timeframes": [15, 30, 60],
    "code":       T14_C_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "atr_mult": 2.0, "vol_window": 20, "max_hold": 15},
    "params":     {},
})

# ============================================================
# THESIS 15: MAVP Adaptive Momentum
# ============================================================

T15_MAVP_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    fast_limit = 0.5
    slow_limit = 0.05
    atr_mult = 1
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        mama, fama = self.feat.mama(close, fastlimit=self.fast_limit, slowlimit=self.slow_limit)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=3)

        atr_stop_long = close < (fama - self.atr_mult * atr_val)
        atr_stop_short = close > (fama + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(high, 8) - (1.2 * atr_val))
        trailing_short = close > (self.feat.rolling_min(low, 8) + (1.2 * atr_val))

        long_setup = (close > fama) & (volume > vol_sma) & (adx_val > 18) & (return_roll > 0)
        short_setup = (close < fama) & (volume > vol_sma) & (adx_val > 18) & (return_roll < 0)

        exit_long = atr_stop_long | trailing_long
        exit_short = atr_stop_short | trailing_short

        long_signal = long_setup & (~exit_long)
        short_signal = short_setup & (~exit_short)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_long, position=0.0)
        self.set_positions(exit_short, position=0.0)

        self.set_positions(long_signal, position=0.8)
        self.set_positions(short_signal, position=-0.8)
"""

TEMPLATES.append({
    "name":       "T15-mavp",
    "thesis":     "15",
    "descr":      "MAVP Adaptive Trend",
    "timeframes": [15, 30, 60],
    "code":       T15_MAVP_A_CODE,
    "fixed":      {"fast_limit": 0.5, "slow_limit": 0.05, "atr_mult": 1, "vol_window": 20},
    "params":     {},
})

T15_MAVP_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_nbdev = 2
    adx_entry = 22
    atr_mult = 2.0
    vol_window = 20
    minperiod = 8
    maxperiod = 30

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        dc_period = self.op.fillna(self.feat.dcperiod(close), 20)
        dc_smooth = self.feat.rolling_max(dc_period, 5)
        mavp_ma = self.feat.mavp(close, periods=dc_smooth, minperiod=self.minperiod, maxperiod=self.maxperiod, matype=0)

        bb_upper = mavp_ma + self.feat.rolling_std(close, 20) * self.bb_nbdev
        bb_lower = mavp_ma - self.feat.rolling_std(close, 20) * self.bb_nbdev

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop_long = close < (mavp_ma - self.atr_mult * atr_val)
        atr_stop_short = close > (mavp_ma + self.atr_mult * atr_val)
        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (close > bb_upper) & (adx_val > self.adx_entry) & (volume > vol_sma) & (return_roll > 0)
        short_signal = (close < bb_lower) & (adx_val > self.adx_entry) & (volume > vol_sma) & (return_roll < 0)

        adx_fade = self.op.crossed_below_value(adx_val, 18)
        exit_setup = self.op.hold_for(adx_fade | atr_stop_long | atr_stop_short | trailing_long | trailing_short, 1)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T15-mavp_B",
    "thesis":     "15",
    "descr":      "MAVP Adaptive BBands",
    "timeframes": [15, 30, 60],
    "code":       T15_MAVP_B_CODE,
    "fixed":      {"bb_nbdev": 2, "adx_entry": 22, "atr_mult": 2.0, "vol_window": 20, "minperiod": 8, "maxperiod": 30},
    "params":     {},
})

T15_MAVP_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    adx_entry = 22
    atr_mult = 2.0
    vol_window = 20
    minperiod = 8
    maxperiod = 30

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        dc_period = self.op.fillna(self.feat.dcperiod(close), 20)
        dc_smooth = self.feat.rolling_max(dc_period, 5)
        mavp_ma = self.feat.mavp(close, periods=dc_smooth, minperiod=self.minperiod, maxperiod=self.maxperiod, matype=0)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)
        trend_mode = self.feat.trendmode(close)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop_long = close < (mavp_ma - self.atr_mult * atr_val)
        atr_stop_short = close > (mavp_ma + self.atr_mult * atr_val)
        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        mavp_cross_up = self.op.crossed_above(close, mavp_ma)
        mavp_cross_dn = self.op.crossed_below(close, mavp_ma)

        long_signal = mavp_cross_up & (adx_val > self.adx_entry) & (volume > vol_sma) & (trend_mode == 1) & (return_roll > 0)
        short_signal = mavp_cross_dn & (adx_val > self.adx_entry) & (volume > vol_sma) & (trend_mode == 1) & (return_roll < 0)

        adx_fade = self.op.crossed_below_value(adx_val, 18)
        trend_exit = self.op.crossed_below_value(trend_mode, 1)
        exit_setup = self.op.hold_for(adx_fade | atr_stop_long | atr_stop_short | trailing_long | trailing_short | trend_exit, 1)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T15-mavp_C",
    "thesis":     "15",
    "descr":      "MAVP TrendMode Gate",
    "timeframes": [15, 30, 60],
    "code":       T15_MAVP_C_CODE,
    "fixed":      {"adx_entry": 22, "atr_mult": 2.0, "vol_window": 20, "minperiod": 8, "maxperiod": 30},
    "params":     {},
})

# ============================================================
# THESIS 16: Price-Volume Velocity Divergence
# ============================================================

T16_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    atr_mult = 2.0
    vol_window = 20
    adx_entry = 15

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=14)
        atr_val = self.feat.atr(high, low, close, timeperiod=14)

        volume_z = self.feat.rolling_zscore(volume, window=self.vol_window)

        atr_stop_long = close < (bb_mid - self.atr_mult * atr_val)
        atr_stop_short = close > (bb_mid + self.atr_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        vol_push = (volume_z > 0.5) & (close > bb_mid) & (adx_val > self.adx_entry)
        price_fade = (volume_z < 0.0) & (close > bb_upper) & (adx_val > self.adx_entry)

        long_signal = vol_push
        short_signal = price_fade

        exit_long = atr_stop_long | trailing_long | (close < bb_mid)
        exit_short = atr_stop_short | trailing_short | (close > bb_mid)

        exit_action = (exit_long & (long_signal == 0)) | (exit_short & (short_signal == 0))

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_action, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T16-A",
    "thesis":     "16",
    "descr":      "Velocity Divergence",
    "timeframes": [15, 30, 60],
    "code":       T16_A_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "atr_mult": 2.0, "vol_window": 20, "adx_entry": 15},
    "params":     {},
})

# ============================================================
# THESIS 17: Volatility-Adjusted Momentum
# ============================================================

T17_A_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    adj_window = 14
    z_window = 20
    z_entry = 1.5
    atr_mult = 2.0
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adj_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.adj_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        roc_val = self.feat.roc(close, timeperiod=self.adj_window)
        adj_mom = roc_val / atr_val
        adj_mom_z = self.feat.rolling_zscore(adj_mom, window=self.z_window)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop = atr_val * self.atr_mult
        atr_stop_long = close < (bb_mid - atr_stop)
        atr_stop_short = close > (bb_mid + atr_stop)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (adj_mom_z > self.z_entry) & (close > bb_mid) & (volume > vol_sma) & (return_roll > 0)
        short_signal = (adj_mom_z < -self.z_entry) & (close < bb_mid) & (volume > vol_sma) & (return_roll < 0)

        exit_setup = (adx_val < 18) | atr_stop_long | atr_stop_short | trailing_long | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T17-A",
    "thesis":     "17",
    "descr":      "Vol-Adj Momentum Breakout",
    "timeframes": [15, 30, 60],
    "code":       T17_A_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "adj_window": 14, "z_window": 20, "z_entry": 1.5, "atr_mult": 2.0, "vol_window": 20},
    "params":     {},
})

T17_B_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    adj_window = 14
    z_window = 20
    z_entry = 1.5
    atr_mult = 2.0
    vol_window = 20
    sma_fast = 13
    sma_slow = 34

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adj_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.adj_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        roc_val = self.feat.roc(close, timeperiod=self.adj_window)
        adj_mom = roc_val / atr_val
        adj_mom_z = self.feat.rolling_zscore(adj_mom, window=self.z_window)

        sma_13 = self.feat.sma(close, timeperiod=self.sma_fast)
        sma_34 = self.feat.sma(close, timeperiod=self.sma_slow)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop = atr_val * self.atr_mult
        atr_stop_long = close < (bb_mid - atr_stop)
        atr_stop_short = close > (bb_mid + atr_stop)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (adj_mom_z > self.z_entry) & (close > bb_mid) & (volume > vol_sma) & (sma_13 > sma_34)
        short_signal = (adj_mom_z < -self.z_entry) & (close < bb_mid) & (volume > vol_sma) & (sma_13 < sma_34)

        exit_setup = (adx_val < 18) | atr_stop_long | atr_stop_short | trailing_long | trailing_short | (adj_mom_z < 0)

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T17-B",
    "thesis":     "17",
    "descr":      "Vol-Adj Momentum + SMA Filter",
    "timeframes": [15, 30, 60],
    "code":       T17_B_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "adj_window": 14, "z_window": 20, "z_entry": 1.5, "atr_mult": 2.0, "vol_window": 20, "sma_fast": 13, "sma_slow": 34},
    "params":     {},
})

T17_C_CODE = """class CustomStrategy(SimpleAlgorithm):
    bb_window = 20
    bb_nbdev = 2
    adj_window = 14
    z_window = 20
    atr_mult_low = 1.5
    atr_mult_high = 2.5
    vol_window = 20

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        bb_upper, bb_mid, bb_lower = self.feat.bbands(close, timeperiod=self.bb_window, nbdevup=self.bb_nbdev, nbdevdn=self.bb_nbdev)

        adx_val = self.feat.adx(high, low, close, timeperiod=self.adj_window)
        atr_val = self.feat.atr(high, low, close, timeperiod=self.adj_window)
        vol_sma = self.feat.sma(volume, timeperiod=self.vol_window)

        roc_val = self.feat.roc(close, timeperiod=self.adj_window)
        adj_mom = roc_val / atr_val
        adj_mom_z = self.feat.rolling_zscore(adj_mom, window=self.z_window)

        vol_regime = atr_val / self.feat.sma(atr_val, timeperiod=self.z_window)
        low_vol = vol_regime < 0.8

        z_entry = self.op.where(low_vol, 2.0, 1.2)
        trailing_mult = self.op.where(low_vol, self.atr_mult_low, self.atr_mult_high)

        return_1 = self.op.fillna(self.op.pct_change(close, periods=1), value=0)
        return_roll = self.feat.rolling_mean(return_1, window=5)

        atr_stop_long = close < (bb_mid - trailing_mult * atr_val)
        atr_stop_short = close > (bb_mid + trailing_mult * atr_val)

        trailing_long = close < (self.feat.rolling_max(close, 10) - atr_val)
        trailing_short = close > (self.feat.rolling_min(close, 10) + atr_val)

        long_signal = (adj_mom_z > z_entry) & (close > bb_mid) & (volume > vol_sma) & (return_roll > 0)
        short_signal = (adj_mom_z < -z_entry) & (close < bb_mid) & (volume > vol_sma) & (return_roll < 0)

        exit_setup = (adx_val < 18) | atr_stop_long | atr_stop_short | trailing_long | trailing_short

        assert not (long_signal & short_signal).any()

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_signal, position=1)
        self.set_positions(short_signal, position=-1)
"""

TEMPLATES.append({
    "name":       "T17-C",
    "thesis":     "17",
    "descr":      "Vol-Adj Momentum Regime",
    "timeframes": [15, 30, 60],
    "code":       T17_C_CODE,
    "fixed":      {"bb_window": 20, "bb_nbdev": 2, "adj_window": 14, "z_window": 20, "atr_mult_low": 1.5, "atr_mult_high": 2.5, "vol_window": 20},
    "params":     {},
})


if __name__ == "__main__":
    generate()
