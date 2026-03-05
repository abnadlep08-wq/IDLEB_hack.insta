import os
import requests
import random
import time
import json
from datetime import datetime

# إعدادات البوت من GitHub Actions
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# إحصائيات
good_hot = 0
bad_hot = 0
good_ig = 0
bad_ig = 0
checked = 0

def send_telegram(message):
    """إرسال النتائج إلى تليجرام"""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, json=data)
    except:
        pass

def check_instagram(username):
    """التحقق من حساب انستغرام - كودك الأصلي"""
    global good_ig, bad_ig, checked
    
    try:
        # هنا نفس الكود الأصلي للتحقق من انستغرام
        headers = {
            'User-Agent': 'Instagram 100.0.0.17.129 Android',
            'Accept-Language': 'en-GB, en-US',
        }
        
        response = requests.get(f'https://www.instagram.com/{username}/?__a=1', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if 'graphql' in data:
                user = data['graphql']['user']
                good_ig += 1
                message = f"""
🎯 <b>تم صيد حساب!</b>

👤 المستخدم: @{username}
📧 البريد: {username}@hotmail.com
✅ الحالة: متاح
👥 متابعين: {user['edge_followed_by']['count']}
📸 منشورات: {user['edge_owner_to_timeline_media']['count']}
🔗 الرابط: https://www.instagram.com/{username}

MOOHAMED جـابلك متاح انستا 🇺🇸☝🏼
                """
                send_telegram(message)
            else:
                bad_ig += 1
        else:
            bad_ig += 1
            
    except Exception as e:
        bad_ig += 1
    
    checked += 1
    print(f"فحص: {username} | متاح: {good_ig} | غير متاح: {bad_ig} | total: {checked}")

def generate_usernames():
    """توليد أسماء مستخدمين عشوائية"""
    base_names = [
        'cristiano', 'leomessi', 'neymarjr', 'therock', 'arianagrande',
        'selenagomez', 'beyonce', 'taylorswift', 'kimkardashian', 'kyliejenner',
        'justinbieber', 'rihanna', 'drake', 'eminem', 'shakira',
        'zayn', 'dualipa', 'cardib', 'nickiminaj', 'jlo'
    ]
    
    usernames = []
    for name in base_names:
        for num in range(10):  # كل اسم مع 10 أرقام عشوائية
            usernames.append(f"{name}{random.randint(1, 9999)}")
    
    random.shuffle(usernames)
    return usernames

def main():
    """الدالة الرئيسية"""
    send_telegram("🚀 بدء الصيد على Instagram...")
    
    usernames = generate_usernames()
    
    for username in usernames[:100]:  # افحص أول 100 اسم
        check_instagram(username)
        time.sleep(random.randint(2, 5))  # تأخير عشوائي
    
    # إرسال تقرير نهائي
    final_message = f"""
📊 <b>تقرير الصيد النهائي</b>

✅ تم الصيد: {good_ig}
❌ غير متاح: {bad_ig}
🔄 تم الفحص: {checked}

🎯 انتهى الصيد!
    """
    send_telegram(final_message)

if __name__ == "__main__":
    main()
