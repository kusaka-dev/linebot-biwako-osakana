def lambda_handler(event, context):
    return{
        "user_id": event["user_id"],
        "message": "エラーが起きました。"
    }