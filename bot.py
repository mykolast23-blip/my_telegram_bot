import os
import logging
import time

logging.basicConfig(level=logging.DEBUG)

def debug_all_tokens():
    """Шукаємо токен у всіх можливих змінних"""
    
    possible_names = [
        'BOT_TOKEN',
        'TELEGRAM_TOKEN', 
        'TELEGRAM_BOT_TOKEN',
        'BOT_API_TOKEN',
        'TOKEN',
        'TELEGRAM_API_TOKEN'
    ]
    
    logging.info("🎯 ПОШУК ТОКЕНУ В УСІХ МОЖЛИВИХ ЗМІННИХ:")
    
    found_token = None
    for name in possible_names:
        value = os.environ.get(name)
        if value:
            logging.info(f"✅ ЗНАЙДЕНО: {name} = {value[:10]}...{value[-10:]}")
            found_token = value
            break
        else:
            logging.info(f"❌ НЕ ЗНАЙДЕНО: {name}")
    
    return found_token

def main():
    logging.info("🚀 Запуск пошуку токену...")
    time.sleep(2)
    
    # Шукаємо токен у всіх можливих змінних
    bot_token = debug_all_tokens()
    
    if bot_token:
        logging.info(f"🎉 ТОКЕН ЗНАЙДЕНО! Довжина: {len(bot_token)} символів")
        
        # Тестуємо бота
        try:
            from telegram.ext import Application
            app = Application.builder().token(bot_token).build()
            logging.info("🟢 Бот успішно ініціалізований!")
            
            from telegram import Update
            from telegram.ext import ContextTypes, CommandHandler
            
            async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
                await update.message.reply_text("🎉 Бот працює! Змінні середовища знайдено!")
            
            app.add_handler(CommandHandler("start", start))
            logging.info("🟢 Бот готовий до роботи!")
            app.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logging.error(f"❌ Помилка бота: {e}")
    else:
        logging.error("💥 ТОКЕН НЕ ЗНАЙДЕНО В ЖОДНІЙ ЗМІННІЙ!")
        logging.error("🔧 ПЕРЕВІРТЕ:")
        logging.error("   1. Чи додали ви змінну в Railway → Variables")
        logging.error("   2. Чи правильно введено назву та значення")
        logging.error("   3. Чи зробили Redeploy після додавання")

if __name__ == '__main__':
    main()