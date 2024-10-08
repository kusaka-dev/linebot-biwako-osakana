import os
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# 環境変数を取得
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

def lambda_handler(event, context):
    line_bot_api.push_message(event["user_id"],TextSendMessage(text=event["message"]))