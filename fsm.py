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

multi_user_id = []
multi_user_breakfast = []
multi_user_lunch = []
multi_user_dinner = []
multi_user_midnight = []

multi_user_store_choosed = []
multi_user_randold = []
rand = -1
arrange_type = -1

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_feature(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "start"

    def on_enter_feature(self, event):
        print("I'm entering feature")
        global store_choosed, randold, multi_user_id, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight, multi_user_randold,multi_user_store_choosed
        
        check_exist = 0
        user_id = event.source.user_id
        for id in multi_user_id:
            if user_id == id:
                check_exist = 1
                break
        if(check_exist == 0):
            multi_user_id.append(user_id)
            multi_user_breakfast.append([])
            multi_user_lunch.append([])
            multi_user_dinner.append([])
            multi_user_midnight.append([])
            multi_user_randold.append([-1])
            multi_user_store_choosed.append("")

        multi_user_breakfast[multi_user_id.index(user_id)] = []
        multi_user_lunch[multi_user_id.index(user_id)] = []
        multi_user_dinner[multi_user_id.index(user_id)] = []
        multi_user_midnight[multi_user_id.index(user_id)] = []

        sheet_dic = sheet.get_all_records()
        for i in range(0,len(sheet_dic)):
            if(sheet_dic[i]["user_id"] == "global"):
                if(sheet_dic[i]["breakfast"] != 0):
                    multi_user_breakfast[multi_user_id.index(user_id)].append(sheet_dic[i]["breakfast"])
                if(sheet_dic[i]["lunch"] != 0):
                    multi_user_lunch[multi_user_id.index(user_id)].append(sheet_dic[i]["lunch"])
                if(sheet_dic[i]["dinner"] != 0):
                    multi_user_dinner[multi_user_id.index(user_id)].append(sheet_dic[i]["dinner"])
                if(sheet_dic[i]["midnight"] != 0):
                    multi_user_midnight[multi_user_id.index(user_id)].append(sheet_dic[i]["midnight"])

        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=TemplateSendMessage(
                alt_text='目錄 template',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://example.com/image.jpg',
                            action=PostbackTemplateAction(
                                label="想吃吃！",
                                text='想吃吃！',
                                #data='action=buy&itemid=1'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://example.com/image.jpg',
                            action=PostbackTemplateAction(
                                label='新增/刪除店家列表',
                                text='新增/刪除店家列表',
                                #data='action=buy&itemid=2'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://example.com/image.jpg',
                            action=PostbackTemplateAction(
                                label='查詢店家資訊！',
                                text='查詢店家資訊！',
                                #data='action=buy&itemid=2'
                            )
                        )
                    ]
                )
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        
    def is_going_to_wanteat(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "start"

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")
        global store_choosed, randold, multi_user_id, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight, multi_user_randold,multi_user_store_choosed

        multi_user_store_choosed[multi_user_id.index(user_id)] = ""
        multi_user_randold[multi_user_id.index(user_id)] = [-1]
        
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
        global rand, multi_user_randold, multi_user_store_choosed

        user_id = event.source.user_id

        rand_repeat = 1
        while(rand_repeat):
            if(len(multi_user_randold[multi_user_id.index(user_id)]) > len(multi_user_breakfast[multi_user_id.index(user_id)])):
                multi_user_randold[multi_user_id.index(user_id)] = [-1]
            rand = random.randint(0,len(multi_user_breakfast[multi_user_id.index(user_id)])-1)
            for i in range(0,len(multi_user_randold[multi_user_id.index(user_id)])):
                if(rand == multi_user_randold[multi_user_id.index(user_id)][i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        multi_user_randold[multi_user_id.index(user_id)].append(rand)
        multi_user_store_choosed[multi_user_id.index(user_id)] = multi_user_breakfast[multi_user_id.index(user_id)][rand]
        store_photo = search_photo(multi_user_store_choosed[multi_user_id.index(user_id)])
        # reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
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
        global rand, multi_user_randold, multi_user_store_choosed
        
        user_id = event.source.user_id

        rand_repeat = 1
        while(rand_repeat):
            if(len(multi_user_randold[multi_user_id.index(user_id)]) > len(multi_user_lunch[multi_user_id.index(user_id)])):
                multi_user_randold[multi_user_id.index(user_id)] = [-1]
            rand = random.randint(0,len(multi_user_lunch[multi_user_id.index(user_id)])-1)
            for i in range(0,len(multi_user_randold[multi_user_id.index(user_id)])):
                if(rand == multi_user_randold[multi_user_id.index(user_id)][i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        multi_user_randold[multi_user_id.index(user_id)].append(rand)
        multi_user_store_choosed[multi_user_id.index(user_id)] = multi_user_lunch[multi_user_id.index(user_id)][rand]
        store_photo = search_photo(multi_user_store_choosed[multi_user_id.index(user_id)])

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
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
        global rand, multi_user_randold, multi_user_store_choosed
        
        user_id = event.source.user_id

        rand_repeat = 1
        while(rand_repeat):
            if(len(multi_user_randold[multi_user_id.index(user_id)]) > len(multi_user_dinner[multi_user_id.index(user_id)])):
                multi_user_randold[multi_user_id.index(user_id)] = [-1]
            rand = random.randint(0,len(multi_user_dinner[multi_user_id.index(user_id)])-1)
            for i in range(0,len(multi_user_randold[multi_user_id.index(user_id)])):
                if(rand == multi_user_randold[multi_user_id.index(user_id)][i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        multi_user_randold[multi_user_id.index(user_id)].append(rand)
        multi_user_store_choosed[multi_user_id.index(user_id)] = multi_user_dinner[multi_user_id.index(user_id)][rand]
        store_photo = search_photo(multi_user_store_choosed[multi_user_id.index(user_id)])

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
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
        global rand, multi_user_randold, multi_user_store_choosed
        
        user_id = event.source.user_id

        rand_repeat = 1
        while(rand_repeat):
            if(len(multi_user_randold[multi_user_id.index(user_id)]) > len(multi_user_midnight[multi_user_id.index(user_id)])):
                multi_user_randold[multi_user_id.index(user_id)] = [-1]
            rand = random.randint(0,len(multi_user_midnight[multi_user_id.index(user_id)])-1)
            for i in range(0,len(multi_user_randold[multi_user_id.index(user_id)])):
                if(rand == multi_user_randold[multi_user_id.index(user_id)][i]):
                    rand_repeat = 1
                    break
                else:
                    rand_repeat = 0
        multi_user_randold[multi_user_id.index(user_id)].append(rand)
        multi_user_store_choosed[multi_user_id.index(user_id)] = multi_user_midnight[multi_user_id.index(user_id)][rand]
        store_photo = search_photo(multi_user_store_choosed[multi_user_id.index(user_id)])

        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
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
        global multi_user_store_choosed

        user_id = event.source.user_id

        print(multi_user_store_choosed[multi_user_id.index(user_id)])
        reply_token = event.reply_token

        message = search_message(multi_user_store_choosed[multi_user_id.index(user_id)])

        send_text_message(reply_token, message)
        self.go_back()
    
    def is_going_to_arrange_store(self, event):
        text = event.message.text
        return text.lower() == "新增/刪除店家列表"

    def on_enter_arrange_store(self, event):
        print("I'm entering arrange_store")
    
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                #thumbnail_image_url = store_photo,
                title = "請選擇欲新增/刪除的店家分類",
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='早餐',
                        text='早餐'
                    ),
                    MessageTemplateAction(
                        label='午餐',
                        text='午餐'
                    ),
                    MessageTemplateAction(
                        label='晚餐',
                        text='晚餐'
                    ),
                    MessageTemplateAction(
                        label='宵夜',
                        text='宵夜'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_arrange_type(self, event):
        global arrange_type
        text = event.message.text
        result = False
        if(text.lower() == "早餐"):
            arrange_type = 1
            result = True
        elif(text.lower() == "午餐"):
            arrange_type = 2
            result = True
        elif(text.lower() == "晚餐"):
            arrange_type = 3
            result = True
        elif(text.lower() == "宵夜"):
            arrange_type = 4
            result = True
        return result

    def on_enter_arrange_type(self, event):
        print("I'm entering arrange_type")

        user_id = event.source.user_id
        message = ""

        if(arrange_type == 1):
            message = message + "你的早餐店家列表如下：\n"
            for store in multi_user_breakfast[multi_user_id.index(user_id)]:
                message = message + store + "\n"
        elif(arrange_type == 2):
            message = message + "你的午餐店家列表如下：\n"
            for store in multi_user_lunch[multi_user_id.index(user_id)]:
                message = message + store + "\n"
        elif(arrange_type == 3):
            message = message + "你的晚餐店家列表如下：\n"
            for store in multi_user_dinner[multi_user_id.index(user_id)]:
                message = message + store + "\n"
        elif(arrange_type == 4):
            message = message + "你的宵夜店家列表如下：\n"
            for store in multi_user_midnight[multi_user_id.index(user_id)]:
                message = message + store + "\n"

        template_message = TemplateSendMessage(
            alt_text='目錄 template',
            template = ConfirmTemplate(
                title='新增/刪除店家列表',
                text='Please select',
                actions=[                              
                    MessageTemplateAction(
                        label='新增店家',
                        text='新增店家',
                    ),
                    MessageTemplateAction(
                        label='刪除店家',
                        text='刪除店家'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(user_id, template_message)
        
        
        
