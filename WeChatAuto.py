import asyncio
from wxauto import WeChat
from googletrans import Translator
import requests

# Discord Webhook URL
# DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1347417671402262528/JGnaeNUYWq5p7JWFMTWL6EHgkbec-kLukPD3eCOmWobNgBSETYAIWtJv2rHSC0ccbBjk"
DISCORD_WEBHOOK_URL = ""

# 定义微信群白名单，只有白名单中的群才处理转发
group_whitelist = ["GameLoop"]

# 初始化谷歌翻译器
translator = Translator()

wx = WeChat()
# 加载更多历史消息
# wx.LoadMoreMessage()
# 获取当前聊天窗口消息
msgs = wx.GetAllMessage()

async def process_messages():
    for msg in msgs:
        # 打印调试信息：消息类型、发送方、内容
        # print(f"{msg.type} {msg.sender} {msg.content}")
        
        # 假设当前群聊消息的 msg.sender 表示群名称，
        # 仅对白名单中的群进行处理（注意：如果群聊消息类型不是 friend/self，请修改判断条件）
        if msg.type in ('friend', 'self'):
            # 使用 await 调用翻译接口，翻译消息内容为英文
            translation = await translator.translate(msg.content, dest='en')
            translated_text = translation.text

            # 输出原文和翻译后的消息（调试信息）
            print(f"[{msg.sender} {msg.time}] 原文：{msg.content}")
            print(f"[{msg.sender} {msg.time}] Translated：{translated_text}")

            # 构造转发到 Discord 的消息内容
            discord_data = {
                "content": f"【群聊】{msg.sender}\n【原文】{msg.content}\n【Translated】{translated_text}"
            }

            # print(discord_data)
            # 若需要实际转发到 Discord，请取消下面代码的注释
            # response = requests.post(DISCORD_WEBHOOK_URL, json=discord_data)
            # if response.status_code != 204:  # Discord 返回 204 表示成功
            #     print(f"转发 Discord 失败，状态码：{response.status_code}")

if __name__ == '__main__':
    asyncio.run(process_messages())
