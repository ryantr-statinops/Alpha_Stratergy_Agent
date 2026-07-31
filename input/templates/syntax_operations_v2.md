# syntax_operations_v2 — Template cung cấp operators mới

## summary
mỗi 4 dòng là 4 nội dung của 1 operation:
ví dụ:
rank_cs_panel
Returns: PanelT
self.op.rank_cs_panel(panel: PanelT, mask: PanelT = None, method='average')
Rank eligible symbols independently at each timestamp as percentile ranks.

## list:

rank_cs_panel
Returns: PanelT
self.op.rank_cs_panel(panel: PanelT, mask: PanelT = None, method='average')
Rank eligible symbols independently at each timestamp as percentile ranks.
demean_cs_panel
Returns: PanelT
self.op.demean_cs_panel(panel: PanelT, mask: PanelT = None, winsorize=None)
Subtract the cross-sectional mean from each eligible symbol.
normalize_l1_cs_panel
Returns: PanelT
self.op.normalize_l1_cs_panel(panel: PanelT, mask: PanelT = None, eps=1e-12)
Normalize each timestamp to unit L1 exposure after masking.
winsorize_cs_panel
Returns: PanelT
self.op.winsorize_cs_panel(panel: PanelT, mask: PanelT = None, lower=0.02, upper=0.98)
Clip each date's eligible cross-section to quantile bounds.
zscore_cs_panel
Returns: PanelT
self.op.zscore_cs_panel(panel: PanelT, mask: PanelT = None, ddof=1)
Standardize each eligible cross-section with safe zero-variance handling.
portfolio_weights_panel
Returns: PanelT
self.op.portfolio_weights_panel(signal: PanelT, method='rank_demean_l1', mask: PanelT = None, rank_method='average', max_abs_weight=None)
Build neutral unit-gross portfolio weights from cross-sectional ranks.