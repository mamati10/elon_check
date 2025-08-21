import requests
import telebot
import time

from keep_alive import keep_alive

keep_alive()  # فعال‌سازی سرور


# ---------- پیکربندی ----------
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAK1WzwEAAAAAKvDTSt6tOY0XIdRgEdPqYUEhX%2Fo%3DgHoGVXhsIiaE3W8pREpEHRS0IOArjf19idjz062BTuXq0DNFJw"
USERNAME = "Mmd_bit10"  # نام کاربری که می‌خوای بررسی کنی
BOT_TOKEN = "8192088890:AAG9cR7Z4FbX0c1qV8aCUNkUo6jQEFpljRQ"
CHAT_ID = "804261647"

# ---------- راه‌اندازی ربات ----------
bot = telebot.TeleBot(BOT_TOKEN)

# ---------- ذخیره وضعیت قبلی ----------
last_name = None
last_profile_image_url = None


def get_user_data(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=name,profile_image_url"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)  # تایم‌اوت 10 ثانیه
        if response.status_code == 200:
            return response.json()["data"]
        elif response.status_code == 429:  # محدودیت نرخ
            print("⚠️ Rate Limit، صبر 15 دقیقه...")
            time.sleep(900)  # 15 دقیقه صبر
            return None
        else:
            print(f"❌ خطا: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ خطای شبکه: {e}")
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
        print("🔎 اولین مقدار ذخیره شد.")
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
while True:
    try:
        print("✅ در حال بررسی تغییرات...")
        check_changes()
    except Exception as e:
        print("❌ خطا:", e)
        bot.send_message(CHAT_ID, f"❌ خطا: {e}")
    time.sleep(300) # هر ۶۰ ثانیه یکبار بررسی شود
    
