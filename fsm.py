from transitions.extensions import GraphMachine
import os
from linebot import LineBotApi, WebhookParser
from linebot.models import *

from utils import send_text_message
from utils import send_button_message

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_wanteat(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "start"

    def is_going_to_breakfast(self, event):
        text = event.message.text
        return text.lower() == "breakfast"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to state3"

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")

        # reply_token = event.reply_token
        # btn = [
        #     {
        #         "type": "postback",
        #         "title": "早餐",
        #         "playload": "breakfast"
        #     },
        #     {
        #         "type": "postback",
        #         "title": "午餐",
        #         "playload": "lunch"
        #     },
        #     {
        #         "type": "postback",
        #         "title": "晚餐",
        #         "playload": "dinner"
        #     },
        #     {
        #         "type": "postback",
        #         "title": "宵夜",
        #         "playload": "midnight"
        #     },
        # ]
        # send_button_message(reply_token, "想吃什麼呢？", btn)
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='早餐',
                        text='breakfast'
                    ),
                    MessageTemplateAction(
                        label='午餐',
                        text='lunch'
                    ),
                    MessageTemplateAction(
                        label='晚餐',
                        text='dinner'
                    ),
                    MessageTemplateAction(
                        label='宵夜',
                        text='midnight'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        #self.go_back()

    def on_exit_wanteat(self):
        print("I'm exit wanteat")

    def on_enter_breakfast(self, event):
        print("I'm entering breakfast")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger ON breakfast")
        self.go_back()

    def on_exit_breakfast(self):
        print("Leaving breakfast")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")


        