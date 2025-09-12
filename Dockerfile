FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# این نصب کرومیوم و وابستگی‌ها رو همزمان انجام میده
RUN playwright install --with-deps


CMD ["python", "main.py"]
