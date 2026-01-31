# 🚀 دليل التثبيت السريع - Seno Music Bot

## المطور: سينو (Seno) - [@idseno](https://t.me/idseno)
## القناة: [@senovip](https://t.me/senovip)

---

## ⚡ التثبيت السريع (5 دقائق)

### 1️⃣ تحميل المشروع

```bash
git clone https://github.com/YOUR-USERNAME/seno-music-bot.git
cd seno-music-bot
```

### 2️⃣ تثبيت المتطلبات

```bash
# تثبيت Python Libraries
pip3 install -r requirements.txt

# تثبيت FFmpeg
sudo apt-get install ffmpeg -y  # Linux
brew install ffmpeg              # macOS
```

### 3️⃣ إعداد المتغيرات

```bash
# نسخ ملف المتغيرات
cp .env.example .env

# تعديل الملف
nano .env
```

املأ المعلومات التالية في `.env`:

```env
API_ID=YOUR_API_ID                    # من my.telegram.org
API_HASH=YOUR_API_HASH                # من my.telegram.org
BOT_TOKEN=YOUR_BOT_TOKEN              # من @BotFather
STRING_SESSION=                       # سنحصل عليه في الخطوة التالية
OWNER_ID=YOUR_USER_ID                 # معرفك الرقمي
CHANNEL_USERNAME=@senovip             # قناتك
DEVELOPER_NAME=اسمك
DEVELOPER_USERNAME=@معرفك
```

### 4️⃣ توليد String Session

```bash
python3 generate_session.py
```

اتبع التعليمات:
1. أدخل API ID
2. أدخل API Hash
3. أدخل رقم هاتف الحساب المساعد
4. أدخل كود التحقق
5. انسخ الـ String Session والصقه في `.env`

### 5️⃣ تشغيل البوت

```bash
python3 main.py
```

✅ **تهانينا! البوت يعمل الآن!** 🎉

---

## 🆘 حل المشاكل السريع

### مشكلة: `ModuleNotFoundError`
```bash
pip3 install -r requirements.txt --upgrade
```

### مشكلة: `FFmpeg not found`
```bash
sudo apt-get install ffmpeg -y
```

### مشكلة: `Invalid session string`
```bash
# احذف الجلسات القديمة
rm *.session*

# أعد توليد String Session
python3 generate_session.py
```

---

## 📞 الدعم

- **التيليجرام:** [@idseno](https://t.me/idseno)
- **القناة:** [@senovip](https://t.me/senovip)

---

<div align="center">

**صُنع بـ ❤️ بواسطة [سينو](https://t.me/idseno)**

</div>
