from keep_alive import keep_alive
from playwright.sync_api import sync_playwright
import time

# فعال نگه داشتن سرویس با Flask
keep_alive()

def check_display_name(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(f"https://x.com/{username}", timeout=60000)
            page.wait_for_selector('[data-testid="User-Name"]', timeout=30000)
            display_name = page.query_selector('[data-testid="User-Name"] span').inner_text().strip()
            browser.close()
            return display_name
        except Exception as e:
            browser.close()
            return f"خطا: {str(e)}"

# مثال استفاده - می‌تونی این بخش رو با نیازت تغییر بدی
if __name__ == "__main__":
    usernames = ["Mmd_bit10", "example_user"]  # لیست اسم‌های کاربری که می‌خوای چک کنی
    for username in usernames:
        result = check_display_name(username)
        print(f"نام پروفایل برای {username}: {result}")
        time.sleep(5)  # تأخیر 5 ثانیه برای جلوگیری از بلاک شدن
