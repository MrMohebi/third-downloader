from flask import Flask, request
from pySmartDL import SmartDL
from dotenv import load_dotenv
import requests
import os
import threading

load_dotenv()
app = Flask(__name__)


def getGapUploadUrl():
    url = "https://core.gap.im/v1/upload/sign.json?type=file"
    headers = {'X-VERSION': '4.5.19', "X-Token": os.getenv('GAP_TOKEN')}
    r = requests.get(url=url, headers=headers)
    data = r.json()
    return data["data"]["file"]["url"]


def sendLinkTelegram(link):
    token = os.getenv('TEL_TOKEN')
    chatId = os.getenv('TEL_CHAT_ID')
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    params = {"chat_id": chatId, "text": link}
    r = requests.get(url=url, params=params)


def uploadToGap(path):
    with open(path, 'rb') as f:
        files = {'file': f}
        r = requests.post(getGapUploadUrl(), files=files)
        data = r.json()
        return data["data"]["SID"]


def gapSendMessage(chatId, text):
    url = 'https://api.gap.im/sendMessage'
    header = {'token': os.getenv("GAP_BOT_TOKEN")}
    data = {'chat_id': int(chatId), "type": "text", "data": text}
    x = requests.post(url, data=data, headers=header)
    return x.text


def getFinalDownloadLink(link):
    dis = "~/pyDL/"
    downloader = SmartDL(link, dis, progress_bar=False)
    downloader.start()
    path = downloader.get_dest()
    urlPart = uploadToGap(path)
    finalUrl = "https://cdn.gaplication.com/o/" + urlPart
    # remove file from server
    os.remove(path)
    return finalUrl


def downloadAndSendToTel(link):
    finalUrl = getFinalDownloadLink(link)
    sendLinkTelegram(finalUrl)
    return finalUrl

@app.route('/')
def index():
    return "Hi :)"


@app.route('/gapBot', methods=['POST'])
def gapBot():
    messageType = request.form.get("type")
    chatId = request.form.get("chat_id")
    data = request.form.get("data")

    if messageType == 'text' and data[:4] == 'http':
        thr = threading.Thread(target=downloadAndSendToTel, args=(data,), kwargs={})
        thr.start()
        return gapSendMessage(chatId, "Add to list, result will be sent to Telegram.")

    return gapSendMessage(chatId, data)


@app.route('/tel', methods=['GET'])
def getLink():
    link = request.args.get('link')
    return downloadAndSendToTel(link)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
