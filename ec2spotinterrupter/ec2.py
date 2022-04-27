import boto3
import logging
from .config import *
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def getAllInstances(tag_key, tag_value):
    all_instances = []
    try:
        ec2 = boto3.client('ec2')
        next_token = ''
        while True: 
            response = ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-lifecycle',
                        'Values': [
                            'spot'
                        ]
                    },
                    {
                        'Name': 'instance-state-name',
                        'Values': [
                            'running'
                        ]
                    },
                    {
                        'Name': 'tag:'+tag_key,
                        'Values': [tag_value]
                    }
                ],
                MaxResults=50,
                NextToken=next_token
            )
            all_instances.append(response['Reservations'])
            
            # no further instances
            if 'NextToken' not in response:
                break

            next_token = response['NextToken']

       
    except ClientError as error:
        logger.exception(error)
        raise error
    
    return all_instances
    
def getInstances(count, tag_key, tag_value):

    arnTemplate = f'arn:aws:ec2:{config.ESI_REGION}:{config.ESI_ACCOUNT}:instance/'

    all_instances = getAllInstances(tag_key, tag_value)

    instances = []
    for r in all_instances:
        for i in r:
            if 'Instances' in i:
                for y in i['Instances']:
                    if 'InstanceId' in y:
                        instances.append(arnTemplate + y['InstanceId'])
    
    result = instances[0:count]
    print(f'{len(instances)} Running Spot Instance(s) were found.')

    return result
