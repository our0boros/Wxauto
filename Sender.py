# 导入
from wxauto import WeChat
import time
from datetime import datetime, timezone, timedelta
import requests
import json

import os
import base64

def send_message(data_title, data):
    # Check if the path is valid and the file exists
    print(os.path.exists(data) , os.path.isfile(data))
    if os.path.exists(data) and os.path.isfile(data):
        print("内容为文件信息")
        # If the file exists, open it as an image and convert it to base64
        with open(data, 'rb') as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')  # Convert to base64 string
        message_data = {
            'recipient': 'Robot',  # Example recipient (you can customize this)
            'message': img_base64,  # Send the base64 encoded image
            'is_image': True,  # Indicate that this is an image
            'title': data_title
        }
    else:
        print("内容为文字信息")
        # If the path doesn't exist or is not a file, treat it as a text message
        message_data = {
            'recipient': 'Robot',  # Example recipient (you can customize this)
            'message': data,  # The message is passed as a string
            'is_image': False,  # Indicate that this is not an image
            'title': data_title
        }

    # Send a POST request to the receiver with JSON data
    # url = 'http://localhost:5000/receive_message'
    # url = "http://cf82-150-203-24-13.ngrok-free.app/receive_message"
    url = "http://7e288ac2.au.cpolar.io/receive_message"

    try:
        # Send the POST request with the structured data
        response = requests.post(url, json=message_data)
        
        # Check if the response status code is 200
        if response.status_code == 200:
            try:
                # Try to parse the response as JSON
                response_json = response.json()
                print(f"Message sent successfully: {response_json}")
            except json.JSONDecodeError:
                # Handle case where the response is not JSON
                print(f"Failed to parse response as JSON. Raw response: {response.text}")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network errors)
        print(f"An error occurred while sending the message: {e}")




# 设置澳大利亚堪培拉时区
canberra_tz = timezone(timedelta(hours=11))

# 获取微信窗口对象
wx = WeChat()

# 输出 > 初始化成功，获取到已登录窗口：xxxx

listen_list = [
    'GameLoop'
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
        # print("### ", who)
        # 回复收到
        for msg in one_msgs:
            if msg[0] != 'SYS':
                timestamp = datetime.now(canberra_tz).strftime('%Y-%m-%d %H:%M')
                message_data = f'{msg[1]}'
                message_title = f'[{msg[0]}][{timestamp}]: '
                print(message_title, message_data)
                # ===================================================
                # 处理消息逻辑（如果有）
                # 
                # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
                # 
                # ===================================================
                # Example usage
                send_message(message_title, message_data)

    time.sleep(wait)
