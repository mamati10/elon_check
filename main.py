import snscrape.modules.twitter as sntwitter
import telebot
import time
from keep_alive import keep_alive

# فعال‌سازی سرور در Render
keep_alive()

# ---------- پیکربندی ----------
USERNAME = "Mmd_bit10"   # نام کاربری که می‌خوای بررسی کنی
BOT_TOKEN = "8192088890:AAG9cR7Z4FbX0c1qV8aCUNkUo6jQEFpljRQ"  # توکن ربات تلگرام
CHAT_ID = "804261647"    # آیدی چت تلگرام

# ---------- راه‌اندازی ربات ----------
bot = telebot.TeleBot(BOT_TOKEN)

# ---------- ذخیره وضعیت قبلی ----------
last_name = None
last_profile_image_url = None

def get_user_data(username):
    try:
        user = next(sntwitter.TwitterUserScraper(username).get_items())
        return {
            "name": user.user.displayname,
            "profile_image_url": user.user.profileImageUrl
        }
    except StopIteration:
        print("❌ کاربر پیدا نشد.")
        return None
    except Exception as e:
        print(f"❌ خطا در گرفتن اطلاعات: {e}")
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
        time.sleep(600)  # هر ۱ دقیقه بررسی شود
