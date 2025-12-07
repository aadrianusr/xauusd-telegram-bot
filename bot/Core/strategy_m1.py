import pandas as pd

from bot.core.indicators import EMA, RSI, BollingerBands, volume_spike


class StrategyM1:

    def __init__(self):
        self.name = "Scalping M1"

    # -----------------------------------------------------------
    # Fungsi utama → menerima dataframe → return sinyal
    # -----------------------------------------------------------
    def generate_signal(self, df: pd.DataFrame):
        """
        df harus punya kolom:
        ['time', 'open', 'high', 'low', 'close', 'volume']
        """

        # Hitung indikator
        df["ema9"] = EMA(df["close"], 9)
        df["ema21"] = EMA(df["close"], 21)

        df["rsi5"] = RSI(df["close"], 5)

        df["bb_upper"], df["bb_mid"], df["bb_lower"] = BollingerBands(df["close"], 20, 2)

        # Ambil bar terbaru (candle terakhir)
        last = df.iloc[-1]
        prev = df.iloc[-2]

        # ----------------------------
        # RULE BUY (sesuai permintaanmu)
        # ----------------------------
        buy_conditions = [
            last["ema9"] > last["ema21"],                     # EMA9 cross up EMA21
            last["rsi5"] > 55,                                # RSI > 55
            prev["close"] < prev["bb_lower"] and last["close"] > last["bb_mid"],   # reject BB lower
            volume_spike(df["volume"])                        # volume spike 12%
        ]

        # ----------------------------
        # RULE SELL (kebalikan BUY)
        # ----------------------------
        sell_conditions = [
            last["ema9"] < last["ema21"],
            last["rsi5"] < 45,
            prev["close"] > prev["bb_upper"] and last["close"] < last["bb_mid"],
            volume_spike(df["volume"])
        ]

        # ----------------------------
        # HASILKAN SINYAL
        # ----------------------------
        if all(buy_conditions):
            return {
                "signal": "BUY",
                "reason": [
                    "EMA9 cross up EMA21",
                    "RSI5 > 55",
                    "Candle reject BB lower",
                    "Volume spike >= 12%"
                ]
            }

        if all(sell_conditions):
            return {
                "signal": "SELL",
                "reason": [
                    "EMA9 cross down EMA21",
                    "RSI5 < 45",
                    "Candle reject BB upper",
                    "Volume spike >= 12%"
                ]
            }

        return None  # Tidak ada sinyal
