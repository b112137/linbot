#-*- coding: utf-8 -*-
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

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")
        message = TemplateSendMessage(
            alt_text='aaa',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='aaa',
                text='',
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

    def is_going_to_breakfast(self, event):
        text = event.message.text
        return text.lower() == "breakfast"

    def on_enter_breakfast(self, event):
        print("I'm entering breakfast")
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='aaa',
                actions=[
                    MessageTemplateAction(
                        label='get',
                        text='get'
                    ),
                    MessageTemplateAction(
                        label='next',
                        text='next'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        #send_text_message(reply_token, "Trigger breakfast")

    def is_going_to_lunch(self, event):
        text = event.message.text
        return text.lower() == "lunch"

    def on_enter_lunch(self, event):
        print("I'm entering lunch")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger lunch")
        self.go_back()

    def is_going_to_dinner(self, event):
        text = event.message.text
        return text.lower() == "dinner"

    def on_enter_dinner(self, event):
        print("I'm entering dinner")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger dinner")
        self.go_back()

    def is_going_to_midnight(self, event):
        text = event.message.text
        return text.lower() == "midnight"

    def on_enter_midnight(self, event):
        print("I'm entering midnight")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger midnight")
        self.go_back()

    def is_going_to_place(self, event):
        text = event.message.text
        return text.lower() == "get"

    def on_enter_place(self, event):
        print("I'm entering place")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger place")
        self.go_back()
    

    












    # def on_enter_state2(self, event):
    #     print("I'm entering state2")

    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "Trigger state2")
    #     self.go_back()

    # def on_exit_state2(self):
    #     print("Leaving state2")

    # def on_enter_state3(self, event):
    #     print("I'm entering state3")

    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "Trigger state3")
    #     self.go_back()

    # def on_exit_state3(self):
    #     print("Leaving state3")


        