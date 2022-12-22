#####
#Query Music Lambda Function Demo.
#####

#This would work with the API Gateway or as a Lambda Function URL.
#Copy this to a new Python Lambda function, then enable
#   the function URL or create an API Gateway. 
# To run the function, access the URL with /?search=Police
# or some other artist to query for.

import boto3
#To use the Pandas library, you need to add the Lambda Layer: AWSDataWrangler-Python39
import pandas as pd
import json
from io import StringIO

# This is the lambda handler function entry point. This function name could be
# modified when creating the function from the SAM toolkit.
def lambda_handler(event, context):
    search = event["queryStringParameters"]['search']
    
    #Uncomment this to use local variables for the bucket and key
    #S3_KEY = 'MusicLibrary.csv'
    #S3_BUCKET = 'markdemostuff'
    
    #OR
    #Uncomment this to use Environment variables for the bucket and key
    #Don't forget to create the Lambda Function environment
    # variables S3_KEY and S3_BUCKET and put the values in them.
    #S3_KEY = os.environ.get('S3_KEY')
    #S3_BUCKET = os.environ.get('S3_BUCKET')
    
    #OR
    #Uncomment this to use SSM Parameters for the bucket and key
    #Don't forget to create the SSM parameters for
    # S3_KEY and S3_BUCKET and put the values in them.
    # Then give the Lambda execution role permissions to Read
    # the two parameters.
    ssm = boto3.client('ssm')
    S3_KEY = ssm.get_parameter(Name='/MusicLibrary/S3_KEY',WithDecryption=False)['Parameter']['Value']
    S3_BUCKET = ssm.get_parameter(Name='/MusicLibrary/S3_BUCKET',WithDecryption=False)['Parameter']['Value']
    
    #Create the s3 client object
    s3_client = boto3.client(service_name='s3')
    #Create the SQL-like query string
    query = """SELECT Artist, Album, Title  
            FROM S3Object
            WHERE LOWER(Artist) like LOWER('%{}%')""".format(search)
    
    #Query the CSV file using S3 Select and only return the results.
    resp = s3_client.select_object_content(Bucket=S3_BUCKET,
                                             Key=S3_KEY,
                                             ExpressionType='SQL',
                                             Expression=query,
                                             InputSerialization={'CSV': {'FileHeaderInfo': 'Use'}},
                                             OutputSerialization={'CSV': {}})
    
    # unpack the response
    records = []
    for event in resp['Payload']:
        if 'Records' in event:
            records.append(event['Records']['Payload'])  
        
    #  store unpacked data as a CSV format
    file_str = ''.join(req.decode('utf-8') for req in records)
    
    df = pd.read_csv(StringIO(file_str),names=["Artist","Album","Song"])
    
    body = df.to_html()

    #Return well-formatted HTML (but not pretty!)
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html"
        },
        "body": "<html><body><h2>Searching for: " + search + "</h2><br><br>" + body + "</body</html>"
    }
