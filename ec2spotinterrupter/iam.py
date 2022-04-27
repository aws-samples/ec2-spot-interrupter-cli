import boto3
import json
import logging
from .config import *
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def assessPermissions():
    
    return True
def createPermissions():
    # todo: check if policy already exists
    policy_arn = createPolicy (config.ESI_FIS_IAM_POLICY_KEY,"This policy was created by ESI CLI tool.")
    role_arn = createRole(config.ESI_FIS_IAM_ROLE_KEY)

    if policy_arn and role_arn:
        attachPolicyToRole(config.ESI_FIS_IAM_ROLE_KEY,policy_arn)
        return role_arn
    else:
        raise Exception('FIS IAM role/policy couldn\'t be created.')
    
def getServiceRoleArn(role_name):
    try:
        client = boto3.client('iam')
        response = client.get_role(
            RoleName=role_name
        )
        logger.info("Role found %s.", role_name)
    except ClientError:
        logger.exception("Couldn't get IAM role %s.", role_name)
        return None
    else:
        return response['Role']['Arn']

def createPolicy(name, description):
    policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowFISExperimentRoleReadOnly",
                "Effect": "Allow",
                "Action": "ec2:DescribeInstances",
                "Resource": "*"
            },
            {
                "Sid": "AllowFISExperimentRoleEC2Actions",
                "Effect": "Allow",
                "Action": "ec2:SendSpotInstanceInterruptions",
                "Resource": "arn:aws:ec2:*:*:instance/*"
            }
        ]
    }
    try:
        client = boto3.client('iam')
        policy = client.create_policy(
            PolicyName=name, 
            Description=description,
            PolicyDocument=json.dumps(policy_doc))
        logger.info("Created policy %s.", policy)
    except ClientError:
        logger.exception("Couldn't create policy %s.", name)
        raise
    else:
        return policy['Policy']['Arn']

def createRole(role_name):
    trust_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "fis.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    try:
        client = boto3.client('iam')
        role = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy))
        logger.info("Created role %s.", role)
    except ClientError:
        logger.exception("Couldn't create role %s.", role_name)
        raise
    else:
        return role['Role']['Arn']

def attachPolicyToRole(role_name, policy_arn):
    try:
        client = boto3.client('iam')
        response = client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        logger.info("Attached policy %s to role %s.", policy_arn, role_name)
    except ClientError:
        logger.exception("Couldn't attach policy %s to role %s.", policy_arn, role_name)
        raise