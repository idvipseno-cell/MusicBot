"""
Seno Music Bot - Main File
المطور: سينو (Seno) - @idseno
القناة: @senovip

الملف الرئيسي لتشغيل البوت
"""

import asyncio
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import Config

# إعداد الـ logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# بانر البوت
BANNER = """
╔═══════════════════════════════════════╗
║                                       ║
║       🎵 Seno Music Bot 🎵           ║
║                                       ║
║   البوت الأكثر تطوراً لتشغيل        ║
║      الموسيقى في تيليجرام           ║
║                                       ║
║   المطور: سينو (Seno)                ║
║   القناة: @senovip                   ║
║   الحساب: @idseno                    ║
║                                       ║
║   النسخة: 3.0 Advanced               ║
║                                       ║
╚═══════════════════════════════════════╝
"""


async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    
    # طباعة البانر
    print(BANNER)
    
    # التحقق من الإعدادات
    print("🔍 جاري التحقق من الإعدادات...")
    
    if not Config.check_config():
        print("\n❌ فشل التحقق من الإعدادات!")
        print("⚠️ يرجى مراجعة ملف .env وإكمال جميع المعلومات المطلوبة.")
        return
    
    print("✅ الإعدادات صحيحة!")
    
    # إنشاء البوت الرئيسي
    print("\n🤖 جاري تشغيل البوت الرئيسي...")
    
    app = Client(
        "seno_music_bot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="handlers")
    )
    
    # إنشاء الحساب المساعد
    print("👤 جاري تشغيل الحساب المساعد...")
    
    assistant = Client(
        "seno_assistant",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.STRING_SESSION
    )
    
    # إنشاء PyTgCalls
    print("📞 جاري تشغيل PyTgCalls...")
    
    global call_py
    call_py = PyTgCalls(assistant)
    
    # بدء التشغيل
    print("\n" + "="*50)
    print("🚀 جاري بدء التشغيل...")
    print("="*50 + "\n")
    
    try:
        # بدء البوت
        await app.start()
        print("✅ البوت الرئيسي يعمل!")
        
        # بدء الحساب المساعد
        await assistant.start()
        print("✅ الحساب المساعد يعمل!")
        
        # بدء PyTgCalls
        await call_py.start()
        print("✅ PyTgCalls يعمل!")
        
        # طباعة معلومات البوت
        me = await app.get_me()
        assistant_me = await assistant.get_me()
        
        print("\n" + "="*50)
        print("📊 معلومات البوت:")
        print("="*50)
        print(f"🤖 البوت: @{me.username}")
        print(f"👤 الحساب المساعد: @{assistant_me.username}")
        print(f"👨‍💻 المطور: {Config.DEVELOPER_NAME} ({Config.DEVELOPER_USERNAME})")
        print(f"📢 القناة: {Config.CHANNEL_USERNAME}")
        print("="*50)
        
        print("\n✅ البوت يعمل بنجاح!")
        print("🎵 جاهز لتشغيل الموسيقى!\n")
        
        # الانتظار حتى يتم إيقاف البوت
        await asyncio.Event().wait()
    
    except KeyboardInterrupt:
        print("\n⚠️ تم إيقاف البوت يدوياً...")
    
    except Exception as e:
        logger.error(f"❌ حدث خطأ: {e}")
        print(f"\n❌ حدث خطأ: {e}")
    
    finally:
        # إيقاف البوت
        print("\n🛑 جاري إيقاف البوت...")
        
        try:
            await call_py.stop()
            print("✅ تم إيقاف PyTgCalls")
        except:
            pass
        
        try:
            await assistant.stop()
            print("✅ تم إيقاف الحساب المساعد")
        except:
            pass
        
        try:
            await app.stop()
            print("✅ تم إيقاف البوت الرئيسي")
        except:
            pass
        
        print("\n👋 وداعاً! شكراً لاستخدام Seno Music Bot")
        print(f"👨‍💻 المطور: {Config.DEVELOPER_NAME} ({Config.DEVELOPER_USERNAME})\n")


if __name__ == "__main__":
    # تشغيل البوت
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
