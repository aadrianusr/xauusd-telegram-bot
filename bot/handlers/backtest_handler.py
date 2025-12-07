import pandas as pd
from telegram import Update
from telegram.ext import CallbackContext

from bot.core.data_feed import DataFeed
from bot.core.strategy_m1 import StrategyM1
from bot.core.strategy_m3 import StrategyM3
from bot.core.strategy_m5 import StrategyM5

data_feed = DataFeed()
strategies = {
    "M1": StrategyM1(),
    "M3": StrategyM3(),
    "M5": StrategyM5()
}

def backtest(update: Update, context: CallbackContext, timeframe="M1"):
    # Ambil data historis
    raw_data = data_feed.get_price(timeframe)
    if not raw_data:
        update.message.reply_text("❌ Gagal ambil data historis.")
        return

    try:
        candles = raw_data.get("candles")  # sesuaikan OANDA / FOREX.com
        df = pd.DataFrame(candles)
    except:
        update.message.reply_text("❌ Data historis tidak valid.")
        return

    strategy = strategies.get(timeframe)
    if not strategy:
        update.message.reply_text(f"❌ Strategy {timeframe} tidak ditemukan.")
        return

    signals = []
    for i in range(1, len(df)):
        subset = df.iloc[:i+1]
        signal = strategy.generate_signal(subset)
        if signal:
            signals.append(signal["signal"])

    total = len(signals)
    buy = signals.count("BUY")
    sell = signals.count("SELL")

    msg = f"📊 Backtest {timeframe}\nTotal sinyal: {total}\nBUY: {buy}\nSELL: {sell}"
    update.message.reply_text(msg)

    # Export ke CSV
    df.to_csv(f"backtest_{timeframe}.csv", index=False)
    update.message.reply_text(f"✅ Hasil backtest disimpan: backtest_{timeframe}.csv")
