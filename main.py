import os
import requests
import time
import logging

# تنظیمات پیشرفته لاگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def debug_environment():
    """بررسی محیط اجرا"""
    logger.info("=== شروع دیباگ ===")
    logger.info(f"TELEGRAM_TOKEN exists: {'TELEGRAM_TOKEN' in os.environ}")
    logger.info(f"TELEGRAM_CHAT_ID exists: {'TELEGRAM_CHAT_ID' in os.environ}")
    
    if 'TELEGRAM_TOKEN' in os.environ:
        token = os.environ['TELEGRAM_TOKEN']
        logger.info(f"Token length: {len(token)}")
        logger.info(f"Token starts with: {token[:10]}...")
    
    if 'TELEGRAM_CHAT_ID' in os.environ:
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        logger.info(f"Chat ID: {chat_id}")

def test_telegram_bot():
    """تست ربات تلگرام"""
    try:
        from telegram import Bot
        
        token = os.environ.get('TELEGRAM_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            logger.error("❌ توکن یا چت آیدی وجود ندارد")
            return False
        
        bot = Bot(token=token)
        
        # تست اتصال
        bot_info = bot.get_me()
        logger.info(f"✅ ربات متصل شد: @{bot_info.username}")
        
        # تست ارسال پیام
        bot.send_message(
            chat_id=chat_id,
            text="🧪 تست ربات: این پیام از Koyeb ارسال شده است!",
            parse_mode='Markdown'
        )
        logger.info("✅ پیام تست ارسال شد")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطا در تست تلگرام: {e}")
        return False

def check_mempool():
    """تست اتصال به mempool.space"""
    try:
        logger.info("🌐 تست اتصال به mempool.space...")
        response = requests.get('https://mempool.space/api/mempool', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ اتصال موفق - {len(data)} تراکنش در ممپول")
            return True
        else:
            logger.error(f"❌ خطای HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ خطا در اتصال به mempool: {e}")
        return False

def main():
    """برنامه اصلی"""
    logger.info("🚀 شروع برنامه...")
    
    # دیباگ محیط
    debug_environment()
    
    # تست‌های اولیه
    telegram_ok = test_telegram_bot()
    mempool_ok = check_mempool()
    
    if telegram_ok and mempool_ok:
        logger.info("🎉 همه تست‌ها موفق! برنامه اصلی شروع می‌شود...")
        
        from telegram import Bot
        bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
        chat_id = os.environ['TELEGRAM_CHAT_ID']
        
        # برنامه اصلی
        counter = 0
        while True:
            try:
                counter += 1
                logger.info(f"🔍 چک شماره {counter}...")
                
                # اینجا کد اصلی بررسی تراکنش‌ها می‌آید
                response = requests.get('https://mempool.space/api/mempool')
                data = response.json()
                
                large_txs = []
                for tx_id, tx in list(data.items())[:30]:
                    if tx.get('fee', 0) > 50000:
                        large_txs.append(tx)
                
                if large_txs:
                    message = f"🐋 {len(large_txs)} تراکنش بزرگ\n"
                    for tx in large_txs[:2]:
                        message += f"💰 {tx['fee']:,} ساتوشی\n"
                    bot.send_message(chat_id=chat_id, text=message)
                    logger.info(f"📤 ارسال پیام برای {len(large_txs)} تراکنش")
                else:
                    logger.info("✅ هیچ تراکنش بزرگی نیست")
                
                logger.info("⏳ انتظار 20 دقیقه...")
                time.sleep(1200)  # 20 دقیقه
                
            except Exception as e:
                logger.error(f"❌ خطا در حلقه اصلی: {e}")
                time.sleep(60)
                
    else:
        logger.error("❌ تست‌ها失败 - برنامه متوقف شد")

if __name__ == "__main__":
    main()
