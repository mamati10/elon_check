from keep_alive import keep_alive
from playwright.sync_api import sync_playwright
import telebot
import time

# فعال‌سازی سرور در Render
keep_alive()

# ---------- پیکربندی ----------
USERNAME = "Mmd_bit10"   # نام کاربری که می‌خوای بررسی کنی
BOT_TOKEN = "8192088890:AAG9cR7Z4FbX0c1qV8aCUNkUo6jQEFpljRQ"
CHAT_ID = "804261647"

# ---------- راه‌اندازی ربات ----------
bot = telebot.TeleBot(BOT_TOKEN)

# ---------- ذخیره وضعیت قبلی ----------
last_name = None
last_profile_image_url = None

def get_user_data(username):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                extra_http_headers={
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://x.com"
                }
            )
            page.goto(f"https://x.com/{username}", timeout=60000)
            page.wait_for_selector('[data-testid="User-Name"]', state="visible", timeout=30000)
            display_name = page.query_selector('[data-testid="User-Name"] span').inner_text().strip()
            profile_image = page.query_selector('div.css-1dbjc4n img')
            profile_image_url = profile_image.get_attribute('src') if profile_image else "عکس پیدا نشد"
            browser.close()
            return {
                "name": display_name,
                "profile_image_url": profile_image_url
            }
    except Exception as e:
        print(f"❌ خطا در گرفتن اطلاعات: {e}")
        bot.send_message(CHAT_ID, f"❌ جزئیات خطا: {str(e)}")
        return None

def check_changes():
    global last_name, last_profile_image_url

    user_data = get_user_data(USERNAME)
    if user_data is None:
        bot.send_message(CHAT_ID, "❌ خطا در دریافت اطلاعات کاربر.")
        return

    current_name = user_data["name"]
    current_profile_image_url = user_data["profile_image_url"]

    if last_name is None:
        last_name = current_name
        last_profile_image_url = current_profile_image_url
        print(f"🔎 اولین مقدار ذخیره شد: {current_name}")
        return

    if current_name != last_name:
        msg = f"⚡️ نام تغییر کرد!\nقبلی: {last_name}\nجدید: {current_name}"
        bot.send_message(CHAT_ID, msg)
        last_name = current_name

    if current_profile_image_url != last_profile_image_url:
        msg = "⚡️ عکس پروفایل تغییر کرد!"
        bot.send_message(CHAT_ID, msg)
        last_profile_image_url = current_profile_image_url

# ---------- حلقه اصلی ----------
if __name__ == "__main__":
    while True:
        try:
            print("✅ در حال بررسی تغییرات...")
            check_changes()
        except Exception as e:
            print(f"❌ خطا: {e}")
            bot.send_message(CHAT_ID, f"❌ خطا: {e}")
        time.sleep(600)  # هر ۱۰ دقیقه بررسی شود
