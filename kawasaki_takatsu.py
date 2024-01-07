"""
kawasaki takatsu Line Bot
"""

import os
import datetime #曜日取得

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from linebot.exceptions import (
        LineBotApiError, InvalidSignatureError
    )

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
userid = os.getenv('LINE_USER_ID')

success_res = {"statusCode": 200, "body": "Success"}
failed_res = {"statusCode": 500, "body": "Error"}

def lambda_handler(event, context):
    # headers = event["headers"]
    # body = event["body"]

    # # get X-Line-Signature header value
    # signature = headers['x-line-signature']

    # # handle webhook body
    # handler.handle(body, signature)

    message_index = main()
    # print(message_index)
    try:
        line_bot_api.push_message(
        userid,
        TextSendMessage(text=message_index))
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        return failed_res

    return success_res


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """ TextMessage handler """
    input_text = event.message.text
    message_reply = 'まぁまぁ'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message_reply))


# Function to determine if it's the 1st or 3rd Tuesday of the month
def is_special_tuesday(day):
    return day.weekday() == 1 and (1 <= day.day <= 7 or 15 <= day.day <= 21)

# Function to determine the garbage type based on the day of the week
def get_garbage_type(day):
    weekday = day.strftime("%A")
    garbage_schedule = {
        "Monday": "ミックスペーパ",
        "Tuesday": "普通ごみ" + ("、粗大ごみ・小物金属" if is_special_tuesday(day) else ""),
        "Wednesday": "缶・ペット・ビン・電池",
        "Thursday": "プラ容器",
        "Friday": "普通ごみ",
        "Saturday": "",
        "Sunday": ""  # Assuming no garbage collection on Sunday
    }
    return garbage_schedule[weekday]

# Main function to determine the garbage collection and send notification
def main():
    # Get tomorrow's date and day of the week
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    # Determine the garbage type for tomorrow
    garbage_type = get_garbage_type(tomorrow)

    # If there is garbage collection tomorrow, send a LINE notification
    message = ""
    if garbage_type:
        message = f"明日は{garbage_type}のごみ収集日です。"

    return message

    # line_bot_api.push_message(userid,message)
    # return {"statusCode": 200, "body": "OK"}


