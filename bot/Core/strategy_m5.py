import pandas as pd
from bot.core.indicators import EMA, RSI


class StrategyM5:

    def __init__(self):
        self.name = "Scalping M5"

    # -----------------------------------------------------------
    # Struktur Pasar (HH/HL)
    # -----------------------------------------------------------
    def detect_market_structure(self, df):
        """
        Deteksi HL sederhana:
        close[-3] > close[-4] dan close[-1] > close[-3]
        """
        try:
            return (
                df["close"].iloc[-3] > df["close"].iloc[-4]
                and df["close"].iloc[-1] > df["close"].iloc[-3]
            )
        except:
            return False

    # -----------------------------------------------------------
    # Minor breakout sederhana
    # -----------------------------------------------------------
    def breakout_minor_resistance(self, df):
        """
        Breakout: close terakhir > high dari 5 candle sebelumnya
        """
        last_close = df["close"].iloc[-1]
        prev_high = df["high"].iloc[-6:-1].max()

        return last_close > prev_high

    # -----------------------------------------------------------
    # Fungsi utama → mengembalikan sinyal
    # -----------------------------------------------------------
    def generate_signal(self, df: pd.DataFrame):

        df["ema50"] = EMA(df["close"], 50)
        df["ema200"] = EMA(df["close"], 200)

        df["rsi14"] = RSI(df["close"], 14)

        last = df.iloc[-1]

        # ----------------------------
        # RULE BUY
        # ----------------------------
        buy_conditions = [
            last["ema50"] > last["ema200"],                   # Trend up
            50 <= last["rsi14"] <= 70,                        # RSI 50–70
            self.detect_market_structure(df),                 # HL valid
            self.breakout_minor_resistance(df),               # Breakout kecil
        ]

        # ----------------------------
        # RULE SELL
        # ----------------------------
        sell_conditions = [
            last["ema50"] < last["ema200"],                   # Trend down
            30 <= last["rsi14"] <= 50,                        # RSI 30–50
            not self.detect_market_structure(df),             # Struktur turun
            last["close"] < df["low"].iloc[-6:-1].min()       # Breakout support minor
        ]

        # ----------------------------
        # HASILKAN SINYAL
        # ----------------------------
        if all(buy_conditions):
            return {
                "signal": "BUY",
                "reason": [
                    "EMA50 > EMA200 (trend naik)",
                    "RSI14 dalam area 50–70",
                    "Struktur HL valid",
                    "Breakout resistance minor"
                ]
            }

        if all(sell_conditions):
            return {
                "signal": "SELL",
                "reason": [
                    "EMA50 < EMA200 (trend turun)",
                    "RSI14 dalam area 30–50",
                    "Struktur pasar lemah",
                    "Breakout support minor"
                ]
            }

        return None
