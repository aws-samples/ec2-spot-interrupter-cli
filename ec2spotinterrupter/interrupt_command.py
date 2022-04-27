import click
from .config import *
from .ec2 import *
from .fis import *
from .iam import *
from .logger import *

def interruptCommand(duration_before_interruption, count, tag_key, tag_value, region, dry_run, confirm, iam_role):
    #check if there are instances matcheing tag
    print('Retrieving EC2 instances details...')
    instances = getInstances(count, tag_key, tag_value)
    if len(instances) == 0:
        logger.info('No further steps will be executed!')
        return
    # instances found
    print(f'{len(instances)} Instance(s) will be interrupted!')

    # confirm and abort if user doesn't want to continue
    if not confirm:
     if not click.confirm('Do you want to continue?'):
        return
    
    # check existing iam role if it wasn't provided
    if not iam_role:
        iam_role = getServiceRoleArn(config.ESI_FIS_IAM_ROLE_KEY)
    
    # if IAM role wasn't provided and no existing role was found
    # todo: if confirm skip confirmation
    if not iam_role:
        ask_for_iam = click.confirm('FIS IAM role wasn\'t provided. Do you want to have it created?')
        
        if ask_for_iam:
            # create permissions
            print('Creating IAM policy and role...', end='')
            iam_role = createPermissions()
            print('Done!')
        else:
            # Abort
            print('Aborting...')
            return

    # Continue
    print('Creating experiment templates...')
    templates = createAllExperimentTemplates(
        instances, iam_role , duration_before_interruption)
    

    # start experiments
    try:
        print('Initiating Spot instances interruptions...')
        startAllExperiments(templates)
        print('Cleaning up...',end='')
        deleteAllExperimentTemplates(templates)
        print('Completed!')
    except Exception as error:
        deleteAllExperimentTemplates(templates)
        raise error
    
    # complete
    click.echo(click.style(f'{len(instances)} Instance(s) interruption completed!', fg="green"))
