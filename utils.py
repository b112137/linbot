import os
import requests

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(id, text, btn):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    aaa = {
      "recipient": {"id": id},
      "message":{
        "attachment":{
        "type":"template",
        "payload":{
          "template_type":"button",
          "text":text,
          "buttons":btn
        }
      }
    }
  }
    response = requests.post(url, json=aaa)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
