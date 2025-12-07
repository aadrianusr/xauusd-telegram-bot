import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import menu_handler, scalping_handler, backtest_handler

# --------------------------
# Logging
# --------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --------------------------
# Callback untuk menu
# --------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_handler.main_menu(update, context)

# --------------------------
# Callback untuk scalping
# --------------------------
async def handle_scalping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    timeframe = query.data  # Misal "M1", "M3", "M5"
    scalping_handler.scalping(update, context, timeframe)

# --------------------------
# Callback untuk backtest
# --------------------------
async def handle_backtest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    timeframe = query.data  # Misal "M1", "M3", "M5"
    backtest_handler.backtest(update, context, timeframe)

# --------------------------
# Jalankan bot
# --------------------------
async def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Command /start
    app.add_handler(CommandHandler("start", start))

    # CallbackQuery (menu)
    app.add_handler(CallbackQueryHandler(handle_scalping, pattern="^(M1|M3|M5)$"))
    app.add_handler(CallbackQueryHandler(handle_backtest, pattern="^(backtest)$"))

    print("Bot started...")

    await app.run_polling()
