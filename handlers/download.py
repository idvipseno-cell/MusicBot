"""
Seno Music Bot - Download Handler
المطور: سينو (Seno) - @idseno
القناة: @senovip

معالج أوامر تنزيل الأغاني
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helpers.youtube import search_youtube, download_audio_for_send
from helpers.decorators import check_subscription
from helpers.database import db
import os


@Client.on_message(filters.command(Config.COMMANDS['download'], prefixes="") & filters.private | filters.group)
@check_subscription
async def download_song(client: Client, message: Message):
    """تنزيل الأغاني"""
    
    user_name = message.from_user.first_name
    user_mention = message.from_user.mention
    
    # التحقق من النص
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **الاستخدام الصحيح:**\n\n"
            "• `نزل` [اسم الأغنية]\n"
            "• `نزل` [رابط يوتيوب]",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]])
        )
        return
    
    query = message.text.split(maxsplit=1)[1]
    
    # رسالة الانتظار
    status_msg = await message.reply_text("🔍 **جاري البحث...**")
    
    try:
        # البحث
        result = await search_youtube(query)
        
        if not result:
            await status_msg.edit_text(Config.ERROR_MSGS['search_failed'])
            return
        
        # التحقق من المدة
        duration_minutes = result.get('duration_seconds', 0) / 60
        if duration_minutes > Config.MAX_SONG_DURATION:
            await status_msg.edit_text(
                f"❌ **الأغنية طويلة جداً!**\n\n"
                f"الحد الأقصى: {Config.MAX_SONG_DURATION} دقيقة\n"
                f"مدة الأغنية: {int(duration_minutes)} دقيقة"
            )
            return
        
        await status_msg.edit_text(
            f"📥 **جاري التنزيل...**\n\n"
            f"📝 {result['title']}"
        )
        
        # التنزيل
        file_path, thumbnail = await download_audio_for_send(result['url'])
        
        if not file_path:
            await status_msg.edit_text(Config.ERROR_MSGS['download_failed'])
            return
        
        # التحقق من الحجم
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        if file_size > Config.MAX_DOWNLOAD_SIZE:
            os.remove(file_path)
            await status_msg.edit_text(
                f"❌ **الملف كبير جداً!**\n\n"
                f"الحد الأقصى: {Config.MAX_DOWNLOAD_SIZE} MB\n"
                f"حجم الملف: {int(file_size)} MB"
            )
            return
        
        await status_msg.edit_text("📤 **جاري الرفع...**")
        
        # الكابشن مع اسم المستخدم
        caption = f"""
🎵 **{result['title']}**

⏱ **المدة:** {result['duration']}
📊 **الحجم:** {int(file_size)} MB
👤 **تم التنزيل بواسطة:** {user_mention}

━━━━━━━━━━━━━━
💿 **Seno Music Bot** - [@{Config.CHANNEL_USERNAME.replace('@', '')}](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})
👨‍💻 **المطور:** {Config.DEVELOPER_NAME}
"""
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 تشغيل في المجموعة", switch_inline_query_current_chat=f"شغل {result['title']}")
            ],
            [
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]
        ])
        
        # إرسال الملف
        try:
            await message.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=thumbnail if thumbnail else Config.DOWNLOAD_IMG,
                duration=result.get('duration_seconds', 0),
                title=result['title'],
                performer="Seno Music Bot",
                reply_markup=keyboard
            )
            
            await status_msg.delete()
            
            # حفظ في قاعدة البيانات
            await db.save_download(message.from_user.id, result)
        
        except Exception as e:
            await status_msg.edit_text(f"❌ **خطأ في الرفع:** {str(e)}")
        
        finally:
            # حذف الملفات المؤقتة
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if thumbnail and os.path.exists(thumbnail):
                    os.remove(thumbnail)
            except:
                pass
    
    except Exception as e:
        print(f"Error in download_song: {e}")
        await status_msg.edit_text(
            f"❌ **حدث خطأ!**\n\n"
            f"الخطأ: {str(e)}"
        )


@Client.on_message(filters.command(Config.COMMANDS['search'], prefixes=""))
@check_subscription
async def search_song(client: Client, message: Message):
    """البحث عن أغنية"""
    
    if len(message.command) < 2:
        await message.reply_text(
            "❌ **الاستخدام الصحيح:**\n\n"
            "`بحث` [اسم الأغنية]"
        )
        return
    
    query = message.text.split(maxsplit=1)[1]
    
    status_msg = await message.reply_text("🔍 **جاري البحث...**")
    
    try:
        from helpers.youtube import search_youtube_multiple
        
        # البحث عن 5 نتائج
        results = await search_youtube_multiple(query, limit=5)
        
        if not results:
            await status_msg.edit_text(Config.ERROR_MSGS['search_failed'])
            return
        
        # بناء النتائج
        search_text = f"🔍 **نتائج البحث عن:** `{query}`\n\n"
        
        buttons = []
        
        for i, result in enumerate(results, 1):
            search_text += f"{i}. **{result['title']}**\n"
            search_text += f"   ⏱ {result['duration']}\n\n"
            
            buttons.append([
                InlineKeyboardButton(
                    f"{i}. تشغيل",
                    callback_data=f"play_{result['video_id']}"
                ),
                InlineKeyboardButton(
                    f"{i}. تنزيل",
                    callback_data=f"dl_{result['video_id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
        ])
        
        await status_msg.edit_text(
            search_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    except Exception as e:
        await status_msg.edit_text(f"❌ **خطأ:** {str(e)}")


# معالج أزرار البحث
@Client.on_callback_query(filters.regex("^(play|dl)_"))
async def search_callback(client: Client, callback_query):
    """معالج أزرار نتائج البحث"""
    
    data = callback_query.data
    action, video_id = data.split("_", 1)
    
    await callback_query.answer("⏳ جاري المعالجة...")
    
    try:
        from helpers.youtube import get_video_info
        
        video_info = await get_video_info(video_id)
        
        if action == "play":
            # إرسال رسالة للمستخدم لتشغيلها في المجموعة
            await callback_query.message.reply_text(
                f"✅ **لتشغيل الأغنية:**\n\n"
                f"انسخ الأمر التالي وأرسله في المجموعة:\n\n"
                f"`شغل {video_info['url']}`"
            )
        
        elif action == "dl":
            # بدء التنزيل
            status_msg = await callback_query.message.reply_text("📥 **جاري التنزيل...**")
            
            file_path, thumbnail = await download_audio_for_send(video_info['url'])
            
            if file_path:
                caption = f"""
🎵 **{video_info['title']}**

⏱ **المدة:** {video_info['duration']}
👤 **بواسطة:** {callback_query.from_user.mention}

━━━━━━━━━━━━━━
💿 **Seno Music Bot**
"""
                
                await callback_query.message.reply_audio(
                    audio=file_path,
                    caption=caption,
                    thumb=thumbnail,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
                    ]])
                )
                
                await status_msg.delete()
                
                # حذف الملفات
                try:
                    os.remove(file_path)
                    if thumbnail:
                        os.remove(thumbnail)
                except:
                    pass
            else:
                await status_msg.edit_text(Config.ERROR_MSGS['download_failed'])
    
    except Exception as e:
        await callback_query.message.reply_text(f"❌ **خطأ:** {str(e)}")
