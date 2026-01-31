"""
Seno Music Bot - YouTube Helper
المطور: سينو (Seno) - @idseno
القناة: @senovip

وظائف التعامل مع يوتيوب والبحث والتنزيل
"""

import yt_dlp
from youtubesearchpython import VideosSearch
import os
import asyncio


async def search_youtube(query: str):
    """البحث عن أغنية في يوتيوب"""
    
    try:
        # إذا كان الاستعلام رابط يوتيوب
        if "youtube.com" in query or "youtu.be" in query:
            return await get_video_info_from_url(query)
        
        # البحث في يوتيوب
        search = VideosSearch(query, limit=1)
        result = await asyncio.to_thread(search.result)
        
        if not result or not result.get('result'):
            return None
        
        video = result['result'][0]
        
        return {
            'title': video['title'],
            'duration': video['duration'],
            'duration_seconds': video.get('duration', {}).get('secondsText', 0),
            'url': video['link'],
            'thumbnail': video['thumbnails'][0]['url'] if video.get('thumbnails') else None,
            'video_id': video['id']
        }
    
    except Exception as e:
        print(f"Error in search_youtube: {e}")
        return None


async def search_youtube_multiple(query: str, limit: int = 5):
    """البحث عن عدة أغاني في يوتيوب"""
    
    try:
        search = VideosSearch(query, limit=limit)
        result = await asyncio.to_thread(search.result)
        
        if not result or not result.get('result'):
            return []
        
        videos = []
        for video in result['result']:
            videos.append({
                'title': video['title'],
                'duration': video['duration'],
                'duration_seconds': video.get('duration', {}).get('secondsText', 0),
                'url': video['link'],
                'thumbnail': video['thumbnails'][0]['url'] if video.get('thumbnails') else None,
                'video_id': video['id']
            })
        
        return videos
    
    except Exception as e:
        print(f"Error in search_youtube_multiple: {e}")
        return []


async def get_video_info(video_id: str):
    """الحصول على معلومات فيديو من معرفه"""
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    return await get_video_info_from_url(url)


async def get_video_info_from_url(url: str):
    """الحصول على معلومات فيديو من رابطه"""
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            
            return {
                'title': info.get('title', 'Unknown'),
                'duration': f"{info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}",
                'duration_seconds': info.get('duration', 0),
                'url': url,
                'thumbnail': info.get('thumbnail'),
                'video_id': info.get('id')
            }
    
    except Exception as e:
        print(f"Error in get_video_info_from_url: {e}")
        return None


async def download_audio(url: str, output_path: str = "downloads"):
    """تنزيل صوت من يوتيوب للتشغيل"""
    
    try:
        # إنشاء مجلد التنزيل
        os.makedirs(output_path, exist_ok=True)
        
        # خيارات التنزيل
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_path}/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            
            # الحصول على مسار الملف
            file_path = f"{output_path}/{info['id']}.mp3"
            
            return file_path
    
    except Exception as e:
        print(f"Error in download_audio: {e}")
        return None


async def download_audio_for_send(url: str, output_path: str = "downloads"):
    """تنزيل صوت من يوتيوب للإرسال للمستخدم"""
    
    try:
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'writethumbnail': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            
            # مسار الملف الصوتي
            audio_file = None
            for ext in ['mp3', 'm4a', 'webm']:
                potential_file = f"{output_path}/{info['title']}.{ext}"
                if os.path.exists(potential_file):
                    audio_file = potential_file
                    break
            
            # مسار الصورة المصغرة
            thumbnail = None
            for ext in ['jpg', 'jpeg', 'png', 'webp']:
                potential_thumb = f"{output_path}/{info['title']}.{ext}"
                if os.path.exists(potential_thumb):
                    thumbnail = potential_thumb
                    break
            
            return audio_file, thumbnail
    
    except Exception as e:
        print(f"Error in download_audio_for_send: {e}")
        return None, None


async def download_thumbnail(url: str, output_path: str = "downloads/thumbnails"):
    """تنزيل الصورة المصغرة"""
    
    try:
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'writethumbnail': True,
            'skip_download': True,
            'outtmpl': f'{output_path}/%(id)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=True)
            
            # البحث عن الصورة المصغرة
            for ext in ['jpg', 'jpeg', 'png', 'webp']:
                thumb_path = f"{output_path}/{info['id']}.{ext}"
                if os.path.exists(thumb_path):
                    return thumb_path
            
            return None
    
    except Exception as e:
        print(f"Error in download_thumbnail: {e}")
        return None
