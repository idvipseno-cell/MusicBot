"""
Seno Music Bot - Admin Handler
المطور: سينو (Seno) - @idseno
القناة: @senovip

معالج أوامر المطور والإدارة
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helpers.decorators import only_owner
from helpers.database import db
import psutil
import time
from datetime import datetime


start_time = time.time()


@Client.on_message(filters.command(Config.COMMANDS['start'], prefixes="") & filters.private)
async def start_command(client: Client, message: Message):
    """أمر البداية"""
    
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    # حفظ المستخدم
    await db.save_user(user_id, user_name)
    
    # رسالة الترحيب
    welcome_text = Config.START_TEXT.format(
        developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
        channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})"
    )
    
    # الأزرار
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 الأوامر", callback_data="help"),
            InlineKeyboardButton("ℹ️ حول", callback_data="about")
        ],
        [
            InlineKeyboardButton("➕ أضفني لمجموعتك", url=f"https://t.me/{client.me.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}"),
            InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{Config.DEVELOPER_USERNAME.replace('@', '')}")
        ],
        [
            InlineKeyboardButton("🤖 تنصيب بوت", callback_data="deploy")
        ]
    ])
    
    # إرسال صورة الترحيب
    try:
        await message.reply_photo(
            photo=Config.START_IMG,
            caption=welcome_text,
            reply_markup=keyboard
        )
    except:
        await message.reply_text(
            welcome_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


@Client.on_message(filters.command(Config.COMMANDS['help'], prefixes=""))
async def help_command(client: Client, message: Message):
    """أمر المساعدة"""
    
    help_text = Config.HELP_TEXT.format(
        developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
        channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 الرئيسية", callback_data="start"),
            InlineKeyboardButton("ℹ️ حول", callback_data="about")
        ],
        [
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
        ]
    ])
    
    await message.reply_text(
        help_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


@Client.on_message(filters.command(Config.COMMANDS['about'], prefixes=""))
async def about_command(client: Client, message: Message):
    """أمر حول البوت"""
    
    # الإحصائيات
    users_count = await db.get_users_count()
    groups_count = await db.get_groups_count()
    plays_count = await db.get_plays_count()
    
    about_text = Config.ABOUT_TEXT.format(
        developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
        channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})",
        users=users_count,
        groups=groups_count,
        songs=plays_count
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 الرئيسية", callback_data="start"),
            InlineKeyboardButton("📚 الأوامر", callback_data="help")
        ],
        [
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}"),
            InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{Config.DEVELOPER_USERNAME.replace('@', '')}")
        ]
    ])
    
    await message.reply_text(
        about_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# معالج الأزرار
@Client.on_callback_query(filters.regex("^(start|help|about|deploy)$"))
async def buttons_callback(client: Client, callback_query):
    """معالج أزرار القوائم"""
    
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if data == "start":
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
                InlineKeyboardButton("➕ أضفني لمجموعتك", url=f"https://t.me/{client.me.username}?startgroup=true")
            ],
            [
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}"),
                InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{Config.DEVELOPER_USERNAME.replace('@', '')}")
            ],
            [
                InlineKeyboardButton("🤖 تنصيب بوت", callback_data="deploy")
            ]
        ])
        
        await callback_query.message.edit_text(
            welcome_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    elif data == "help":
        help_text = Config.HELP_TEXT.format(
            developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
            channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})"
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 الرئيسية", callback_data="start"),
                InlineKeyboardButton("ℹ️ حول", callback_data="about")
            ],
            [
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]
        ])
        
        await callback_query.message.edit_text(
            help_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    elif data == "about":
        users_count = await db.get_users_count()
        groups_count = await db.get_groups_count()
        plays_count = await db.get_plays_count()
        
        about_text = Config.ABOUT_TEXT.format(
            developer=f"[{Config.DEVELOPER_NAME}]({Config.DEVELOPER_USERNAME})",
            channel=f"[@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})",
            users=users_count,
            groups=groups_count,
            songs=plays_count
        )
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 الرئيسية", callback_data="start"),
                InlineKeyboardButton("📚 الأوامر", callback_data="help")
            ],
            [
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}"),
                InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{Config.DEVELOPER_USERNAME.replace('@', '')}")
            ]
        ])
        
        await callback_query.message.edit_text(
            about_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    elif data == "deploy":
        deploy_text = f"""
