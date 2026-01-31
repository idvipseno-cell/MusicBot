"""
Seno Music Bot - Music Handler
المطور: سينو (Seno) - @idseno
القناة: @senovip

معالج أوامر تشغيل الموسيقى
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import asyncio
from config import Config
from helpers.youtube import search_youtube, download_audio
from helpers.decorators import check_subscription, only_admin
from helpers.database import db

# قائمة التشغيل لكل مجموعة
queues = {}


async def play_next(chat_id: int, call: PyTgCalls):
    """تشغيل الأغنية التالية من القائمة"""
    if chat_id in queues and len(queues[chat_id]) > 0:
        next_song = queues[chat_id].pop(0)
        
        try:
            await call.play(
                chat_id,
                AudioPiped(next_song['file'])
            )
            
            return next_song
        except Exception as e:
            print(f"Error playing next song: {e}")
            return await play_next(chat_id, call)
    
    return None


@Client.on_message(filters.command(Config.COMMANDS['play'], prefixes="") & filters.group)
@check_subscription
async def play_music(client: Client, message: Message):
    """تشغيل الموسيقى في المكالمة"""
    
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    # التحقق من وجود نص أو رد على رسالة
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "❌ **الاستخدام الصحيح:**\n\n"
            "• `شغل` [اسم الأغنية]\n"
            "• `شغل` [رابط يوتيوب]\n"
            "• رد على ملف صوتي بـ `شغل`",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]])
        )
        return
    
    # رسالة الانتظار
    status_msg = await message.reply_text("🔍 **جاري البحث عن الأغنية...**")
    
    try:
        # إذا كان رد على ملف صوتي
        if message.reply_to_message and message.reply_to_message.audio:
            audio = message.reply_to_message.audio
            file_path = await message.reply_to_message.download()
            
            song_info = {
                'title': audio.title or audio.file_name,
                'duration': audio.duration,
                'file': file_path,
                'thumbnail': Config.PLAYING_IMG,
                'requester': user_name
            }
        
        else:
            # البحث في يوتيوب
            query = message.text.split(maxsplit=1)[1]
            
            await status_msg.edit_text("🔍 **جاري البحث في يوتيوب...**")
            
            # البحث
            result = await search_youtube(query)
            
            if not result:
                await status_msg.edit_text(Config.ERROR_MSGS['search_failed'])
                return
            
            await status_msg.edit_text("📥 **جاري تحميل الأغنية...**")
            
            # التحميل
            file_path = await download_audio(result['url'])
            
            if not file_path:
                await status_msg.edit_text(Config.ERROR_MSGS['download_failed'])
                return
            
            song_info = {
                'title': result['title'],
                'duration': result['duration'],
                'file': file_path,
                'thumbnail': result['thumbnail'],
                'url': result['url'],
                'requester': user_name
            }
        
        # إضافة للقائمة
        if chat_id not in queues:
            queues[chat_id] = []
        
        queues[chat_id].append(song_info)
        
        # الحصول على PyTgCalls
        from main import call_py
        
        # إذا لم يكن هناك تشغيل حالي
        if len(queues[chat_id]) == 1:
            await status_msg.edit_text("🎵 **جاري التشغيل...**")
            
            await call_py.play(
                chat_id,
                AudioPiped(song_info['file'])
            )
            
            # رسالة التشغيل
            caption = f"""
🎵 **الآن يتم التشغيل**

📝 **العنوان:** {song_info['title']}
⏱ **المدة:** {song_info.get('duration', 'غير معروف')}
👤 **بواسطة:** {user_name}

