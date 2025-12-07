from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from bot.handlers.scalping_handler import handle_scalping
from bot.handlers.backtest_handler import handle_backtest

# -------------------------------
# Fungsi menu utama
# -------------------------------
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Scalping", callback_data="menu_scalping")],
        [InlineKeyboardButton("Backtest", callback_data="menu_backtest")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Pilih menu:", reply_markup=reply_markup)


# -------------------------------
# Fungsi callback button
# -------------------------------
def handle_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "menu_scalping":
        handle_scalping(update, context)
    elif query.data == "menu_backtest":
        handle_backtest(update, context)
    else:
        query.edit_message_text(text="Menu belum tersedia.")
