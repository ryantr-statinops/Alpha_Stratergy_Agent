"""
name:    VnSmallCsMomentumOnlyProbe
summary: Purely diagnostic probe. Weights small caps by squared price momentum
         (close/ema)^2 alone, with only positivity and liquidity-style gates.
         If its metrics equal the value-momentum composite, the squared
         momentum term dominates the book and the fundamental layers are
         decorative. Diagnostic only; not a standalone trading thesis.
idea:    Diagnostic only. Isolates the trend_ratio squared term that drives the
         composite. No fundamental multiplier, so any equality with the
         composite reveals that momentum alone reproduces the book.
"""


class CustomStrategy(SimpleAlgorithm):
    def __algorithm__(self):
        close = self.data.pv_close_panel
        volume = self.data.pv_volume_panel

        trend_ratio = self.feat.safe_divide_panel(close, self.feat.ema_panel(close))
        eligible = (close > 0) & (volume > 0)

        signal = trend_ratio * trend_ratio

        weights = self.op.portfolio_weights_panel(signal, method='demean_l1', mask=eligible)
        self.set_portfolio_positions(weights)
