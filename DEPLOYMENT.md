# 🚀 دليل التنصيب المتقدم - Seno Music Bot

## المطور: سينو (Seno) - [@idseno](https://t.me/idseno)

---

## 📋 جدول المحتويات

1. [التنصيب على VPS](#vps-deployment)
2. [التنصيب على Heroku](#heroku-deployment)
3. [التنصيب على Railway](#railway-deployment)
4. [التنصيب على Render](#render-deployment)
5. [التنصيب باستخدام Docker](#docker-deployment)
6. [التنصيب على الكمبيوتر المحلي](#local-deployment)

---

## 🖥️ VPS Deployment

### متطلبات VPS
- نظام: Ubuntu 20.04+ / Debian 11+
- RAM: 512 MB على الأقل
- المعالج: 1 Core
- التخزين: 2 GB
- النطاق الترددي: غير محدود

### خطوات التنصيب

#### 1. الاتصال بالـ VPS

```bash
ssh root@your-vps-ip
```

#### 2. تحديث النظام

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

#### 3. تثبيت المتطلبات الأساسية

```bash
# Python و Git
sudo apt-get install python3 python3-pip git ffmpeg -y

# تحديث pip
pip3 install --upgrade pip
```

#### 4. استنساخ المشروع

```bash
cd /home
git clone https://github.com/YOUR-USERNAME/seno-music-bot.git
cd seno-music-bot
```

#### 5. تثبيت المكتبات

```bash
pip3 install -r requirements.txt
```

#### 6. إعداد المتغيرات

```bash
# نسخ ملف المثال
cp .env.example .env

# تعديل الملف
nano .env
```

#### 7. توليد String Session

```bash
python3 generate_session.py
```

#### 8. التشغيل بـ Screen

```bash
# تثبيت screen
sudo apt-get install screen -y

# إنشاء جلسة
screen -S seno-music

# تشغيل البوت
python3 main.py

# للخروج: Ctrl+A ثم D
# للعودة: screen -r seno-music
```

#### 9. التشغيل بـ PM2 (موصى به)

```bash
# تثبيت Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# تثبيت PM2
sudo npm install pm2 -g

# تشغيل البوت
pm2 start main.py --name seno-music --interpreter python3

# أوامر PM2 المفيدة:
pm2 list                # عرض البوتات
pm2 stop seno-music     # إيقاف
pm2 restart seno-music  # إعادة تشغيل
pm2 logs seno-music     # عرض اللوجات
pm2 monit              # مراقبة حية

# التشغيل التلقائي عند إعادة التشغيل
pm2 startup
pm2 save
```

#### 10. تحديث البوت

```bash
cd /home/seno-music-bot
git pull
pip3 install -r requirements.txt --upgrade
pm2 restart seno-music
```

---

## ☁️ Heroku Deployment

### التنصيب بضغطة واحدة

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### التنصيب اليدوي

#### 1. تثبيت Heroku CLI

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. تسجيل الدخول

```bash
heroku login
```

#### 3. إنشاء التطبيق

```bash
cd seno-music-bot
heroku create your-bot-name
```

#### 4. إضافة Buildpacks

```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
```

#### 5. إعداد المتغيرات

```bash
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set STRING_SESSION=your_string_session
heroku config:set OWNER_ID=your_user_id
heroku config:set CHANNEL_USERNAME=@senovip
# ... باقي المتغيرات
```

#### 6. رفع البوت

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

#### 7. تفعيل الـ Worker

```bash
heroku ps:scale worker=1
```

#### 8. عرض اللوجات

```bash
heroku logs --tail
```

---

## 🚂 Railway Deployment

### 1. إنشاء حساب

زر [Railway.app](https://railway.app) وسجل حساب

### 2. إنشاء مشروع جديد

- اضغط "New Project"
- اختر "Deploy from GitHub repo"
- اختر repository البوت

### 3. إضافة المتغيرات

في Variables، أضف:
- `API_ID`
- `API_HASH`
- `BOT_TOKEN`
- `STRING_SESSION`
- `OWNER_ID`
- ... إلخ

### 4. التنصيب

Railway سيبدأ التنصيب تلقائياً

---

## 🎨 Render Deployment

### 1. إنشاء حساب

زر [Render.com](https://render.com) وسجل حساب

### 2. إنشاء Web Service

- اضغط "New +"
- اختر "Background Worker"
- اربط GitHub repo

### 3. الإعدادات

```yaml
Build Command: pip install -r requirements.txt
Start Command: python3 main.py
```

### 4. المتغيرات

أضف جميع المتغيرات من `.env`

---

## 🐳 Docker Deployment

### 1. إنشاء Dockerfile

```dockerfile
FROM python:3.11-slim

# تثبيت FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# تشغيل البوت
CMD ["python3", "main.py"]
```

### 2. بناء الـ Image

```bash
docker build -t seno-music-bot .
```

### 3. تشغيل الـ Container

```bash
docker run -d \
  --name seno-music \
  --env-file .env \
  seno-music-bot
```

### 4. Docker Compose

إنشاء `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: seno-music-bot
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./downloads:/app/downloads
```

تشغيل:

```bash
docker-compose up -d
```

---

## 💻 Local Deployment (Windows)

### 1. تثبيت Python

حمل Python من [python.org](https://python.org) وثبته

### 2. تثبيت FFmpeg

حمل FFmpeg من [ffmpeg.org](https://ffmpeg.org) وأضفه لـ PATH

### 3. تثبيت المكتبات

```cmd
pip install -r requirements.txt
```

### 4. إعداد .env

انسخ `.env.example` إلى `.env` واملأ البيانات

### 5. توليد Session

```cmd
python generate_session.py
```

### 6. تشغيل البوت

```cmd
python main.py
```

---

## 🔧 نصائح التنصيب

### الأمان
- لا تشارك ملف `.env` مطلقاً
- استخدم string session مخصص لكل بوت
- فعّل المصادقة الثنائية

### الأداء
- استخدم VPS مع 1GB RAM على الأقل
- فعّل swap على الـ VPS
- استخدم PM2 للتشغيل المستمر

### التحديثات
- راجع [CHANGELOG.md](CHANGELOG.md) بانتظام
- احتفظ بنسخة احتياطية قبل التحديث
- اختبر على بيئة تجريبية أولاً

---

## 📞 الدعم

واجهت مشكلة؟

- **التيليجرام:** [@idseno](https://t.me/idseno)
- **القناة:** [@senovip](https://t.me/senovip)
- **البريد:** seno@example.com

---

<div align="center">

**🎵 نجاح التنصيب! استمتع بالبوت! 🎵**

**صُنع بـ ❤️ بواسطة [سينو](https://t.me/idseno)**

</div>
