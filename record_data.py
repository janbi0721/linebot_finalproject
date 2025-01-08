import json
import os
from datetime import datetime

DATA_FILE = "user_data.json"
#############################################
# 用戶資料操作函數

# 確保用戶存在，若不存在則新增
def ensure_user_exists(user_id):

    data = load_user_data()
    if user_id not in data:
        # 初始化用戶數據
        data[user_id] = {"moods": [], "diaries": [], "sleep": []}
        print(f"新增用戶: {user_id}")
    save_user_data(data)

#載入用戶資料
def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 保存用戶資料
def save_user_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

##################################
# 記錄用戶數據函數

#記錄心情
def record_mood(user_id, mood):
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {"moods": [], "diaries": [], "sleep": []}
    today = datetime.now().strftime("%Y-%m-%d")
    found = False
    for mood_entry in data[user_id]["moods"]:
        if mood_entry["date"] == today:
            mood_entry["mood"] = mood
            found = True
            break
    if not found:
        data[user_id]["moods"].append({"date": today, "mood": mood})
    save_user_data(data)

#紀錄日記
# 紀錄日記
def record_diary(user_id, entry):
    data = load_user_data()  # 載入現有的用戶資料
    if user_id not in data:
        data[user_id] = {"moods": [], "diaries": [], "sleep": []}
    today = datetime.now().strftime("%Y-%m-%d")
    # 檢查當天是否已有日記
    for diary in data[user_id]["diaries"]:
        if diary["date"] == today:
            # 覆蓋當天的日記
            diary["entry"] = entry
            break
    else:
        # 如果沒有當天的日記，新增一條新的日記
        data[user_id]["diaries"].append({"date": today, "entry": entry})
    save_user_data(data)

# 紀錄睡眠時間（同一天覆蓋舊資料）
def record_sleep(user_id, hours):
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {"moods": [], "diaries": [], "sleep": []}
    today = datetime.now().strftime("%Y-%m-%d")
    found = False
    for sleep_entry in data[user_id]["sleep"]:
        if sleep_entry["date"] == today:
            sleep_entry["hours"] = hours
            found = True
            break
    if not found:
        data[user_id]["sleep"].append({"date": today, "hours": hours})
    save_user_data(data)

