"""
Seno Music Bot - Subscription Handler
المطور: سينو (Seno) - @idseno
القناة: @senovip

معالج الاشتراك الإجباري في القناة
"""

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config


async def check_user_subscription(client: Client, user_id: int) -> bool:
    """التحقق من اشتراك المستخدم في القناة"""
    
    if not Config.CHANNEL_USERNAME:
        return True
    
    try:
        # محاولة الحصول على معلومات العضو
        member = await client.get_chat_member(
            Config.CHANNEL_USERNAME,
            user_id
        )
        
        # التحقق من حالة العضوية
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return True  # في حالة الخطأ، السماح بالمرور


async def send_subscription_message(message):
    """إرسال رسالة طلب الاشتراك"""
    
    subscription_text = f"""
🔒 **يجب الاشتراك في القناة أولاً!**

للاستمرار في استخدام البوت، يرجى:

1️⃣ الاشتراك في قناة المطور
2️⃣ العودة والضغط على "تحقق من الاشتراك"

━━━━━━━━━━━━━━
💡 **لماذا الاشتراك؟**
• للحصول على آخر التحديثات
• معرفة المميزات الجديدة
• الدعم الفني السريع

👨‍💻 **المطور:** {Config.DEVELOPER_NAME}
"""
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 اشترك في القناة",
                url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ تحقق من الاشتراك",
                callback_data="check_subscription"
            )
        ]
    ])
    
    try:
        await message.reply_text(
            subscription_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except:
        # في حالة كان callback query
        await message.message.reply_text(
            subscription_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


# معالج زر التحقق من الاشتراك
@Client.on_callback_query(filters.regex("^check_subscription$"))
async def check_subscription_callback(client: Client, callback_query):
    """معالج زر التحقق من الاشتراك"""
    
    user_id = callback_query.from_user.id
    
    # التحقق من الاشتراك
    is_subscribed = await check_user_subscription(client, user_id)
    
    if is_subscribed:
        await callback_query.answer(
            "✅ تم التحقق! يمكنك الآن استخدام البوت",
            show_alert=True
        )
        
        # حذف رسالة الاشتراك
        try:
            await callback_query.message.delete()
        except:
            pass
        
        # إرسال رسالة الترحيب
        welcome_text = Config.START_TEXT.format(
            developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
            channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})"
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📚 الأوامر", callback_data="help"),
                InlineKeyboardButton("ℹ️ حول", callback_data="about")
            ],
            [
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]
        ])
        
        await callback_query.message.reply_text(
            welcome_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    else:
        await callback_query.answer(
            "❌ لم تشترك بعد! اشترك في القناة أولاً",
            show_alert=True
        )


from pyrogram import filters
