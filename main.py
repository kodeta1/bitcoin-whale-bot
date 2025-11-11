```python
import os
import requests
import time
from telegram import Bot
from datetime import datetime

# تنظیمات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_whale_transactions():
    """دریافت تراکنش‌های بزرگ از mempool.space"""
    try:
        print(f"{datetime.now()} - 🔍 در حال بررسی تراکنش‌های بیت‌کوین...")
        response = requests.get('https://mempool.space/api/mempool', timeout=10)
        mempool = response.json()
        
        large_txs = []
        for tx_id, tx_data in list(mempool.items())[:30]:  # بررسی 30 تراکنش اول
            if tx_data.get('fee', 0) > 50000:  # فیلتر کارمزد بالا
                large_txs.append({
                    'id': tx_id,
                    'fee': tx_data['fee'],
                    'size': tx_data['size']
                })
        
        print(f"✅ {len(large_txs)} تراکنش بزرگ یافت شد")
        return large_txs[:3]  # فقط ۳ تراکنش بزرگ
        
    except Exception as e:
        print(f"❌ خطا در دریافت داده: {e}")
        return []

def send_alert(bot, transactions):
    """ارسال هشدار به تلگرام"""
    if not transactions:
        return
    
    message = "🐋 **هشدار تراکنش بزرگ بیت‌کوین** 🚨\n\n"
    for i, tx in enumerate(transactions, 1):
        message += f"**تراکنش #{i}**\n"
        message += f"💰 کارمزد: {tx['fee']:,} ساتوشی\n"
        message += f"📦 حجم: {tx['size']} بایت\n"
        message += f"🆔 شناسه: {tx['id'][:15]}...\n"
        message += "─────────────────\n"
    
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        print("📤 پیام با موفقیت ارسال شد")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")

def main():
    """برنامه اصلی"""
    print("🚀 ربات نهنگ‌یاب بیت‌کوین شروع به کار کرد")
    
    # ایجاد ربات
    bot = Bot(token=TELEGRAM_TOKEN)
    
    while True:
        try:
            # بررسی تراکنش‌ها
            transactions = get_whale_transactions()
            
            # ارسال هشدار اگر تراکنش بزرگی وجود دارد
            if transactions:
                send_alert(bot, transactions)
            else:
                print("✅ هیچ تراکنش بزرگی یافت نشد")
            
            # انتظار ۲۰ دقیقه (1200 ثانیه)
            print("⏳ منتظر ۲۰ دقیقه...")
            time.sleep(1200)
            
        except Exception as e:
            print(f"❌ خطا در برنامه اصلی: {e}")
            print("⏳ تلاش مجدد در ۶۰ ثانیه...")
            time.sleep(60)

if __name__ == "__main__":
    main()
... 
