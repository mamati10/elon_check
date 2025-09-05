from playwright.sync_api import sync_playwright

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

# مثال استفاده - می‌تونی اینو با نیازت تغییر بدی
if __name__ == "__main__":
    username = "Mmd_bit10"  # اسم کاربری که می‌خوای چک کنی
    result = check_display_name(username)
    print(f"نام پروفایل: {result}")
