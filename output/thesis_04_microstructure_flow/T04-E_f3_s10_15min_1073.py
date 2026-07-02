"""
name:    T04-E_f3_s10
summary: A/D Oscillator Divergence
idea:    Bullish/bearish divergence between price and Accumulation/Distribution Oscillator with RSI confirmation.
"""
class CustomStrategy(SimpleAlgorithm):
    adosc_fast = 3
    adosc_slow = 10
    thesis_group = "04"

    def __algorithm__(self):
        close = self.data.pv_close
        high = self.data.pv_high
        low = self.data.pv_low
        volume = self.data.pv_volume

        adosc = self.feat.adosc(high, low, close, volume, fastperiod=self.adosc_fast, slowperiod=self.adosc_slow)
        rsi = self.feat.rsi(close, timeperiod=10)
        adx_val = self.feat.adx(high, low, close, timeperiod=10)

        price_rising = close > self.op.previous(close)
        price_falling = close < self.op.previous(close)

        bullish_div = price_falling & (adosc > self.op.previous(adosc)) & (rsi < 40)
        bearish_div = price_rising & (adosc < self.op.previous(adosc)) & (rsi > 60)

        long_setup = bullish_div & (adx_val > 22)
        short_setup = bearish_div & (adx_val > 22)
        exit_setup = self.op.crossed_below(close, self.feat.sma(close, 14)) | self.op.crossed_above(close, self.feat.sma(close, 14)) | (adx_val < 15)

        self.set_positions(exit_setup, position=0)
        self.set_positions(long_setup, position=1)
        self.set_positions(short_setup, position=-1)

