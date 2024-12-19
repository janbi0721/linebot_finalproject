"# linebot_finalproject" 
# LINE療心
目標 利用line讓人每天記錄日記 並利用openai檢測情緒 並且生成每周分析報告

# 诶不是 哥們
![alt text](image.png)

## 使用方法 重要


@所有人

## GIT 使用指南

### 0.複製資料庫到本地端
```git
git clone https://github.com/janbi0721/linebot_finalproject.git
```

### 1.建立資料庫 *警告 這個不會再做任何一次 不要再嘗試用了*
```git
echo "# week30926" >> README.md
git init
git config user.email "C112156229@nkust.edu.tw"
git config user.name "janbi0721"
git branch -M main
git remote add origin https://github.com/janbi0721/20240926.git #後面連結
```
### 2.如何將檔案上傳到github

```git
git add .				#丟入暫存區
git commit -m "你對這個版本的介紹"
git push -u origin main
```

### 3.將儲存庫下載到本機端
```git
git clone https://github.com/janbi0721/linebot_finalproject.git
```

### 4.更新github資料庫 (當我資料是舊版的時候)
```git
git pull
```

### 5.資料衝突 解決
ESC按著
```git
:wq
```

### 6.當pull不成功時如何解決 (簡單來說就是兩人同時改)
```git
git marge
git fetch
```
git marge 是檢查哪裡不同
!!注意 git fetch是強制取代

#########################################
https://pandeyshikha075.medium.com/building-a-chat-server-and-client-in-python-with-socket-programming-c76de52cc1d5
########################################
複製到本地端
git clone 儲存庫 #遠端儲存網址