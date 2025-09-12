FROM python:3.11-slim

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libgbm1 libasound2 libpangocairo-1.0-0 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxrender1 libcairo2 libdbus-1-3 libexpat1 libfontconfig1 libfreetype6 libglib2.0-0 libpango-1.0-0 libpixman-1-0 libpng16-16 libstdc++6 zlib1g libgtk-4-1 libgraphene-1.0-0 libgstgl-1.0-0 libgstcodecparsers-1.0-0 libenchant-2-2 libsecret-1-0 libmanette-0.2-0 libgles2 \
    && rm -rf /var/lib/apt/lists/*

# تنظیم محیط
WORKDIR /app
COPY . /app

# نصب پکیج‌های پایتون
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# اجرای برنامه
CMD ["python", "main.py"]
