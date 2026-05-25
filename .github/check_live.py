import requests
import os

username = "myrtech"
bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

# قراءة الحالة السابقة
state_file = "live_state.txt"
was_live = False
if os.path.exists(state_file):
    with open(state_file) as f:
        was_live = f.read().strip() == "live"

# فحص إذا الحساب لايف الآن
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
try:
    r = requests.get(f'https://www.tiktok.com/@{username}/live', headers=headers, timeout=10)
    is_live = '"status":4' in r.text or 'liveRoomUserInfo' in r.text
except:
    is_live = False

# حفظ الحالة الحالية
with open(state_file, 'w') as f:
    f.write("live" if is_live else "offline")

# إرسال إشعار فقط لما يبدأ اللايف (مرة وحدة)
if is_live and not was_live:
    msg = f"🔴 {username} يبث الآن على TikTok! انضم الآن 🎉"
    requests.get(
        f'https://api.telegram.org/bot{bot_token}/sendMessage',
        params={'chat_id': chat_id, 'text': msg}
    )
    print("✅ تم إرسال الإشعار!")
elif is_live:
    print("⏳ لايف شغال، الإشعار أُرسل مسبقاً")
else:
    print("💤 الحساب مو لايف")
