from telethon import TelegramClient, events
import requests
import json
import base64

url = "https://ocr.captchaai.com/solve.php"
encoded_string = ''
image_name = 'data:image/jpeg;base64,' + encoded_string


i = 0

filename = './12' + str(i) + '.jpg'

files = [
    ('file', ('file', open(filename, 'rb'), 'application/octet-stream'))
]

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
    global i
    global encoded_string
    global payload
    global filename
    global image_name

    if event.media:

        await client.download_media(event.message, file=filename)
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode('utf-8')
        image_name = 'data:image/jpeg;base64,' + encoded_string
        payload = {'key': '07d69d230e008d713d077d6831d72bef',
                   'json': '0',
                   'calc': '0',
                   'method': 'base64',
                   'body': image_name, }
        postresponse = requests.request(
            "POST", url, data=payload)
        print(postresponse.text)
        captcha_solve = postresponse.text.replace(postresponse.text[:3], "", 1)
        print(captcha_solve)
        await client.send_message(event.chat_id, captcha_solve)

        i += 1

client.run_until_disconnected()
