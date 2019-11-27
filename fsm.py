from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_wanteat(self, event):
        text = event.message.text
        print(text)
        return text.lower() == "START"

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "go to state3"

    def on_enter_wanteat(self, event):
        print("I'm entering wanteat")

        reply_token = event.reply_token
        btn = [
            {
                "type": "postback",
                "title": "早餐",
                "playload": "breakfast"
            },
            {
                "type": "postback",
                "title": "午餐",
                "playload": "lunch"
            },
            {
                "type": "postback",
                "title": "晚餐",
                "playload": "dinner"
            },
            {
                "type": "postback",
                "title": "宵夜",
                "playload": "midnight"
            },
        ]
        send_button_message(reply_token, "想吃什麼呢？", btn)
        self.go_back()

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger ONON state1")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

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


        