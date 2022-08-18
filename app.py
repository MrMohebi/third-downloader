from flask import Flask, request
from pySmartDL import SmartDL
from dotenv import load_dotenv
import requests
import os

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


@app.route('/')
def t():
    return "Hi :)"


@app.route('/gapBot', methods=['POST'])
def t():
    return request.form


@app.route('/tel', methods=['GET'])
def getLink():
    link = request.args.get('link')
    dis = "~/pyDL/"
    downloader = SmartDL(link, dis, progress_bar=False)
    downloader.start()
    path = downloader.get_dest()
    urlPart = uploadToGap(path)
    finalUrl = "https://cdn.gaplication.com/o/" + urlPart
    # remove file from server
    os.remove(path)
    sendLinkTelegram(finalUrl)
    return finalUrl


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
