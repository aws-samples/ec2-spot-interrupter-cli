import boto3
import time
import click
import logging
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed

logger = logging.getLogger(__name__)

WAIT_TIME = 2


def createExperimentTemplate(instanceArns, fisRoleArn, duration_before_interruption):
    if not instanceArns:
        raise Exception('Creating FIS template, instance Id can\'t be empty')
    
    client = boto3.client('fis')
    response = client.create_experiment_template(
        description='Created by ec2-spot-interrupter tool',
        stopConditions=[
            {
                    'source': 'none',
            },
        ],
        targets={
            'targetSpot': {
                'resourceType': 'aws:ec2:spot-instance',
                'resourceArns': instanceArns,
                'selectionMode': 'ALL',
            }
        },
        actions={
            'actionSpot': {
                'actionId': 'aws:ec2:send-spot-instance-interruptions',
                'parameters': {
                    'durationBeforeInterruption': 'PT{0}M'.format(duration_before_interruption)
                },
                'targets': {
                    'SpotInstances': 'targetSpot'
                },
            }
        },
        roleArn=fisRoleArn,

    )
    return response['experimentTemplate']['id']


def createAllExperimentTemplates(instanceArns, fisRoleArn, duration_before_interruption):
    if not fisRoleArn:
        raise Exception('FIS IAM role can\'t be empty')

    templatesIds = []
    for i in range(len(instanceArns)//5 + 1):
        onlyFiveInstances = instanceArns[5*i:5*(i+1)]
        if onlyFiveInstances:
            templatesIds.append(createExperimentTemplate(
                onlyFiveInstances, fisRoleArn, duration_before_interruption))
            
    
    logger.info(f'{len(templatesIds)} templates created.')
    return templatesIds


def deleteAllExperimentTemplates(templates):
    time.sleep(WAIT_TIME)
    client = boto3.client('fis')
    for r in templates:
        response = client.delete_experiment_template(
            id=r
        )

#retry=retry_if_exception_type(boto3.client.exceptions.ServiceQuotaExceededException),
@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def startRetryExperiment(id):
    
    client = boto3.client('fis')
    try:
        response = client.start_experiment(
            experimentTemplateId=id)
    # there is a FIS service limit of 5 concurrent experiments to be running
    except client.exceptions.ServiceQuotaExceededException as error:
        logger.exception(error)
        raise error
    
    return response


def startAllExperiments(templates):
    if not templates:
        raise Exception('FIS templates can\'t be empty')

    with click.progressbar(templates) as bar:
        for r in bar:
            startRetryExperiment(r)
            time.sleep(WAIT_TIME)
            


def stop_experiment():
    pass
