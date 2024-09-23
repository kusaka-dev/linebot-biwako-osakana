import os
import logging
import tempfile
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

s3 = boto3.resource('s3')
# 環境変数を取得
backet_name = os.getenv('BUCKET_NAME')
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

    # with tempfile.TemporaryFile() as tmp:
    #     for chunk in image.iter_content():
    #         tmp.write(chunk)
    #     tmp.seek(0)
    #
    # bucket = s3.Bucket(backet_name)
    # bucket.put_object(
    #         Body=tmp,
    #         Key=f'{imageid}.png'
    #     )
    line_bot_api.reply_message(
            replytoken,
            TextSendMessage(text='アップロードに成功しました')
        )
    return {
        "bucketname": backet_name,
        "imagename": str(imageid) + ".png",
        "user_id": user_id
    }