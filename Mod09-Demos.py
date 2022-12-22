# Sample Lambda function for a simple email
# This function must be associated with a role that has SNS publish permissions
# In my demo, this is the "testsns" Lambda function.

import boto3
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Publish a simple message to the specified SNS topic
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:612526645826:DemoTopic',   
        Subject ='From Lambda',
        Message=event["message_body"]   
    )

    return 'OK'

# Test invoking the above function without lambda
lambda_payload = {"message_body":"Simulated Lambda Function"}
lambda_handler(lambda_payload,"none")

# Invoke the Lambda function from Python

import boto3
import json
lambda_client = boto3.client('lambda')
lambda_payload = {"message_body":"Lambda Function triggered from Python Locally"}
lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:612526645826:function:testsns', 
                     InvocationType='RequestResponse',
                     Payload=json.dumps(lambda_payload))


# Sample function to trigger a message from S3
# This function must be associated with a role that has SNS publish permissions

import boto3

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key =    event['Records'][0]['s3']['object']['key']

    sns = boto3.client('sns')
    sns.publish(
        TopicArn = 'arn:aws:sns:us-east-1:612526645826:DemoTopic',
        Subject = 'File uploaded to bucket: ' + bucket,
        Message = 'The new file is: ' + key
    )


