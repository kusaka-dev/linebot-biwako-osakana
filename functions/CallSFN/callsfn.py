import json
import os
from types import BuiltinMethodType
import datetime
import base64
import hashlib
import hmac
import boto3
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

client = boto3.client('stepfunctions')

# 環境変数を取得
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
statemachine_arn = os.getenv('STATEMACHINE_ARN')

def lambda_handler(event, context):
    body = event["body"]
    signature = event["headers"]["x-line-signature"]
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    if signature != base64.b64encode(hash).decode():
        return {
            "statusCode": 401,
            "body": 'Unauthorized'
        }

    now = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    jsonbody = json.loads(body)
    print(jsonbody)
    imageid = jsonbody["events"][0]["message"]["id"]
    replytoken = jsonbody["events"][0]["replyToken"]
    print(replytoken)
    user_id = jsonbody["events"][0]["source"]["userId"]
    type = jsonbody["events"][0]["message"]["type"]
    if type == "image":
        client.start_execution(
            stateMachineArn=statemachine_arn,
            name="job-" + str(now),
            input=json.dumps({
                "imageid": imageid,
                "replytoken": replytoken,
                "user_id": user_id
            })
        )
    # きたメッセージが画像以外の場合、ステートマシンは実行せず、「判定したい魚の写真を送ってください」と返信して終了。
    else:
        line_bot_api.reply_message(replytoken,TextSendMessage(text='判定したい魚の写真を送ってください'))
    return {'body': 'ok'}