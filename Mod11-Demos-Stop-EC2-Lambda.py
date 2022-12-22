# Use InstanceName for the event input property
# ex: {"InstanceName": "Demo Server 2019"}
# Wildcards must follow RegEx syntax
# ex: {"InstanceName": "Demo*"}

import boto3
import re

def lambda_handler(event, context):
        
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        if instance.tags != None:
            for tags in instance.tags:
                if tags["Key"] == 'Name' and re.match(re.compile(event["InstanceName"].lower()),tags["Value"].lower()):
                    print("Stopping instance: - %s,  Instance Id - %s " %(tags["Value"],instance.id))
                    instance.stop()
