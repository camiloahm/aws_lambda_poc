import json
import boto3
import random

def lambda_handler(event, context):
    print("In lambda handler")
    
    queryname = event["queryStringParameters"]['queryname']
    
    #Don't forget to create the SSM parameter for
    # /doggieWebSite/topSecretDoggieName  and put the value in it.
    # Then give the Lambda execution role permissions to Read
    # the parameter.
    # If you want to use a Secure string parameter, change "WithDecryption" to True
    # and give the Lambda execution role permissions to Read
    # the encryption Key as well.
    ssm = boto3.client('ssm')
    topSecretDoggieName = ssm.get_parameter(Name='/doggieWebSite/topSecretDoggieName',WithDecryption=False)['Parameter']['Value']
    
    #OR
    # Comment out the ssm lines above and just set the topSecretDoggieName in code
    # topSecretDoggieName = "MyDoggieName"

    if (queryname.lower() == topSecretDoggieName.lower()):
        responsetext = "Correct! My name is " + topSecretDoggieName + "!"
    else:
        responsetext = "My name isn't " + queryname + ", it's " + topSecretDoggieName + "!"

    photonumber = random.randint(1, 5)
    dogphoto = "bigdog" + str(photonumber) + ".jpg"

    client = boto3.client("s3")  
    # Generating a pre-signed URL with a 2 second lifetime
    presignedURL = client.generate_presigned_url('get_object',
                                            Params={'Bucket': 'labdemowebsite','Key': dogphoto},
                                            ExpiresIn=2)
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "responsetext": responsetext,
            "image": presignedURL
        })
    }

    return resp