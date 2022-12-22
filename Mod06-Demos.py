# --------
# Create bucket and upload an object
# --------

import boto3
s3_client=boto3.client('s3')
s3_client.create_bucket(Bucket='demo-bucket-123454321')
s3_client.upload_file('W:\My Documents\AWS\Demos\DevOnAWS\MusicLibrary.csv',
                      'demo-bucket-123454321',
                      'MusicLibrary.csv')
s3_client.upload_file('W:\My Documents\AWS\Demos\DevOnAWS\Mod10-PuppyWeb\Puppy.jpg',
                      'demo-bucket-123454321',
                      'Puppy.jpg')

# ----------------------
# Multipart upload example
# ----------------------

import boto3
from datetime import datetime

start_time = datetime.now()

s3_resource = boto3.resource('s3')

from boto3.s3.transfer import TransferConfig
config = TransferConfig(multipart_threshold=1024 * 5, 
                        max_concurrency=10,
                        multipart_chunksize=1024 * 5,
                        use_threads=True)

bucket_name = 'demo-bucket-123454321'

file_path = 'd:\Training\TestMovie.mp4'
key = 'TestMovie.mp4'

s3_resource.Object(bucket_name, key).upload_file(file_path,Config=config)    

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# ----------------------
# Multipart download example
# ----------------------

import boto3
from datetime import datetime

start_time = datetime.now()

s3_resource = boto3.resource('s3')

from boto3.s3.transfer import TransferConfig
config = TransferConfig(multipart_threshold=1024 * 100, 
                        max_concurrency=10,
                        multipart_chunksize=1024 * 100,
                        use_threads=True)                    

bucket_name = 'demo-bucket-123454321'

file_path = 'd:\Training\TestMovie-DL.mp4'
key = 'TestMovie.mp4'

s3_resource.Object(bucket_name, key).download_file(file_path,Config=config)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# ----------------------
# Multipart download example using defaults
# ----------------------

import boto3
from datetime import datetime

start_time = datetime.now()

s3_resource = boto3.resource('s3')

from boto3.s3.transfer import TransferConfig

bucket_name = 'demo-bucket-123454321'

file_path = 'd:\Training\TestMovie-DL.mp4'
key = 'TestMovie.mp4'

s3_resource.Object(bucket_name, key).download_file(file_path)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# ----------------------------------------------
# Download the ENTIRE CSV file for LOCAL processing
# ----------------------------------------------

import boto3
import pandas as pd
from datetime import datetime

start_time = datetime.now()

# Creating the low level functional client
client = boto3.client('s3')
    
# Create the S3 object variable
obj = client.get_object(Bucket = 'demo-bucket-123454321',Key = 'MusicLibrary.csv')
    
# Read data from the S3 object
data = pd.read_csv(obj['Body'])
    
# Query just for The Police
queryresult = data.query('Artist == "The Police"')
print(queryresult)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# -----------------------------------------------------------------
# Process the CSV file using S3 Select BEFORE returning the results
# -----------------------------------------------------------------

import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

start_time = datetime.now()

S3_KEY = 'MusicLibrary.csv'
S3_BUCKET = 'demo-bucket-123454321'

s3_client = boto3.client(service_name='s3')
query = """SELECT Artist, Album, Title  
        FROM S3Object
        WHERE Artist like '%Police%'"""

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

df = pd.read_csv(StringIO(file_str))

# Print the data frame
print('Printing the data frame...')
print(df)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

# ----------------------
# Generate a presigned URL that only lasts for 30 seconds
# ----------------------

import boto3

client = boto3.client("s3")

response = client.generate_presigned_url('get_object',
                                        Params={'Bucket': 'demo-bucket-123454321','Key': 'Puppy.jpg'},
                                        ExpiresIn=30)

print(response)

# ----
# Retrieve the list of existing buckets
# ----
import boto3
s3client = boto3.client('s3')

response = s3client.list_buckets() # Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

# ----
# Paginate over a large list of objects
# ----
import boto3
s3client = boto3.client('s3')
paginator = s3client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket='labdemowebsite',
                                   PaginationConfig={'PageSize': 5})
for page in page_iterator:
        print(page['Contents'])

# ------------
# Delete the demo objects and bucket
# ------------

import boto3

AWS_REGION = "us-east-1"
S3_BUCKET_NAME = "demo-bucket-123454321"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

def cleanup_s3_bucket():
    # Deleting objects
    for s3_object in s3_bucket.objects.all():
        s3_object.delete()
    # Deleting objects versions if S3 versioning enabled
    for s3_object_ver in s3_bucket.object_versions.all():
        s3_object_ver.delete()
    print("S3 Bucket cleaned up")

cleanup_s3_bucket()

s3_bucket.delete()

print("S3 Bucket deleted")