━━━━━━━━━━━━━━
💿 **تم التشغيل بواسطة:** [Seno Music Bot](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})
"""
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⏸ إيقاف مؤقت", callback_data="pause"),
                    InlineKeyboardButton("⏭ تخطي", callback_data="skip"),
                    InlineKeyboardButton("⏹ إيقاف", callback_data="stop")
                ],
                [
                    InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
                ]
            ])
            
            await status_msg.delete()
            
            # إرسال صورة التشغيل
            try:
                await message.reply_photo(
                    photo=song_info.get('thumbnail', Config.PLAYING_IMG),
                    caption=caption,
                    reply_markup=keyboard
                )
            except:
                await message.reply_text(caption, reply_markup=keyboard)
            
            # حفظ في قاعدة البيانات
            await db.save_play(chat_id, song_info)
        
        else:
            # إضافة لقائمة الانتظار
            position = len(queues[chat_id])
            
            await status_msg.edit_text(
                f"✅ **تمت الإضافة لقائمة الانتظار**\n\n"
                f"📝 **العنوان:** {song_info['title']}\n"
                f"🔢 **الترتيب:** #{position}\n"
                f"👤 **بواسطة:** {user_name}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📋 قائمة التشغيل", callback_data="queue")
                ]])
            )
    
    except Exception as e:
        print(f"Error in play_music: {e}")
        await status_msg.edit_text(
            f"❌ **حدث خطأ أثناء التشغيل!**\n\n"
            f"الخطأ: {str(e)}"
        )


@Client.on_message(filters.command(Config.COMMANDS['pause'], prefixes="") & filters.group)
@only_admin
async def pause_music(client: Client, message: Message):
    """إيقاف التشغيل مؤقتاً"""
    
    chat_id = message.chat.id
    
    from main import call_py
    
    try:
        await call_py.pause_stream(chat_id)
        
        await message.reply_text(
            "⏸ **تم إيقاف التشغيل مؤقتاً**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("▶️ استمرار", callback_data="resume")
            ]])
        )
    except Exception as e:
        await message.reply_text(Config.ERROR_MSGS['not_in_call'])


@Client.on_message(filters.command(Config.COMMANDS['resume'], prefixes="") & filters.group)
@only_admin
async def resume_music(client: Client, message: Message):
    """استكمال التشغيل"""
    
    chat_id = message.chat.id
    
    from main import call_py
    
    try:
        await call_py.resume_stream(chat_id)
        
        await message.reply_text(
            "▶️ **تم استكمال التشغيل**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⏸ إيقاف مؤقت", callback_data="pause")
            ]])
        )
    except Exception as e:
        await message.reply_text(Config.ERROR_MSGS['not_in_call'])


@Client.on_message(filters.command(Config.COMMANDS['stop'], prefixes="") & filters.group)
@only_admin
async def stop_music(client: Client, message: Message):
    """إيقاف التشغيل نهائياً"""
    
    chat_id = message.chat.id
    
    from main import call_py
    
    try:
        await call_py.leave_group_call(chat_id)
        
        # مسح القائمة
        if chat_id in queues:
            queues[chat_id].clear()
        
        await message.reply_text(
            "⏹ **تم إيقاف التشغيل**\n\n"
            "شكراً لاستخدامك Seno Music Bot 🎵",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]])
        )
    except Exception as e:
        await message.reply_text(Config.ERROR_MSGS['not_in_call'])


@Client.on_message(filters.command(Config.COMMANDS['skip'], prefixes="") & filters.group)
@only_admin
async def skip_music(client: Client, message: Message):
    """تخطي للأغنية التالية"""
    
    chat_id = message.chat.id
    
    from main import call_py
    
    if chat_id not in queues or len(queues[chat_id]) == 0:
        await message.reply_text(Config.ERROR_MSGS['queue_empty'])
        return
    
    try:
        # تخطي الأغنية الحالية
        next_song = await play_next(chat_id, call_py)
        
        if next_song:
            caption = f"""
⏭ **تم التخطي للأغنية التالية**

📝 **العنوان:** {next_song['title']}
⏱ **المدة:** {next_song.get('duration', 'غير معروف')}

━━━━━━━━━━━━━━
💿 **تم التشغيل بواسطة:** [Seno Music Bot](https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')})
"""
            
            await message.reply_text(
                caption,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
                ]])
            )
        else:
            await call_py.leave_group_call(chat_id)
            await message.reply_text("✅ **انتهت قائمة التشغيل**")
    
    except Exception as e:
        await message.reply_text(f"❌ **خطأ:** {str(e)}")


@Client.on_message(filters.command(Config.COMMANDS['queue'], prefixes="") & filters.group)
async def queue_list(client: Client, message: Message):
    """عرض قائمة التشغيل"""
    
    chat_id = message.chat.id
    
    if chat_id not in queues or len(queues[chat_id]) == 0:
        await message.reply_text(
            "📭 **قائمة التشغيل فارغة**\n\n"
            "استخدم `شغل` لإضافة أغاني!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
            ]])
        )
        return
    
    queue_text = "📋 **قائمة التشغيل الحالية:**\n\n"
    
    for i, song in enumerate(queues[chat_id], 1):
        if i == 1:
            queue_text += f"🎵 **الآن:** {song['title']}\n"
            queue_text += f"   👤 بواسطة: {song['requester']}\n\n"
        else:
            queue_text += f"{i}. {song['title']}\n"
            queue_text += f"   👤 {song['requester']}\n"
    
    queue_text += f"\n📊 **المجموع:** {len(queues[chat_id])} أغنية"
    
    await message.reply_text(
        queue_text,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📢 القناة", url=f"https://t.me/{Config.CHANNEL_USERNAME.replace('@', '')}")
        ]])
    )


# معالجات الأزرار
@Client.on_callback_query(filters.regex("^(pause|resume|skip|stop|queue)$"))
async def button_handler(client: Client, callback_query):
    """معالج أزرار التحكم"""
    
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    # التحقق من الصلاحيات
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.status not in ["creator", "administrator"]:
        await callback_query.answer("❌ هذا الأمر للمشرفين فقط!", show_alert=True)
        return
    
    from main import call_py
    
    try:
        if data == "pause":
            await call_py.pause_stream(chat_id)
            await callback_query.answer("⏸ تم الإيقاف المؤقت")
        
        elif data == "resume":
            await call_py.resume_stream(chat_id)
            await callback_query.answer("▶️ تم الاستكمال")
        
        elif data == "skip":
            next_song = await play_next(chat_id, call_py)
            if next_song:
                await callback_query.answer(f"⏭ تم التخطي: {next_song['title']}")
            else:
                await call_py.leave_group_call(chat_id)
                await callback_query.answer("✅ انتهت القائمة")
        
        elif data == "stop":
            await call_py.leave_group_call(chat_id)
            if chat_id in queues:
                queues[chat_id].clear()
            await callback_query.answer("⏹ تم الإيقاف")
        
        elif data == "queue":
            # عرض القائمة
            await callback_query.answer("📋 قائمة التشغيل")
    
    except Exception as e:
        await callback_query.answer(f"❌ خطأ: {str(e)}", show_alert=True)
