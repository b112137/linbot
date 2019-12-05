import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

load_dotenv()

multi_user_id = []
multi_user_machine = []

machine = TocMachine(states=["user",
            "feature",
            "wanteat",
            "breakfast",
            "lunch",
            "dinner",
            "midnight",
            "place",
            "arrange_store",
            "arrange_type",
            "add_store",
            "add_condition",
            "add_yes",
            "add_no",
            "delete_store",
            "delete_condition",
            "search_store",
            "search_condition"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "feature",
                "conditions": "is_going_to_feature",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "breakfast", "lunch", "dinner", "midnight", "arrange_store", "arrange_type", "add_store", "add_condition", "delete_store", "search_store"],
                "dest": "feature",
                "conditions": "is_going_to_feature",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "wanteat",
                "conditions": "is_going_to_wanteat",
            },
            {
                "trigger": "advance",
                "source": ["wanteat","breakfast"],
                "dest": "breakfast",
                "conditions": "is_going_to_breakfast",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "lunch"],
                "dest": "lunch",
                "conditions": "is_going_to_lunch",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "dinner"],
                "dest": "dinner",
                "conditions": "is_going_to_dinner",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "midnight"],
                "dest": "midnight",
                "conditions": "is_going_to_midnight",
            },
            {
                "trigger": "advance",
                "source": ["breakfast", "lunch", "dinner", "midnight"],
                "dest": "place",
                "conditions": "is_going_to_place",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "arrange_store",
                "conditions": "is_going_to_arrange_store",
            },
            {
                "trigger": "advance",
                "source": "arrange_store",
                "dest": "arrange_type",
                "conditions": "is_going_to_arrange_type",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "add_store",
                "conditions": "is_going_to_arrange_type",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "add_store",
                "conditions": "is_going_to_add_store",
            },
            {
                "trigger": "advance",
                "source": "add_store",
                "dest": "add_condition",
                "conditions": "is_going_to_add_condition",
            },
            {
                "trigger": "advance",
                "source": "add_condition",
                "dest": "add_yes",
                "conditions": "is_going_to_add_yes",
            },
            {
                "trigger": "advance",
                "source": "add_condition",
                "dest": "add_no",
                "conditions": "is_going_to_add_no",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "delete_store",
                "conditions": "is_going_to_delete_store",
            },
            {
                "trigger": "advance",
                "source": "delete_store",
                "dest": "delete_condition",
                "conditions": "is_going_to_delete_condition",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "search_store",
                "conditions": "is_going_to_search_store",
            },
            {
                "trigger": "advance",
                "source": "search_store",
                "dest": "search_condition",
                "conditions": "is_going_to_search_condition",
            },
            {
                "trigger": "go_back", 
                "source": ["add_condition","add_yes", "add_no"], 
                "dest": "add_store",
            },
            {
                "trigger": "go_back", 
                "source": "delete_condition", 
                "dest": "delete_store",
            },
            {
                "trigger": "go_back", 
                "source": "search_condition", 
                "dest": "search_store",
            },
            {
                "trigger": "go_back", 
                "source": "place", 
                "dest": "feature",
            },
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
channel_access_token = str(channel_access_token)

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    global multi_user_id, multi_user_machine
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    check_exist = 0
    user_id = events[0].source.user_id
    for id in multi_user_id:
        if user_id == id:
            check_exist = 1
            break
    if(check_exist == 0):
        multi_user_id.append(user_id)
        multi_user_machine.append(TocMachine(states=["user",
            "feature",
            "wanteat",
            "breakfast",
            "lunch",
            "dinner",
            "midnight",
            "place",
            "arrange_store",
            "arrange_type",
            "add_store",
            "add_condition",
            "add_yes",
            "add_no",
            "delete_store",
            "delete_condition",
            "search_store",
            "search_condition"],
        transitions=[
            {
                "trigger": "advance",
                "source": "user",
                "dest": "feature",
                "conditions": "is_going_to_feature",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "breakfast", "lunch", "dinner", "midnight", "arrange_store", "arrange_type", "add_store", "add_condition", "delete_store", "search_store"],
                "dest": "feature",
                "conditions": "is_going_to_feature",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "wanteat",
                "conditions": "is_going_to_wanteat",
            },
            {
                "trigger": "advance",
                "source": ["wanteat","breakfast"],
                "dest": "breakfast",
                "conditions": "is_going_to_breakfast",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "lunch"],
                "dest": "lunch",
                "conditions": "is_going_to_lunch",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "dinner"],
                "dest": "dinner",
                "conditions": "is_going_to_dinner",
            },
            {
                "trigger": "advance",
                "source": ["wanteat", "midnight"],
                "dest": "midnight",
                "conditions": "is_going_to_midnight",
            },
            {
                "trigger": "advance",
                "source": ["breakfast", "lunch", "dinner", "midnight"],
                "dest": "place",
                "conditions": "is_going_to_place",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "arrange_store",
                "conditions": "is_going_to_arrange_store",
            },
            {
                "trigger": "advance",
                "source": "arrange_store",
                "dest": "arrange_type",
                "conditions": "is_going_to_arrange_type",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "add_store",
                "conditions": "is_going_to_arrange_type",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "add_store",
                "conditions": "is_going_to_add_store",
            },
            {
                "trigger": "advance",
                "source": "add_store",
                "dest": "add_condition",
                "conditions": "is_going_to_add_condition",
            },
            {
                "trigger": "advance",
                "source": "add_condition",
                "dest": "add_yes",
                "conditions": "is_going_to_add_yes",
            },
            {
                "trigger": "advance",
                "source": "add_condition",
                "dest": "add_no",
                "conditions": "is_going_to_add_no",
            },
            {
                "trigger": "advance",
                "source": "arrange_type",
                "dest": "delete_store",
                "conditions": "is_going_to_delete_store",
            },
            {
                "trigger": "advance",
                "source": "delete_store",
                "dest": "delete_condition",
                "conditions": "is_going_to_delete_condition",
            },
            {
                "trigger": "advance",
                "source": "feature",
                "dest": "search_store",
                "conditions": "is_going_to_search_store",
            },
            {
                "trigger": "advance",
                "source": "search_store",
                "dest": "search_condition",
                "conditions": "is_going_to_search_condition",
            },
            {
                "trigger": "go_back", 
                "source": ["add_condition","add_yes", "add_no"], 
                "dest": "add_store",
            },
            {
                "trigger": "go_back", 
                "source": "delete_condition", 
                "dest": "delete_store",
            },
            {
                "trigger": "go_back", 
                "source": "search_condition", 
                "dest": "search_store",
            },
            {
                "trigger": "go_back", 
                "source": "place", 
                "dest": "feature",
            },
        ],
        initial="user",
        auto_transitions=False,
        show_conditions=True,))

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {multi_user_machine[multi_user_id.index(user_id)].state}")
        print(f"REQUEST BODY: \n{body}")
        
        response = multi_user_machine[multi_user_id.index(user_id)].advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")
    
    return "OK"

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
