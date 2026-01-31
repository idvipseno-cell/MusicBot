"""
Seno Music Bot - String Session Generator
المطور: سينو (Seno) - @idseno
القناة: @senovip

هذا السكريبت لتوليد String Session للحساب المساعد
"""

import asyncio
from pyrogram import Client

print("""
╔══════════════════════════════════════╗
║   Seno Music Bot - Session Generator ║
║                                      ║
║   المطور: سينو (Seno)               ║
║   القناة: @senovip                  ║
╚══════════════════════════════════════╝
""")

async def generate_session():
    api_id = input("\n📝 أدخل API ID: ")
    api_hash = input("📝 أدخل API HASH: ")
    
    if not api_id or not api_hash:
        print("\n❌ يجب إدخال API ID و API HASH!")
        return
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("\n❌ API ID يجب أن يكون رقماً!")
        return
    
    print("\n⏳ جاري الاتصال بتيليجرام...")
    
    async with Client(
        "seno_session",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True
    ) as app:
        print("\n✅ تم الاتصال بنجاح!")
        
        session_string = await app.export_session_string()
        
        print("\n" + "="*50)
        print("✨ تم توليد String Session بنجاح!")
        print("="*50)
        print("\n📋 انسخ السطر التالي والصقه في ملف .env:")
        print(f"\nSTRING_SESSION={session_string}")
        print("\n" + "="*50)
        
        with open("string_session.txt", "w") as f:
            f.write(session_string)
        
        print("\n💾 تم حفظ الـ Session في ملف string_session.txt")
        print("\n⚠️ تحذير: لا تشارك هذا الـ Session مع أحد!")
        print("\n✅ يمكنك الآن إغلاق هذا البرنامج والعودة لإعداد البوت")


if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n\n❌ تم الإلغاء!")
    except Exception as e:
        print(f"\n❌ حدث خطأ: {str(e)}")
