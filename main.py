```python
import os
import requests
import time
from telegram import Bot

print("🚀 شروع ربات نهنگ‌یاب...")

# دریافت توکن‌ها از Secrets
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

bot = Bot(token=TOKEN)

# تست اولیه
bot.send_message(chat_id=CHAT_ID, text="✅ ربات در Replit فعال شد!")
print("پیام تست ارسال شد")

def check_whales():
    try:
        print("🔍 بررسی تراکنش‌ها...")
        response = requests.get('https://mempool.space/api/mempool')
        data = response.json()
        
        large_txs = []
        for tx_id, tx in list(data.items())[:50]:
            if tx.get('fee', 0) > 50000:  # کارمزد بالا
                large_txs.append(tx)
        
        return large_txs[:3]
    except Exception as e:
        print(f"خطا: {e}")
        return []

# برنامه اصلی
counter = 0
while True:
    try:
        counter += 1
        print(f"🔍 چک شماره {counter}")
        
        transactions = check_whales()
        if transactions:
            message = f"🐋 {len(transactions)} تراکنش بزرگ\n"
            for tx in transactions:
                message += f"💰 {tx['fee']:,} ساتوشی\n"
            bot.send_message(chat_id=CHAT_ID, text=message)
            print("پیام ارسال شد")
        else:
            print("تراکنش بزرگی نیست")
        
        print("⏳ 20 دقیقه صبر...")
        time.sleep(1200)  # 20 دقیقه
        
    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(60)
```
