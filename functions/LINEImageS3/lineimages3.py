import os
import logging
import tempfile
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

s3_client = boto3.client('s3')
# 環境変数を取得
s3_bucket_name = os.getenv('S3_BUCKET_NAME')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.info('image event')
    imageid = event["imageid"]
    replytoken = event["replytoken"]
    user_id = event["user_id"]
    image = line_bot_api.get_message_content(imageid)
    s3_client.put_object(Bucket=s3_bucket_name, Key=f'{imageid}.png', Body=image.content)
    line_bot_api.reply_message(
            replytoken,
            TextSendMessage(text='アップロードに成功しました')
        )
    return {
        "bucketname": s3_bucket_name,
        "imagename": str(imageid) + ".png",
        "replytoken": replytoken,
        "user_id": user_id
    }