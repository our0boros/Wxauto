# 导入
from wxauto import WeChat
import time
from datetime import datetime, timezone, timedelta
import requests
import json

def send_message(data):
    # Send a POST request to the receiver
    url = 'http://localhost:5000/receive_message'

    response = requests.post(url, json=data)
    
    # Print the response from the receiver
    if response.status_code == 200:
        print(f"Message sent successfully: {response.json()}")
    else:
        print(f"Failed to send message: {response.json()}")

# 设置澳大利亚堪培拉时区
canberra_tz = timezone(timedelta(hours=11))

# 获取微信窗口对象
wx = WeChat()
# 输出 > 初始化成功，获取到已登录窗口：xxxx

listen_list = [
    '8715 The Guild?'
]
for i in listen_list:
    wx.AddListenChat(who=i, savepic=True)

# 持续监听消息，并且收到消息后回复“收到”
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who              # 获取聊天窗口名（人或群名）
        one_msgs = msgs.get(chat)   # 获取消息内容

        # 回复收到
        for msg in one_msgs:
            timestamp = datetime.now(canberra_tz).strftime('%Y-%m-%d %H:%M')
            message_data = f'[{msg[0]}][{timestamp}]：{msg[1]}'
            print(message_data)
        # ===================================================
        # 处理消息逻辑（如果有）
        # 
        # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
        # 
        # ===================================================
        # Example usage
        send_message(message_data)
        
        # if msgtype == 'friend':
        #     chat.SendMsg('收到')  # 回复收到
    time.sleep(wait)
