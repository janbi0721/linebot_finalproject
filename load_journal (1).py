import json
def load_journal(date,user_id):
    with open('user_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for i in data["user_id"]["diaries"]:
        if date == i["date"]:
            return i["entry"]