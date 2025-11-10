import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Отримуємо токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не знайдено!")
else:
    logging.info(f"✅ Токен знайдено! Довжина: {len(BOT_TOKEN)} символів")

# Створюємо клавіатуру
keyboard = [
    ["📊 Статистика", "ℹ️ Інформація"],
    ["🔔 Сповіщення", "⚙️ Налаштування"],
    ["🆘 Допомога"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Вітаю, {user.first_name}!\n\n"
        "Я ваш Telegram бот з розширеними функціями!\n"
        "Скористайтесь кнопками або командами знизу:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **Доступні команди:**

/start - Початок роботи
/help - Ця довідка  
/info - Інформація про бота
/stats - Статистика

🎛 **Клавіатура:**
📊 Статистика - покаже статистику
ℹ️ Інформація - інфо про бота
🔔 Сповіщення - налаштування сповіщень
⚙️ Налаштування - налаштування бота
🆘 Допомога - швидка довідка
    """
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
🤖 **Інформація про бота**

**Хостинг:** Replit.com + GitHub
**Мова:** Python
**Бібліотека:** python-telegram-bot
**Версія:** 2.0 з клавіатурою
**Статус:** Активний ✅

Бот успішно працює та готовий до розширення!
Код зберігається на GitHub 🚀
    """
    await update.message.reply_text(info_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats_text = """
📈 **Статистика бота**

**Користувачі:** 1
**Повідомлень:** 0
**Активність:** Висока
**Аптайм:** Тільки запущений

Статистика буде збиратись з часом!
    """
    await update.message.reply_text(stats_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    if text == "📊 Статистика":
        await stats_command(update, context)
    elif text == "ℹ️ Інформація":
        await info_command(update, context)
    elif text == "🔔 Сповіщення":
        await update.message.reply_text("🔔 Розділ сповіщень у розробці...")
    elif text == "⚙️ Налаштування":
        await update.message.reply_text("⚙️ Налаштування будуть доступні найближчим часом!")
    elif text == "🆘 Допомога":
        await help_command(update, context)
    else:
        await update.message.reply_text("Не розпізнав команду 🤔")

async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    
    # Якщо це не команда з клавіатури
    if text not in [btn for row in keyboard for btn in row]:
        await update.message.reply_text(
            f"💬 {user.first_name}, ви написали:\n`{text}`\n\n"
            f"Використовуйте кнопки або команду /help",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Помилка: {context.error}")

def main():
    if not BOT_TOKEN:
        logging.error("❌ Не можу запустити бота без BOT_TOKEN")
        return
    
    try:
        # Створюємо бота
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Додаємо обробники команд
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("info", info_command))
        app.add_handler(CommandHandler("stats", stats_command))
        
        # Обробник кнопок клавіатури
        app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'[📊ℹ️🔔⚙️🆘]'), button_handler))
        
        # Обробник звичайних повідомлень
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))
        
        # Обробник помилок
        app.add_error_handler(error_handler)
        
        logging.info("🟢 Бот запускається...")
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logging.error(f"❌ Помилка запуску: {e}")

if __name__ == '__main__':
    main()
