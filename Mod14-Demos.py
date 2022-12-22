# Create your own CloudWatch Custom NameSpace and Metrics
import boto3

client = boto3.client('cloudwatch')

client.put_metric_data(
    Namespace='LabDemo',
    MetricData=[
        {
            'MetricName': 'AppHits',
            'Dimensions': [
                {
                    'Name': 'Application',
                    'Value': 'TestAppOne'
                },
            ],            
            'Value': 1,
            'Unit': 'Count'
        },
    ]
)
