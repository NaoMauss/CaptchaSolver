from telethon import TelegramClient, events
import requests
import json

url = "https://ocr.captchaai.com/solve.php"

payload = {'key': '07d69d230e008d713d077d6831d72bef',
           'numeric': '4',
           'json': '1',
           'calc': '0'}
files = [
    ('file', ('file', open('./12.jpg', 'rb'), 'application/octet-stream'))
]
headers = {}

# api_id and api_hash from https://my.telegram.org/apps
api_id = 10495395
api_hash = 'f472cc916a0e365d26803bc082576463'

client = TelegramClient('user', api_id, api_hash).start()

# This message can contain any text, links, and emoji:
message = "Hello! My name is Nao"


@client.on(events.NewMessage())
async def handler(event):
    sender = await event.get_input_sender()
  # file="11.jpg" is attached image, its optional parameter
    # await client.send_message(sender, message)

# Read all messages from the chat
# and print them to the console


@client.on(events.NewMessage())
async def handler(event):
    print(event.raw_text)

# Download all media from the chat
# and save them to the current directory


@client.on(events.NewMessage())
async def handler(event):
    if event.media:
        await client.download_media(event.message, file="./12.jpg")
        postresponse = requests.request(
            "POST", url, headers=headers, data=payload, files=files)
        print(postresponse.text)
        json_dict = json.loads(postresponse.text)
        await client.send_message(event.chat_id, json_dict['request'])


client.run_until_disconnected()
