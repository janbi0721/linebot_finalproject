import json
def load_journal(date,user_id):
    print("取得的資料",date,user_id)
    with open('user_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for i in data[f"{user_id}"]["diaries"]:
        print(date == i["date"],type(date),type(i["date"]))
        if date == i["date"]:
            return i["entry"]
    return "找不到日記 請確認日期是否正確"