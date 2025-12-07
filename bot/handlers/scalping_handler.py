import pandas as pd
from telegram import Update
from telegram.ext import CallbackContext

from bot.core.data_feed import DataFeed
from bot.core.strategy_m1 import StrategyM1
from bot.core.strategy_m3 import StrategyM3
from bot.core.strategy_m5 import StrategyM5


def scalping_signal(update: Update, context: CallbackContext, timeframe="M1"):
    df = pd.DataFrame(DataFeed().get_price(timeframe=timeframe)['candles'])

    # Convert data sesuai format dataframe
    df = df.rename(columns={
        'time': 'time',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume'
    })

    strategy_map = {
        "M1": StrategyM1(),
        "M3": StrategyM3(),
        "M5": StrategyM5()
    }

    strategy = strategy_map.get(timeframe)
    signal_data = strategy.generate_signal(df)

    if signal_data:
        msg = f"PAIR: XAUUSD\nTIMEFRAME: {timeframe}\nSIGNAL: {signal_data['signal']}\nREASON:\n"
        for reason in signal_data['reason']:
            msg += f"- {reason}\n"
    else:
        msg = f"PAIR: XAUUSD\nTIMEFRAME: {timeframe}\nSIGNAL: NONE"

    update.message.reply_text(msg)
