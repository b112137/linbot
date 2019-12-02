from transitions.extensions import GraphMachine
import os
from linebot import LineBotApi, WebhookParser
from linebot.models import *

from utils import send_text_message
from utils import send_button_message

import random
from map_search import search_message, search_photo

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("./auth.json", scope)
client = gspread.authorize(creds)

spreadsheet_key = "15X-GEDSNyUfA_5JFOkh4LjTdIBeq-rBrEdJ2GPVYGl8"
sheet = client.open_by_key(spreadsheet_key).sheet1


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

breakfast_list = []
lunch_list = []
dinner_list = []
midnight_list = []
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
        
        breakfast_list = []
        lunch_list = []
        dinner_list = []
        midnight_list = []

        sheet_dic = sheet.get_all_records()
        for i in range(0,len(sheet_dic)):
            if(sheet_dic[i]["user_id"] == "global"):
                if(sheet_dic[i]["breakfast"] != 0):
                    breakfast_list.append(sheet_dic[i]["breakfast"])
                if(sheet_dic[i]["lunch"] != 0):
                    lunch_list.append(sheet_dic[i]["lunch"])
                if(sheet_dic[i]["dinner"] != 0):
                    dinner_list.append(sheet_dic[i]["dinner"])
                if(sheet_dic[i]["midnight"] != 0):
                    midnight_list.append(sheet_dic[i]["midnight"])

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
            if(len(randold) > len(breakfast_list)):
                randold = [-1]
            rand = random.randint(0,len(breakfast_list)-1)
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = breakfast_list[rand]
        store_photo = search_photo(store_choosed)
        # reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
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
            if(len(randold) > len(lunch_list)):
                randold = [-1]
            rand = random.randint(0,len(lunch_list)-1)
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = lunch_list[rand]
        store_photo = search_photo(store_choosed)

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
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
            if(len(randold) > len(dinner_list)):
                randold = [-1]
            rand = random.randint(0,len(dinner_list)-1)
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = dinner_list[rand]
        store_photo = search_photo(store_choosed)

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
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
            if(len(randold) > len(midnight_list)):
                randold = [-1]
            rand = random.randint(0,len(midnight_list)-1)
            for i in range(0,len(randold)):
                if(rand == randold[i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        randold.append(rand)
        store_choosed = midnight_list[rand]
        store_photo = search_photo(store_choosed)

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
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

        message = search_message(store_choosed)

        send_text_message(reply_token, message)
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


        