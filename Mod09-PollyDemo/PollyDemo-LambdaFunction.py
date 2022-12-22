import boto3

def lambda_handler(event, context):
    speak = event["queryStringParameters"]['speak']
    subject = event["queryStringParameters"]['subject']

    s3 = boto3.resource('s3')
    bucket_name = "pollywebdemo"
    key_name = "mp3/" + subject + ".mp3"

    polly = boto3.client("polly")
    response = polly.synthesize_speech(
    Text=speak,
    OutputFormat="mp3",
    VoiceId="Matthew")
    stream = response["AudioStream"]

    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=key_name, Body=stream.read())

    client = boto3.client("s3")  
    # Generating a pre-signed URL with a 2 second lifetime
    presignedURL = client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name,'Key': key_name},
                                            ExpiresIn=120)

    #Return well-formatted HTML (but not pretty!)
    return {
        "statusCode": 200,
        "headers": {
            "content-type": "text/html"
        },
        'body': '<html><body><center><h2>Polly is speaking to you:</h2><br><br><audio controls="controls"><source src="' + presignedURL + '" type="audio/mpeg"><br><br></center></body</html>'
    }
