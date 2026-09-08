import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ 內建標準庫

LINE_ACCESS_TOKEN = os.environ.get('LINE_ACCESS_TOKEN')
TARGET_ID = os.environ.get('TARGET_ID')

def get_dynamic_message():
    # 直接指定 Asia/Taipei 時區（自動處理台灣時間）
    now_tw = datetime.now(ZoneInfo("Asia/Taipei"))
    
    date_str = now_tw.strftime("%Y-%m-%d")
    time_str = "15:00"
    
    message = f"""【基隆區處轄區-今日04:00~15:00區間新聞輿情】
搜尋時間：{date_str} {time_str}
❌11小時內尚無本處轄區新聞。"""
    
    return message

def send_line_message():
    if not LINE_ACCESS_TOKEN or not TARGET_ID:
        print("Error: 缺少 LINE_ACCESS_TOKEN 或 TARGET_ID 環境變數")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": TARGET_ID,
        "messages": [
            {
                "type": "text",
                "text": get_dynamic_message()
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("訊息發送成功！")
    else:
        print(f"發送失敗，HTTP 狀態碼: {response.status_code}, 內容: {response.text}")

if __name__ == '__main__':
    send_line_message()
