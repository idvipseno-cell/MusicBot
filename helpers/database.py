"""
Seno Music Bot - Database Helper
المطور: سينو (Seno) - @idseno
القناة: @senovip

إدارة قاعدة البيانات (MongoDB أو ملف محلي)
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from config import Config


class Database:
    """كلاس إدارة قاعدة البيانات"""
    
    def __init__(self):
        self.db_file = "database.json"
        self.data = self._load_db()
    
    def _load_db(self) -> Dict:
        """تحميل قاعدة البيانات"""
        
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # قاعدة بيانات افتراضية
        return {
            'users': {},
            'groups': {},
            'plays': [],
            'downloads': []
        }
    
    def _save_db(self):
        """حفظ قاعدة البيانات"""
        
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    # المستخدمين
    async def save_user(self, user_id: int, name: str):
        """حفظ مستخدم جديد"""
        
        user_id_str = str(user_id)
        
        if user_id_str not in self.data['users']:
            self.data['users'][user_id_str] = {
                'name': name,
                'joined': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            }
        else:
            self.data['users'][user_id_str]['last_seen'] = datetime.now().isoformat()
            self.data['users'][user_id_str]['name'] = name
        
        self._save_db()
    
    async def get_users_count(self) -> int:
        """الحصول على عدد المستخدمين"""
        return len(self.data['users'])
    
    async def get_all_users(self) -> List[int]:
        """الحصول على جميع معرفات المستخدمين"""
        return [int(uid) for uid in self.data['users'].keys()]
    
    # المجموعات
    async def save_group(self, group_id: int, title: str):
        """حفظ مجموعة جديدة"""
        
        group_id_str = str(group_id)
        
        if group_id_str not in self.data['groups']:
            self.data['groups'][group_id_str] = {
                'title': title,
                'joined': datetime.now().isoformat(),
                'last_active': datetime.now().isoformat()
            }
        else:
            self.data['groups'][group_id_str]['last_active'] = datetime.now().isoformat()
            self.data['groups'][group_id_str]['title'] = title
        
        self._save_db()
    
    async def get_groups_count(self) -> int:
        """الحصول على عدد المجموعات"""
        return len(self.data['groups'])
    
    # التشغيل
    async def save_play(self, chat_id: int, song_info: Dict):
        """حفظ سجل تشغيل"""
        
        play_record = {
            'chat_id': chat_id,
            'title': song_info.get('title'),
            'url': song_info.get('url'),
            'requester': song_info.get('requester'),
            'timestamp': datetime.now().isoformat()
        }
        
        self.data['plays'].append(play_record)
        
        # الاحتفاظ بآخر 1000 سجل فقط
        if len(self.data['plays']) > 1000:
            self.data['plays'] = self.data['plays'][-1000:]
        
        self._save_db()
    
    async def get_plays_count(self) -> int:
        """الحصول على عدد مرات التشغيل"""
        return len(self.data['plays'])
    
    # التنزيلات
    async def save_download(self, user_id: int, song_info: Dict):
        """حفظ سجل تنزيل"""
        
        download_record = {
            'user_id': user_id,
            'title': song_info.get('title'),
            'url': song_info.get('url'),
            'timestamp': datetime.now().isoformat()
        }
        
        self.data['downloads'].append(download_record)
        
        # الاحتفاظ بآخر 1000 سجل فقط
        if len(self.data['downloads']) > 1000:
            self.data['downloads'] = self.data['downloads'][-1000:]
        
        self._save_db()
    
    async def get_downloads_count(self) -> int:
        """الحصول على عدد مرات التنزيل"""
        return len(self.data['downloads'])


# إنشاء instance واحد من الـ Database
db = Database()
