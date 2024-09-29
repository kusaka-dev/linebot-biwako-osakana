import os
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

# 環境変数を取得
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

def lambda_handler(event, context):
    replytoken = event["replytoken"]
    print(replytoken)
    line_bot_api.push_message(replytoken,TextSendMessage(imagename))
    return {
        "bucketname": s3_bucket_name,
        "imagename": str(imageid) + ".png",
        "user_id": user_id
    }