#!/bin/bash

# Seno Music Bot - Run Script
# المطور: سينو (Seno) - @idseno
# القناة: @senovip

echo "╔═══════════════════════════════════════╗"
echo "║       🎵 Seno Music Bot 🎵           ║"
echo "║                                       ║"
echo "║   المطور: سينو (Seno)                ║"
echo "║   القناة: @senovip                   ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    echo "قم بتثبيت Python3 أولاً"
    exit 1
fi

echo "✅ Python3 موجود"

# التحقق من FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg غير مثبت!"
    echo "هل تريد تثبيته؟ (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        sudo apt-get update
        sudo apt-get install ffmpeg -y
    else
        echo "❌ FFmpeg مطلوب لتشغيل البوت"
        exit 1
    fi
fi

echo "✅ FFmpeg موجود"

# التحقق من المكتبات
echo "🔍 التحقق من المكتبات..."
pip3 install -r requirements.txt --quiet

# التحقق من ملف .env
if [ ! -f ".env" ]; then
    echo "⚠️ ملف .env غير موجود!"
    echo "هل تريد إنشاءه؟ (y/n)"
    read -r answer
    if [ "$answer" = "y" ]; then
        cp .env.example .env
        echo "✅ تم إنشاء .env من .env.example"
        echo "يرجى تعبئة المعلومات في ملف .env ثم إعادة التشغيل"
        exit 0
    else
        echo "❌ ملف .env مطلوب"
        exit 1
    fi
fi

echo "✅ ملف .env موجود"
echo ""
echo "🚀 جاري تشغيل البوت..."
echo ""

# تشغيل البوت
python3 main.py
