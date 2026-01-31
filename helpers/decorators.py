"""
Seno Music Bot - Decorators
المطور: سينو (Seno) - @idseno
القناة: @senovip

ديكوريتورز مخصصة للتحقق من الصلاحيات والاشتراك
"""

from functools import wraps
from pyrogram.types import Message
from config import Config
from handlers.subscription import check_user_subscription, send_subscription_message


def check_subscription(func):
    """ديكوريتور للتحقق من اشتراك المستخدم في القناة"""
    
    @wraps(func)
    async def wrapper(client, message: Message):
        # التحقق من الاشتراك
        is_subscribed = await check_user_subscription(client, message.from_user.id)
        
        if not is_subscribed:
            await send_subscription_message(message)
            return
        
        # تنفيذ الدالة إذا كان مشترك
        return await func(client, message)
    
    return wrapper


def only_owner(func):
    """ديكوريتور للسماح للمطور فقط"""
    
    @wraps(func)
    async def wrapper(client, message: Message):
        # التحقق من المعرف
        if message.from_user.id != Config.OWNER_ID:
            await message.reply_text(Config.ERROR_MSGS['no_permission'])
            return
        
        # تنفيذ الدالة إذا كان المطور
        return await func(client, message)
    
    return wrapper


def only_admin(func):
    """ديكوريتور للسماح للمشرفين فقط في المجموعات"""
    
    @wraps(func)
    async def wrapper(client, message: Message):
        # إذا كان في الخاص، السماح
        if message.chat.type == "private":
            return await func(client, message)
        
        # التحقق من الصلاحيات في المجموعة
        chat_member = await client.get_chat_member(
            message.chat.id,
            message.from_user.id
        )
        
        if chat_member.status not in ["creator", "administrator"]:
            await message.reply_text(Config.ERROR_MSGS['not_admin'])
            return
        
        # تنفيذ الدالة إذا كان مشرف
        return await func(client, message)
    
    return wrapper


def check_bot_admin(func):
    """ديكوريتور للتحقق من أن البوت مشرف"""
    
    @wraps(func)
    async def wrapper(client, message: Message):
        # إذا كان في الخاص، تخطي
        if message.chat.type == "private":
            return await func(client, message)
        
        # التحقق من صلاحيات البوت
        bot_member = await client.get_chat_member(
            message.chat.id,
            client.me.id
        )
        
        if bot_member.status not in ["administrator"]:
            await message.reply_text(Config.ERROR_MSGS['bot_not_admin'])
            return
        
        # تنفيذ الدالة
        return await func(client, message)
    
    return wrapper
