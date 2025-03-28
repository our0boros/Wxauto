from flask import Flask, request, jsonify
import os
import json
import base64
from datetime import datetime
import requests
from googletrans import Translator
# 初始化谷歌翻译器
translator = Translator()

# Initialize Flask app
app = Flask(__name__)

# Define a folder to save the files
FILES_FOLDER = 'files'

# Ensure the files directory exists
if not os.path.exists(os.path.join(os.getcwd(), FILES_FOLDER)):
    os.makedirs(FILES_FOLDER)

@app.route('/receive_message', methods=['POST'])
def receive_message():
    try:
        # Get the JSON data from the incoming POST request
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No JSON data received!"}), 400
        
        # Extract the message and recipient
        message = data.get('message')
        recipient = data.get('recipient')
        is_image = data.get('is_image', False)
        title = data.get('title')

        # 替换 title 中的时间为接收端时间，保留发信人，屏蔽 [Time] 和 [Recall]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if title:
            sender = title.split(']')[0] + ']'  # 提取发信人部分，如 [发信人]
            # 移除 [Time][xxxx] 和 [Recall][xxxx]
            if '[Time]' in title or '[Recall]' in title:
                print(f"Message ignored: {title}")
                return jsonify({"status": "ignored", "message": "Time or Recall message ignored!"}), 200
            title = f"[{sender}][{current_time}]"

        # Process the message
        if is_image:
            # Handle image messages (base64 encoded)
            image_data = base64.b64decode(message)

            # Generate a unique filename using the current timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_name = f"{timestamp}.jpg"  # You can change the extension based on the image type

            # Combine the current working directory with the files folder and the new filename
            file_path = os.path.join(os.getcwd(), FILES_FOLDER, file_name)

            # Save the image to the disk
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)

            print(f"Image saved at {file_path}")

            # Send the image to Discord or process further if needed
            send_to_discord(file_path, title)

        else:
            # If the message is text, just print it and forward it to Discord
            print(f"Received message from {recipient}: {message}")
            send_to_discord(message, title)

        return jsonify({"status": "success", "message": "Message received!"}), 200
    except Exception as e:
        # Catch any unexpected errors and return a response
        print(f"Error occurred: {e}")
        return jsonify({"status": "error", "message": "An error occurred while processing the request!"}), 500


def send_to_discord(content, title=None):
    # Your Discord webhook URL
    webhook_url = 'https://discord.com/api/webhooks/1347799415250751548/94qMyrXSM2ZC0YsJ28n2diLEJcXCA75q5V33FogiArlBC0t6XSk-8bpWqAYUFnpKNruE'
    # 使用 await 调用翻译接口，翻译消息内容为英文
    translation = translator.translate(content, dest='en')
    content = translation.text

    # Prepare the data dictionary for the payload (this can be text or an embed message)
    data = {
        'payload_json': json.dumps({
            'content': content,
            'username': title,
        })
    }

    # If the content is a file path (image), we attach it
    if isinstance(content, str) and os.path.exists(content):  # If content is a file path (image)
        with open(content, 'rb') as file:
            files = {'file1': file}  # Send as file1, you can use different names for multiple files
            # Send the POST request with the file and the payload_json
            response = requests.post(webhook_url, data=data, files=files)
            files['file1'].close()
    else:
        # Send text-based content if not a file
        response = requests.post(webhook_url, data=data)
    
    if response.status_code == 204:
        print("Message sent to Discord successfully!")
    else:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
