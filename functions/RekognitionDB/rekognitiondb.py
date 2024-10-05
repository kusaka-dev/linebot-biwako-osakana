import os
import boto3

# 環境変数を取得
project_arn = os.getenv('PROJECT_ARN')
table_name = os.getenv('TABLE_NAME')

rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    bucketname = event["bucketname"]
    print(bucketname)
    imagename = event["imagename"]
    print(imagename)

    response = rekognition.detect_custom_labels(
        ProjectVersionArn=project_arn,
        Image={'S3Object': {'Bucket': event["bucketname"],'Name': event["imagename"]}},
    )
    user_id = event["user_id"]

    print(response)

    if not response["CustomLabels"]:
        message = "この写真ではうまく判定できませんでした・・・。"

    else:
        resultname = response['CustomLabels'][0]['Name']
        resultpercent = response['CustomLabels'][0]['Confidence']
        user_id = event["user_id"]

        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                "FishName": {"S": resultname}
            }
        )
        item = response["Item"]
        per = round(resultpercent, 2)
        features = item["features"]["S"]

        message = '''**判定結果**\n名前 : {0} \n信頼度 : {1}%\n特徴 : {2}'''.format(resultname, str(per), futures)
        print(message)
    return {
        "user_id": user_id,
        "message": message
    }