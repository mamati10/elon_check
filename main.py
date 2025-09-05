import requests
from bs4 import BeautifulSoup

def check_display_name(username):
    url = f"https://x.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "خطا در دسترسی به صفحه: " + str(response.status_code)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # استخراج نام پروفایل (این سلکتور ممکنه تغییر کنه - بررسی کن)
    name_tag = soup.find('div', {'data-testid': 'User-Name'})
    if name_tag:
        display_name = name_tag.find('span').text.strip()
        return display_name
    else:
        return "نام پروفایل پیدا نشد (ممکنه صفحه تغییر کرده باشه)"

# مثال استفاده
print(check_display_name("Mmd_bit10"))  # جایگزین با نام کاربری مورد نظر
