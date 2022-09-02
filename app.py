from flask import Flask, request
from pySmartDL import SmartDL
from dotenv import load_dotenv
import requests
import os
import threading
from requests_toolbelt.multipart.encoder import MultipartEncoder

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
    session = requests.Session()
    with open(path, 'rb') as f:
        try:
            m = MultipartEncoder(fields={'file': (path.split("/")[-1], f, 'application/octet-stream'),"composite": "NONE"})
            headers = {'Content-Type': m.content_type}
            print('start to uploading =>'+path, flush=True)
            r = requests.post(getGapUploadUrl(), data=m, headers=headers)
            print('uploaded to gap =>'+path, flush=True)
            data = r.json()
            return data["data"]["SID"]
        except Exception as e:
            print("error in uploading gap =>" + path, flush=True)
            print(e, flush=True)
    session.close()


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
    print("downloaded =>" + link, flush=True)
    print("file =>" + path, flush=True)
    urlPart = uploadToGap(path)
    finalUrl = "https://cdn.gaplication.com/o/" + urlPart
    # remove file from server
    os.remove(path)
    return finalUrl


def downloadAndSendToTel(link):
    finalUrl = getFinalDownloadLink(link)
    sendLinkTelegram(finalUrl)
    return finalUrl


def downloadAndSendToGap(link,chatId):
    finalUrl = getFinalDownloadLink(link)
    gapSendMessage(chatId, finalUrl)
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
        thr = threading.Thread(target=downloadAndSendToGap, args=(data,chatId,), kwargs={})
        thr.start()
        return gapSendMessage(chatId, "Add to list, result will be sent here.")

    return gapSendMessage(chatId, data)


@app.route('/tel', methods=['GET'])
def getLink():
    link = request.args.get('link')
    return downloadAndSendToTel(link)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
