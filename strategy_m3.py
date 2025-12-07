import pandas as pd

from bot.core.indicators import EMA, MACD, Stochastic, ATR


class StrategyM3:

    def __init__(self):
        self.name = "Scalping M3"

    # -----------------------------------------------------------
    # Fungsi utama → menerima dataframe → mengembalikan sinyal
    # -----------------------------------------------------------
    def generate_signal(self, df: pd.DataFrame):
        """
        df harus punya kolom:
        ['time', 'open', 'high', 'low', 'close', 'volume']
        """

        # Hitung indikator
        df["ema20"] = EMA(df["close"], 20)
        df["ema50"] = EMA(df["close"], 50)

        macd_line, signal_line, macd_hist = MACD(df["close"])
        df["macd_hist"] = macd_hist

        df["stoch_k"], df["stoch_d"] = Stochastic(df["high"], df["low"], df["close"])

        df["atr"] = ATR(df["high"], df["low"], df["close"])

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # ----------------------------
        # RULE BUY
        # ----------------------------
        buy_conditions = [
            last["ema20"] > last["ema50"],                # EMA20 > EMA50
            last["macd_hist"] > 0,                        # MACD histogram positif
            prev["stoch_k"] < prev["stoch_d"] and last["stoch_k"] > last["stoch_d"],  # crossover naik
            20 <= last["stoch_k"] <= 50,                  # area 20–50
            last["close"] > last["ema20"],                # candle close di atas EMA20
            last["atr"] > df["atr"].mean() * 0.5          # ATR di atas threshold sederhana
        ]

        # ----------------------------
        # RULE SELL
        # ----------------------------
        sell_conditions = [
            last["ema20"] < last["ema50"],
            last["macd_hist"] < 0,
            prev["stoch_k"] > prev["stoch_d"] and last["stoch_k"] < last["stoch_d"],
            20 <= last["stoch_k"] <= 50,
            last["close"] < last["ema20"],
            last["atr"] > df["atr"].mean() * 0.5
        ]

        # ----------------------------
        # HASILKAN SINYAL
        # ----------------------------
        if all(buy_conditions):
            return {
                "signal": "BUY",
                "reason": [
                    "EMA20 > EMA50",
                    "MACD histogram positif",
                    "Stochastic crossover naik",
                    "Stoch di area 20–50",
                    "Candle close di atas EMA20",
                    "ATR di atas threshold"
                ]
            }

        if all(sell_conditions):
            return {
                "signal": "SELL",
                "reason": [
                    "EMA20 < EMA50",
                    "MACD histogram negatif",
                    "Stochastic crossover turun",
                    "Stoch di area 20–50",
                    "Candle close di bawah EMA20",
                    "ATR di atas threshold"
                ]
            }

        return None   # Tidak ada sinyal
