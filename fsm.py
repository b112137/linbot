from transitions.extensions import GraphMachine
import os
from linebot import LineBotApi, WebhookParser
from linebot.models import TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, MessageTemplateAction, ButtonsTemplate, ConfirmTemplate, TextSendMessage, ImageSendMessage

from utils import send_text_message

import random
from map_search import search_message, search_photo, search_address
from get_time import get_time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("./auth.json", scope)
client = gspread.authorize(creds)

spreadsheet_key = "15X-GEDSNyUfA_5JFOkh4LjTdIBeq-rBrEdJ2GPVYGl8"
sheet = client.open_by_key(spreadsheet_key).sheet1
sheet2 = client.open_by_key(spreadsheet_key).get_worksheet(1)
sheet3 = client.open_by_key(spreadsheet_key).get_worksheet(2)

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_access_token = str(channel_access_token)
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
want_add_text = ""
want_delete_text = ""
wand_search_text = ""
feedback_text = ""
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_feature(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "start" or text.lower() == "返回主選單"

    def on_enter_feature(self, event):
        print("I'm entering feature")
        global sheet2, multi_user_id, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight, multi_user_randold,multi_user_store_choosed
        
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
            if(sheet_dic[i]["user_id"] == "global" or sheet_dic[i]["user_id"] == user_id):
                if(sheet_dic[i]["breakfast"] != 0):
                    multi_user_breakfast[multi_user_id.index(user_id)].append(sheet_dic[i]["breakfast"])
                if(sheet_dic[i]["lunch"] != 0):
                    multi_user_lunch[multi_user_id.index(user_id)].append(sheet_dic[i]["lunch"])
                if(sheet_dic[i]["dinner"] != 0):
                    multi_user_dinner[multi_user_id.index(user_id)].append(sheet_dic[i]["dinner"])
                if(sheet_dic[i]["midnight"] != 0):
                    multi_user_midnight[multi_user_id.index(user_id)].append(sheet_dic[i]["midnight"])

        message = TemplateSendMessage(
            alt_text='主選單',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/12/04/JYzZ4L.jpg',
                        action=MessageTemplateAction(
                            label="想吃吃！",
                            text='想吃吃！',
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/12/04/lnmCyx.jpg',
                        action=MessageTemplateAction(
                            label='查詢店家資訊！',
                            text='查詢店家資訊！',
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/12/04/Cleb52.jpg',
                        action=MessageTemplateAction(
                            label='新增/刪除店家列表',
                            text='新增/刪除店家列表',
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/12/10/1GH3X4.jpg',
                        action=MessageTemplateAction(
                            label='意見回饋！',
                            text='意見回饋！',
                        )
                    )
                ]
            ) 
        )
        sheet2.append_row([event.source.user_id, get_time(), 0, "回到主選單", self.state])
        line_bot_api.push_message(user_id, message)

    def is_going_to_wanteat(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "想吃吃！"

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")
        global multi_user_id, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight, multi_user_randold,multi_user_store_choosed

        user_id = event.source.user_id

        multi_user_store_choosed[multi_user_id.index(user_id)] = ""
        multi_user_randold[multi_user_id.index(user_id)] = [-1]
        message = TemplateSendMessage(
            alt_text='想吃什麼呢？',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2019/12/04/1a53yH.jpg',
                title='想吃什麼呢？',
                text='點選後將隨機推薦店家！',
                actions=[
                    MessageTemplateAction(
                        label='早餐',
                        text='吃早餐！'
                    ),
                    MessageTemplateAction(
                        label='午餐',
                        text='吃午餐！'
                    ),
                    MessageTemplateAction(
                        label='晚餐',
                        text='吃晚餐！'
                    ),
                    MessageTemplateAction(
                        label='宵夜',
                        text='吃宵夜！'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    def is_going_to_breakfast(self, event):
        text = event.message.text
        return text.lower() == "吃早餐！" or text.lower() == "換一家！"

    def on_enter_breakfast(self, event):
        print("I'm entering breakfast")
        global sheet2, rand, multi_user_randold, multi_user_store_choosed

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
        store_address = search_address(multi_user_store_choosed[multi_user_id.index(user_id)])
        # reply_token = event.reply_token
        sheet2.append_row([event.source.user_id, get_time(), 0, multi_user_store_choosed[multi_user_id.index(user_id)],self.state])
        message = TemplateSendMessage(
            alt_text=multi_user_store_choosed[multi_user_id.index(user_id)],
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
                text = store_address,
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
        return text.lower() == "吃午餐！" or text.lower() == "換一家！"

    def on_enter_lunch(self, event):
        print("I'm entering lunch")
        global sheet2, rand, multi_user_randold, multi_user_store_choosed
        
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
        store_address = search_address(multi_user_store_choosed[multi_user_id.index(user_id)])
        sheet2.append_row([event.source.user_id, get_time(), 0, multi_user_store_choosed[multi_user_id.index(user_id)],self.state])
        message = TemplateSendMessage(
            alt_text=multi_user_store_choosed[multi_user_id.index(user_id)],
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
                text = store_address,
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
        return text.lower() == "吃晚餐！" or text.lower() == "換一家！"

    def on_enter_dinner(self, event):
        print("I'm entering dinner")
        global sheet2, rand, multi_user_randold, multi_user_store_choosed
        
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
        store_address = search_address(multi_user_store_choosed[multi_user_id.index(user_id)])
        sheet2.append_row([event.source.user_id, get_time(), 0, multi_user_store_choosed[multi_user_id.index(user_id)],self.state])
        message = TemplateSendMessage(
            alt_text=multi_user_store_choosed[multi_user_id.index(user_id)],
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
                text = store_address,
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
        return text.lower() == "吃宵夜！" or text.lower() == "換一家！"

    def on_enter_midnight(self, event):
        print("I'm entering midnight")
        global sheet2, rand, multi_user_randold, multi_user_store_choosed
        
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
        store_address = search_address(multi_user_store_choosed[multi_user_id.index(user_id)])
        sheet2.append_row([event.source.user_id, get_time(), 0, multi_user_store_choosed[multi_user_id.index(user_id)],self.state])
        message = TemplateSendMessage(
            alt_text=multi_user_store_choosed[multi_user_id.index(user_id)],
            template=ButtonsTemplate(
                thumbnail_image_url = store_photo,
                title = multi_user_store_choosed[multi_user_id.index(user_id)],
                text = store_address,
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
        self.go_back(event)
    
    def is_going_to_arrange_store(self, event):
        text = event.message.text
        return text.lower() == "新增/刪除店家列表"

    def on_enter_arrange_store(self, event):
        print("I'm entering arrange_store")
    
        message = TemplateSendMessage(
            alt_text='請選擇欲新增/刪除的店家分類',
            template=ButtonsTemplate(
                #thumbnail_image_url = store_photo,
                title = "請選擇欲新增/刪除的店家分類",
                text='點選後將顯示店家列表',
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

        sheet_dic = sheet.get_all_records()
        if(arrange_type == 1):
            message = message + "你的早餐店家列表如下：\n"
            for i in range(0,len(multi_user_breakfast[multi_user_id.index(user_id)])):
                global_check = 1
                for j in range(0,len(sheet_dic)):
                    if(sheet_dic[j]["user_id"] == user_id):
                        if(sheet_dic[j]["breakfast"] == multi_user_breakfast[multi_user_id.index(user_id)][i]):
                            message = message + multi_user_breakfast[multi_user_id.index(user_id)][i] + "[自訂]\n"
                            global_check = 0
                            break
                if(global_check == 1):
                    message = message + multi_user_breakfast[multi_user_id.index(user_id)][i] + "\n"
        elif(arrange_type == 2):
            message = message + "你的午餐店家列表如下：\n"
            for i in range(0,len(multi_user_lunch[multi_user_id.index(user_id)])):
                global_check = 1
                for j in range(0,len(sheet_dic)):
                    if(sheet_dic[j]["user_id"] == user_id):
                        if(sheet_dic[j]["lunch"] == multi_user_lunch[multi_user_id.index(user_id)][i]):
                            message = message + multi_user_lunch[multi_user_id.index(user_id)][i] + "[自訂]\n"
                            global_check = 0
                            break
                if(global_check == 1):
                    message = message + multi_user_lunch[multi_user_id.index(user_id)][i] + "\n"
        elif(arrange_type == 3):
            message = message + "你的晚餐店家列表如下：\n"
            for i in range(0,len(multi_user_dinner[multi_user_id.index(user_id)])):
                global_check = 1
                for j in range(0,len(sheet_dic)):
                    if(sheet_dic[j]["user_id"] == user_id):
                        if(sheet_dic[j]["dinner"] == multi_user_dinner[multi_user_id.index(user_id)][i]):
                            message = message + multi_user_dinner[multi_user_id.index(user_id)][i] + "[自訂]\n"
                            global_check = 0
                            break
                if(global_check == 1):
                    message = message + multi_user_dinner[multi_user_id.index(user_id)][i] + "\n"
        elif(arrange_type == 4):
            message = message + "你的宵夜店家列表如下：\n"
            for i in range(0,len(multi_user_midnight[multi_user_id.index(user_id)])):
                global_check = 1
                for j in range(0,len(sheet_dic)):
                    if(sheet_dic[j]["user_id"] == user_id):
                        if(sheet_dic[j]["midnight"] == multi_user_midnight[multi_user_id.index(user_id)][i]):
                            message = message + multi_user_midnight[multi_user_id.index(user_id)][i] + "[自訂]\n"
                            global_check = 0
                            break
                if(global_check == 1):
                    message = message + multi_user_midnight[multi_user_id.index(user_id)][i] + "\n"
        message = message + "\n輸入\"返回主選單\"或點擊下方選單可返回主選單"

        template_message = TemplateSendMessage(
            alt_text='新增/刪除店家列表',
            template = ConfirmTemplate(
                title='新增/刪除店家列表',
                text='新增/刪除店家列表',
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
        send_text_message(event.reply_token, message)
        line_bot_api.push_message(user_id, template_message)
        
    def is_going_to_add_store(self, event):
        text = event.message.text
        result = False
        if(text == "新增店家"):
            result = True
        return result

    def on_enter_add_store(self, event):
        global sheet, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight
        print("I'm entering add_store")
        
        user_id = event.source.user_id
        
        multi_user_breakfast[multi_user_id.index(user_id)] = []
        multi_user_lunch[multi_user_id.index(user_id)] = []
        multi_user_dinner[multi_user_id.index(user_id)] = []
        multi_user_midnight[multi_user_id.index(user_id)] = []

        sheet_dic = sheet.get_all_records()
        for i in range(0,len(sheet_dic)):
            if(sheet_dic[i]["user_id"] == "global" or sheet_dic[i]["user_id"] == user_id):
                if(sheet_dic[i]["breakfast"] != 0):
                    multi_user_breakfast[multi_user_id.index(user_id)].append(sheet_dic[i]["breakfast"])
                if(sheet_dic[i]["lunch"] != 0):
                    multi_user_lunch[multi_user_id.index(user_id)].append(sheet_dic[i]["lunch"])
                if(sheet_dic[i]["dinner"] != 0):
                    multi_user_dinner[multi_user_id.index(user_id)].append(sheet_dic[i]["dinner"])
                if(sheet_dic[i]["midnight"] != 0):
                    multi_user_midnight[multi_user_id.index(user_id)].append(sheet_dic[i]["midnight"])

        message = "請輸入店家名稱\n名稱格式：\n\"店名 區域、路名、分店名稱\"\n範例一：麥當勞 台南大學店\n範例二：路易莎 台南勝利路\n範例三：職人雙饗丼 育樂街\n\n輸入\"返回主選單\"或點擊下方選單可返回主選單"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        
    def is_going_to_add_condition(self, event):
        global want_add_text
        want_add_text = event.message.text
        result = True
        return result

    def on_enter_add_condition(self, event):
        global sheet2
        print("I'm entering add_store")

        user_id = event.source.user_id
        add_check = 0

        if(arrange_type == 1):
            for i in range(0,len(multi_user_breakfast[multi_user_id.index(user_id)])):
                if(want_add_text == multi_user_breakfast[multi_user_id.index(user_id)][i]):
                    add_check = 1
        elif(arrange_type == 2):
            for i in range(0,len(multi_user_lunch[multi_user_id.index(user_id)])):
                if(want_add_text == multi_user_lunch[multi_user_id.index(user_id)][i]):
                    add_check = 1
        elif(arrange_type == 3):
            for i in range(0,len(multi_user_dinner[multi_user_id.index(user_id)])):
                if(want_add_text == multi_user_dinner[multi_user_id.index(user_id)][i]):
                    add_check = 1
        elif(arrange_type == 4):
            for i in range(0,len(multi_user_midnight[multi_user_id.index(user_id)])):
                if(want_add_text == multi_user_midnight[multi_user_id.index(user_id)][i]):
                    add_check = 1

        if(add_check == 1):
            message = "此店家已存在列表內，請重新輸入！"
            sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)
        else:
            message = search_message(want_add_text)
            if(message == "Not Found"):
                message = "找不到此店家，請重新輸入！"
                sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
                send_text_message(event.reply_token, message)
                self.go_back(event)
            else:
                template_message = TemplateSendMessage(
                    alt_text="是否加入\"" + want_add_text + "\"至店家列表？",
                    template = ConfirmTemplate(
                        title= "是否加入\"" + want_add_text + "\"至店家列表？",
                        text="是否加入\"" + want_add_text + "\"至店家列表？(請確認上述店家資訊)",
                        actions=[                              
                            MessageTemplateAction(
                                label='是',
                                text='是',
                            ),
                            MessageTemplateAction(
                                label='否',
                                text='否'
                            )
                        ]
                    )
                )
                send_text_message(event.reply_token, message)
                line_bot_api.push_message(user_id, template_message)

    def is_going_to_add_yes(self, event):
        text = event.message.text
        result = False
        if(text == "是"):
            result = True
        return result

    def on_enter_add_yes(self, event):
        global sheet2
        print("I'm entering add_yes")
        global sheet
        user_id = event.source.user_id
        if(arrange_type == 1):
            add_list = [user_id, want_add_text, 0, 0, 0]
        elif(arrange_type == 2):
            add_list = [user_id, 0, want_add_text, 0, 0]
        elif(arrange_type == 3):
            add_list = [user_id, 0, 0, want_add_text, 0]
        elif(arrange_type == 4):
            add_list = [user_id, 0, 0, 0, want_add_text]
        sheet.append_row(add_list)

        message = "加入完成！"
        sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
        send_text_message(event.reply_token, message)
        self.go_back(event)

    def is_going_to_add_no(self, event):
        text = event.message.text
        result = False
        if(text == "否"):
            result = True
        return result

    def on_enter_add_no(self, event):
        global sheet2
        print("I'm entering add_no")
        message = "加入失敗！"
        sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
        send_text_message(event.reply_token, message)
        self.go_back(event)
    
    def is_going_to_delete_store(self, event):
        global arrange_type
        text = event.message.text
        result = False
        if(text == "刪除店家"):
            result = True
        return result

    def on_enter_delete_store(self, event):
        global sheet, multi_user_breakfast, multi_user_lunch, multi_user_dinner, multi_user_midnight
        print("I'm entering delete_store")

        user_id = event.source.user_id

        multi_user_breakfast[multi_user_id.index(user_id)] = []
        multi_user_lunch[multi_user_id.index(user_id)] = []
        multi_user_dinner[multi_user_id.index(user_id)] = []
        multi_user_midnight[multi_user_id.index(user_id)] = []

        sheet_dic = sheet.get_all_records()
        for i in range(0,len(sheet_dic)):
            if(sheet_dic[i]["user_id"] == "global" or sheet_dic[i]["user_id"] == user_id):
                if(sheet_dic[i]["breakfast"] != 0):
                    multi_user_breakfast[multi_user_id.index(user_id)].append(sheet_dic[i]["breakfast"])
                if(sheet_dic[i]["lunch"] != 0):
                    multi_user_lunch[multi_user_id.index(user_id)].append(sheet_dic[i]["lunch"])
                if(sheet_dic[i]["dinner"] != 0):
                    multi_user_dinner[multi_user_id.index(user_id)].append(sheet_dic[i]["dinner"])
                if(sheet_dic[i]["midnight"] != 0):
                    multi_user_midnight[multi_user_id.index(user_id)].append(sheet_dic[i]["midnight"])

        message = "請輸入完整店家名稱\n(需在以上店家列表內)\n\n輸入\"返回主選單\"或點擊下方選單可返回主選單"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
    
    def is_going_to_delete_condition(self, event):
        global want_delete_text
        want_delete_text = event.message.text
        result = True
        return result

    def on_enter_delete_condition(self, event):
        print("I'm entering delete_condition")
        global sheet

        user_id = event.source.user_id
        delete_index = -1
        delete_check = 0

        sheet_dic = sheet.get_all_records()
        if(arrange_type == 1):
            for i in range(0,len(sheet_dic)):
                if(sheet_dic[i]["user_id"] == user_id):
                    if(sheet_dic[i]["breakfast"] == want_delete_text):
                        delete_index = i + 2
                        delete_check = 1
                        break
                elif(sheet_dic[i]["user_id"] == "global"):
                    if(sheet_dic[i]["breakfast"] == want_delete_text):
                        delete_check = 2
                        break
        elif(arrange_type == 2):
            for i in range(0,len(sheet_dic)):
                if(sheet_dic[i]["user_id"] == user_id):
                    if(sheet_dic[i]["lunch"] == want_delete_text):
                        delete_index = i + 2
                        delete_check = 1
                        break
                elif(sheet_dic[i]["user_id"] == "global"):
                    if(sheet_dic[i]["lunch"] == want_delete_text):
                        delete_check = 2
                        break
        elif(arrange_type == 3):
            for i in range(0,len(sheet_dic)):
                if(sheet_dic[i]["user_id"] == user_id):
                    if(sheet_dic[i]["dinner"] == want_delete_text):
                        delete_index = i + 2
                        delete_check = 1
                        break
                elif(sheet_dic[i]["user_id"] == "global"):
                    if(sheet_dic[i]["dinner"] == want_delete_text):
                        delete_check = 2
                        break
        elif(arrange_type == 4):
            for i in range(0,len(sheet_dic)):
                if(sheet_dic[i]["user_id"] == user_id):
                    if(sheet_dic[i]["midnight"] == want_delete_text):
                        delete_index = i + 2
                        delete_check = 1
                        break
                elif(sheet_dic[i]["user_id"] == "global"):
                    if(sheet_dic[i]["midnight"] == want_delete_text):
                        delete_check = 2
                        break
        
        if(delete_check == 1):
            sheet.update_cell(delete_index, 1, "delete")
            message = "刪除完成！"
            sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)
        elif(delete_check == 0):
            message = "列表內無此店家，請重新輸入！"
            sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)
        elif(delete_check == 2):
            message = "此店家為系統預設店家故無法刪除，請重新輸入！"
            sheet2.append_row([event.source.user_id, get_time(), 0, message, self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)

    def is_going_to_search_store(self, event):
        text = event.message.text
        return text.lower() == "查詢店家資訊！"

    def on_enter_search_store(self, event):
        print("I'm entering search_store")

        user_id = event.source.user_id

        message = "請輸入店家名稱\n名稱格式：\n\"店名 區域、路名、分店名稱\"\n範例一：麥當勞 台南大學店\n範例二：路易莎 台南勝利路\n範例三：職人雙饗丼 育樂街\n\n輸入\"返回主選單\"或點擊下方選單可返回主選單"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    def is_going_to_search_condition(self, event):
        global wand_search_text
        wand_search_text = event.message.text
        result = True
        return result

    def on_enter_search_condition(self, event):
        global sheet2
        print("I'm entering delete_condition")
        message = search_message(wand_search_text)
        if(message == "Not Found"):
            message = "找不到此店家，請重新輸入！"
            sheet2.append_row([event.source.user_id, get_time(), 0, message,self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)
        else:
            sheet2.append_row([event.source.user_id, get_time(), 0, "result",self.state])
            send_text_message(event.reply_token, message)
            self.go_back(event)

    def is_going_to_feedback(self, event):
        text = event.message.text
        return text.lower() == "意見回饋！"

    def on_enter_feedback(self, event):
        print("I'm entering feedback")
        user_id = event.source.user_id

        message = "你有什麼意見ㄇ？\n\n輸入\"返回主選單\"或點擊下方選單可返回主選單"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))

    def is_going_to_feedback_condition(self, event):
        global feedback_text
        feedback_text = event.message.text
        return True

    def on_enter_feedback_condition(self, event):
        global sheet3
        print("I'm entering feedback_condition")
        user_id = event.source.user_id
        sheet3.append_row([event.source.user_id, get_time(), feedback_text])
        message = "郭收到你寶貴的意見囉！"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        self.go_back(event)
    
    def is_going_to_draw_fsm(self, event):
        text = event.message.text
        return text.lower() == "fsm"

    def on_enter_draw_fsm(self, event):
        print("I'm entering draw_fsm")
        user_id = event.source.user_id
        message = ImageSendMessage(
            original_content_url='https://upload.cc/i1/2019/12/09/G92Dx5.png',
            preview_image_url='https://upload.cc/i1/2019/12/09/G92Dx5.png'
        )
        line_bot_api.push_message(user_id, message)
        self.go_back(event)