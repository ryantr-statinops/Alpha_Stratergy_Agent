"""Kalman Filter — 1D and 2D implementations for numpy arrays."""
import numpy as np


def kalman_1d(price, process_noise=1e-5, measure_noise=0.01):
    """Online 1D Kalman filter returning (state, state_std, residual).

    Params
    ------
    price : np.ndarray
        Close prices
    process_noise : float
        Q — how much the state can change per step (low = smooth)
    measure_noise : float
        R — how much we trust each new observation (low = trust more)

    Returns
    -------
    state : np.ndarray
        Filtered state estimate (same length as price)
    state_std : np.ndarray
        Standard deviation of the state estimate
    residual : np.ndarray
        Innovation (price - predicted_state)
    """
    n = len(price)
    state = np.full(n, np.nan)
    state_std = np.full(n, np.nan)
    residual = np.full(n, np.nan)

    if n == 0:
        return state, state_std, residual

    x = float(price[0])
    p = 1.0
    state[0] = x
    state_std[0] = np.sqrt(P)

    for i in range(1, n):
        # Predict
        x_pred = x
        p_pred = P + process_noise

        # Update
        K = p_pred / (p_pred + measure_noise)
        innov = float(price[i]) - x_pred
        x = x_pred + K * innov
        P = (1 - K) * p_pred

        state[i] = x
        state_std[i] = np.sqrt(P)
        residual[i] = innov

    return state, state_std, residual


def kalman_2d(price, hl_range, process_noise=1e-5, measure_noise_close=0.01, measure_noise_range=0.05):
    """2D Kalman filter tracking both price level and intraday range.

    State vector: [price_state, range_state]
    Measurement: [close, high - low]

    Returns
    -------
    state_price : np.ndarray
    state_range : np.ndarray
    residual : np.ndarray  (close - predicted_price)
    """
    n = len(price)
    state_price = np.full(n, np.nan)
    state_range = np.full(n, np.nan)
    residual = np.full(n, np.nan)

    if n == 0:
        return state_price, state_range, residual

    x = np.array([float(price[0]), 0.0], dtype=float)
    P = np.eye(2) * 1.0
    R = np.diag([measure_noise_close, measure_noise_range])
    Q = np.eye(2) * process_noise
    H = np.eye(2)

    state_price[0] = x[0]
    state_range[0] = x[1]

    for i in range(1, n):
        # Predict
        x_pred = x
        P_pred = P + Q

        # Update
        z = np.array([float(price[i]), float(hl_range[i])], dtype=float)
        y = z - H @ x_pred
        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T @ np.linalg.inv(S)
        x = x_pred + K @ y
        P = (np.eye(2) - K @ H) @ P_pred

        state_price[i] = x[0]
        state_range[i] = x[1]
        residual[i] = y[0]

    return state_price, state_range, residual


def kalman_proxy(price, window=10):
    """Simple proxy for Kalman filter using SMA + residual calculation.
    
    Use this when a full Kalman is not available (e.g. XNOQuant templates).
    Returns (state, residual) where state = SMA(price, window).
    """
    import talib
    state = talib.SMA(np.asarray(price), timeperiod=window)
    residual = price - state
    return state, residual