```python
import os
import requests
import time
from telegram import Bot
from datetime import datetime

# تنظیمات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def log(message):
    """لاگ کردن پیام‌ها"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_whale_transactions():
    """دریافت تراکنش‌های بزرگ"""
    try:
        log("🔍 بررسی تراکنش‌های بیت‌کوین...")
        response = requests.get('https://mempool.space/api/mempool', timeout=10)
        mempool = response.json()
        
        large_txs = []
        for tx_id, tx_data in list(mempool.items())[:50]:
            if tx_data.get('fee', 0) > 50000:
                large_txs.append({
                    'id': tx_id,
                    'fee': tx_data['fee'],
                    'size': tx_data['size']
                })
        
        log(f"✅ {len(large_txs)} تراکنش بزرگ یافت شد")
        return large_txs[:3]
        
    except Exception as e:
        log(f"❌ خطا: {e}")
        return []

def send_alert(bot, transactions):
    """ارسال هشدار"""
    if not transactions:
        return
    
    message = "🐋 **هشدار تراکنش بزرگ بیت‌کوین** 🚨\n\n"
    for i, tx in enumerate(transactions, 1):
        message += f"**تراکنش #{i}**\n"
        message += f"💰 کارمزد: {tx['fee']:,} ساتوشی\n"
        message += f"📦 حجم: {tx['size']} بایت\n"
        message += "─────────────────\n"
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        log("📤 پیام ارسال شد")
    except Exception as e:
        log(f"❌ ارسال پیام: {e}")

def main():
    """برنامه اصلی"""
    log("🚀 ربات نهنگ‌یاب شروع به کار کرد")
    bot = Bot(token=TELEGRAM_TOKEN)
    
    while True:
        try:
            transactions = get_whale_transactions()
            if transactions:
                send_alert(bot, transactions)
            else:
                log("✅ هیچ تراکنش بزرگی یافت نشد")
            
            log("⏳ انتظار 20 دقیقه...")
            time.sleep(1200)  # 20 دقیقه
        except Exception as e:
            log(f"❌ خطای اصلی: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
```
