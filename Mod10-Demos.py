# Basic Hello World Lambda Function for an API Gateway Demo

def lambda_handler(event, context):
    body = 'Hello ' + event["queryStringParameters"]['name']
    return {
        'statusCode': 200,
        'body': body
    }