🤖 **تنصيب بوت موسيقى خاص بك!**

احصل على بوت موسيقى احترافي بحقوقك الكاملة مع:

**✨ المميزات:**
━━━━━━━━━━━━━━
✅ بوت كامل بحقوقك
✅ دعم فني مستمر
✅ تحديثات دورية مجانية
✅ استضافة آمنة ومستقرة
✅ لوحة تحكم شاملة
✅ تخصيص كامل

**💰 السعر:**
• اشتراك شهري: **${Config.SUBSCRIPTION_PRICE}**
• يشمل: البوت + الاستضافة + الدعم

**📞 للتواصل والطلب:**
تواصل مع المطور مباشرة:
{Config.DEVELOPER_USERNAME}

━━━━━━━━━━━━━━
🌟 **استثمر في بوتك الخاص اليوم!**
"""
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👨‍💻 تواصل للطلب", url=f"https://t.me/{Config.DEVELOPER_USERNAME.replace('@', '')}")
            ],
            [
                InlineKeyboardButton("🏠 الرئيسية", callback_data="start")
            ]
        ])
        
        await callback_query.message.edit_text(
            deploy_text,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    await callback_query.answer()


# أوامر المطور
@Client.on_message(filters.command(["احصائيات", "stats"]) & filters.user(Config.OWNER_ID))
@only_owner
async def stats_command(client: Client, message: Message):
    """إحصائيات البوت (للمطور فقط)"""
    
    # جمع البيانات
    users_count = await db.get_users_count()
    groups_count = await db.get_groups_count()
    plays_count = await db.get_plays_count()
    downloads_count = await db.get_downloads_count()
    
    # معلومات السيرفر
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    # مدة التشغيل
    uptime_seconds = int(time.time() - start_time)
    uptime = f"{uptime_seconds // 3600}ساعة {(uptime_seconds % 3600) // 60}دقيقة"
    
    stats_text = f"""
📊 **إحصائيات البوت**

**👥 المستخدمين:**
• العدد الكلي: `{users_count}`
• المجموعات: `{groups_count}`

**🎵 الاستخدام:**
• مرات التشغيل: `{plays_count}`
• مرات التنزيل: `{downloads_count}`

**💻 السيرفر:**
• CPU: `{cpu_usage}%`
• RAM: `{ram_usage}%`
• Disk: `{disk_usage}%`
• Uptime: `{uptime}`

**📅 التاريخ:**
`{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`

━━━━━━━━━━━━━━
👨‍💻 **المطور:** {Config.DEVELOPER_NAME}
"""
    
    await message.reply_text(stats_text)


@Client.on_message(filters.command(["اذاعة", "broadcast"]) & filters.user(Config.OWNER_ID))
@only_owner
async def broadcast_command(client: Client, message: Message):
    """إذاعة رسالة لجميع المستخدمين (للمطور فقط)"""
    
    if not message.reply_to_message:
        await message.reply_text("❌ **رد على رسالة للإذاعة!**")
        return
    
    # الحصول على جميع المستخدمين
    users = await db.get_all_users()
    
    success = 0
    failed = 0
    
    status_msg = await message.reply_text("📢 **جاري الإذاعة...**")
    
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
            
            if success % 20 == 0:
                await status_msg.edit_text(
                    f"📢 **جاري الإذاعة...**\n\n"
                    f"✅ نجح: {success}\n"
                    f"❌ فشل: {failed}"
                )
        except:
            failed += 1
    
    await status_msg.edit_text(
        f"✅ **اكتملت الإذاعة!**\n\n"
        f"✅ نجح: {success}\n"
        f"❌ فشل: {failed}"
    )


@Client.on_message(filters.command(["المستخدمين", "users"]) & filters.user(Config.OWNER_ID))
@only_owner
async def users_command(client: Client, message: Message):
    """عرض معلومات المستخدمين (للمطور فقط)"""
    
    users_count = await db.get_users_count()
    groups_count = await db.get_groups_count()
    
    text = f"""
👥 **معلومات المستخدمين**

• المستخدمين: `{users_count}`
• المجموعات: `{groups_count}`
• المجموع: `{users_count + groups_count}`

━━━━━━━━━━━━━━
📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    
    await message.reply_text(text)
