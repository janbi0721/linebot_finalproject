import matplotlib.pyplot as plt
import numpy as np
import json
import os
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

# 讀取 JSON 檔案並將資料儲存在 data 變數中
with open('user_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def make_charts(userid):
    Feeling = [i["mood"] for i in data[f'{userid}']["moods"]]
    sleep = [i["hours"] for i in data[f'{userid}']["sleep"]]
    date_Feeling = [i["date"] for i in data[f'{userid}']["moods"]]
    date_sleep = [i['date'] for i in data[f'{userid}']["sleep"]]
    Feeling_array = np.array(Feeling)
    sleep_array = np.array(sleep)
    date_Feeling_array = np.array(date_Feeling)
    date_sleep_array = np.array(date_sleep)
    plt.figure(figsize=(10, 16))
    # 圖一：心情指數
    plt.subplot(2, 1, 1)
    plt.xticks(rotation=45)
    plt.ylim(0, 10)
    plt.xlabel('日期')
    plt.ylabel('心情指數')
    plt.title('每日心情指數')
    plt.bar(date_Feeling_array, Feeling_array)
    # 圖二：睡眠時間
    plt.subplot(2, 1, 2)
    plt.xticks(rotation=45)
    plt.ylim(0, 10)
    plt.xlabel('日期')
    plt.ylabel('睡眠時間 (小時)')
    plt.title('每日睡眠時間')
    plt.bar(date_sleep_array, sleep_array)
    # 添加大標題
    plt.suptitle('心情與睡眠分析報告', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=5.0)  # h_pad 用於調整垂直間距
    plt.savefig(f'{userid}_analysis_report.png')
    # 創建資料夾並儲存圖表為圖片
    output_dir = 'analysis_report'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'{userid}_analysis_report.png'))
    
    return {
        "平均睡眠時數": round(np.mean(sleep_array),1),
        "平均心情指數": round(np.mean(Feeling_array),1),
        "心情最差的日子": date_Feeling_array[np.where(Feeling_array == np.min(Feeling_array))].tolist(),
        "心情最好的日子": date_Feeling_array[np.where(Feeling_array == np.max(Feeling_array))].tolist(),
        "睡眠最少的日子": date_sleep_array[np.where(sleep_array == np.min(sleep_array))].tolist(),
        "睡眠最多的日子": date_sleep_array[np.where(sleep_array == np.max(sleep_array))].tolist()
    }
