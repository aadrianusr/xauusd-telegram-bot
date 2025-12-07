import pandas as pd
import numpy as np


# -----------------------------
# EMA
# -----------------------------
def EMA(series, period):
    return series.ewm(span=period, adjust=False).mean()


# -----------------------------
# RSI
# -----------------------------
def RSI(series, period=14):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# -----------------------------
# Bollinger Bands
# -----------------------------
def BollingerBands(series, period=20, std_dev=2):
    ma = series.rolling(period).mean()
    std = series.rolling(period).std()

    upper = ma + (std_dev * std)
    lower = ma - (std_dev * std)

    return upper, ma, lower


# -----------------------------
# MACD
# -----------------------------
def MACD(series, fast=12, slow=26, signal=9):
    ema_fast = EMA(series, fast)
    ema_slow = EMA(series, slow)
    macd = ema_fast - ema_slow
    signal_line = EMA(macd, signal)
    histogram = macd - signal_line
    return macd, signal_line, histogram


# -----------------------------
# Stochastic
# -----------------------------
def Stochastic(high, low, close, period=14, smooth_k=3, smooth_d=3):
    lowest_low = low.rolling(period).min()
    highest_high = high.rolling(period).max()

    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    k_smooth = k.rolling(smooth_k).mean()
    d = k_smooth.rolling(smooth_d).mean()

    return k_smooth, d


# -----------------------------
# ATR (Average True Range)
# -----------------------------
def ATR(high, low, close, period=14):
    hl = high - low
    hc = (high - close.shift()).abs()
    lc = (low - close.shift()).abs()

    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    atr = tr.rolling(period).mean()
    return atr


# -----------------------------
# Volume spike
# -----------------------------
def volume_spike(volume, threshold=1.12):
    # true jika volume sekarang >= 12% lebih tinggi dari sebelumnya
    if len(volume) < 2:
        return False
    return volume.iloc[-1] >= volume.iloc[-2] * threshold
