# List Objects in Bucket using the Client API 
# Return type: dict / additional API calls needed to get objects

def listClient():
	import boto3
	s3client = boto3.client('s3')
	response = s3client.list_objects_v2(Bucket='labdemowebsite')
	for content in response['Contents']:
		print(content['Key'],content['LastModified'])

listClient()

# List Objects in Bucket using the Resource API
# Resources represent an object-oriented interface to Amazon Web Services (AWS). 
# They provide a higher-level abstraction than the raw, low-level calls made by service clients
def listResource():
	import boto3
	s3resource = boto3.resource('s3')
	bucket = s3resource.Bucket('labdemowebsite')
	for object in bucket.objects.all():
		print(object.key, object.last_modified)

listResource()

# Running the code without a function
import boto3
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket('labdemowebsite')
for object in bucket.objects.all():
	print(object.key, object.last_modified)

#Waiter Examples

#Without a waiter
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
	TableName='Test123',
	KeySchema=[
		{
			'AttributeName': 'custid',
			'KeyType': 'HASH'  # Partition key
		}
	],
	AttributeDefinitions=[
		{
			'AttributeName': 'custid',
			'AttributeType': 'N'
		}
	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 10,
		'WriteCapacityUnits': 10
	}
)

print("Table status:", table.table_status)
print("Waiting 3 seconds...")
time.sleep(3)
get_table = dynamodb.Table("Test123")
print("Table status:", get_table.table_status)

# ==============
# Delete Table
# ==============
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Test123')
table.delete()
print("Test table deleted.")

#With a waiter
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
	TableName='Test123',
	KeySchema=[
		{
			'AttributeName': 'custid',
			'KeyType': 'HASH'  # Partition key
		}
	],
	AttributeDefinitions=[
		{
			'AttributeName': 'custid',
			'AttributeType': 'N'
		}
	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 10,
		'WriteCapacityUnits': 10
	}
)

print("Table status:", table.table_status)
table.meta.client.get_waiter('table_exists').wait(TableName='Test123')
get_table = dynamodb.Table("Test123")
print("Table status:", get_table.table_status)

# ==============
# Delete Table
# ==============
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Test123')
table.delete()
print("Test table deleted.")