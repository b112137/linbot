from transitions.extensions import GraphMachine
import os
from linebot import LineBotApi, WebhookParser
from linebot.models import *

from utils import send_text_message
from utils import send_button_message

import random
#from map_search import search_message
import googlemaps

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

breakfast_list = ["少爺手作蛋餅 勝利", "元之氣 勝利", "小孩先生 勝利"]
lunch_list = ["菇雞", "麥當勞", "肯德基"]
dinner_list = ["小赤佬", "職人雙饗丼", "肉肉控"]
midnight_list = ["一點刈包", "九年九班", "小上海"]
store_choosed = ""
randold = [-1]
rand = -1

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_wanteat(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "start"

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")
        global store_choosed, randold
        store_choosed = ""
        randold = [-1]
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='想吃什麼呢？',
                text='點選後將隨機推薦店家！',
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
        return text.lower() == "breakfast" or text.lower() == "換一家！"

    def on_enter_breakfast(self, event):
        print("I'm entering breakfast")
        global rand, randold, store_choosed

        rand_repeat = 1
        while(rand_repeat):
            rand = random.randint(0,len(breakfast_list))
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = breakfast_list[rand]
        # reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title = store_choosed,
                text = 'Please select',
                actions=[
                    MessageTemplateAction(
                        label='獲取店家資訊！',
                        text='獲取店家資訊！'
                    ),
                    MessageTemplateAction(
                        label='換一家！',
                        text='換一家！'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        # send_text_message(reply_token, "Trigger breakfast")

    def is_going_to_lunch(self, event):
        text = event.message.text
        return text.lower() == "lunch" or text.lower() == "換一家！"

    def on_enter_lunch(self, event):
        print("I'm entering lunch")
        global rand, randold, store_choosed
        
        rand_repeat = 1
        while(rand_repeat):
            rand = random.randint(0,len(lunch_list))
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = lunch_list[rand]

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title = store_choosed,
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='獲取店家資訊！',
                        text='獲取店家資訊！'
                    ),
                    MessageTemplateAction(
                        label='換一家！',
                        text='換一家！'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_dinner(self, event):
        text = event.message.text
        return text.lower() == "dinner" or text.lower() == "換一家！"

    def on_enter_dinner(self, event):
        print("I'm entering dinner")
        global rand, randold, store_choosed
        
        rand_repeat = 1
        while(rand_repeat):
            rand = random.randint(0,len(dinner_list))
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = dinner_list[rand]

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title = store_choosed,
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='獲取店家資訊！',
                        text='獲取店家資訊！'
                    ),
                    MessageTemplateAction(
                        label='換一家！',
                        text='換一家！'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_midnight(self, event):
        text = event.message.text
        return text.lower() == "midnight" or text.lower() == "換一家！"

    def on_enter_midnight(self, event):
        print("I'm entering midnight")
        global rand, randold, store_choosed
        
        rand_repeat = 1
        while(rand_repeat):
            rand = random.randint(0,len(midnight_list))
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = midnight_list[rand]

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title = store_choosed,
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='獲取店家資訊！',
                        text='獲取店家資訊！'
                    ),
                    MessageTemplateAction(
                        label='換一家！',
                        text='換一家！'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_place(self, event):
        text = event.message.text
        return text.lower() == "獲取店家資訊！"

    def on_enter_place(self, event):
        print("I'm entering place")
        global store_choosed
        print(store_choosed)
        reply_token = event.reply_token

        #message = search_message(store_choosed)

        send_text_message(reply_token, store_choosed)
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


        