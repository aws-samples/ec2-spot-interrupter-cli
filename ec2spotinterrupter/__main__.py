"""
Description: Use this command tool to simulate Amazon EC2 Spot Instances interruptions
Written by: Ahmed Nada
"""
from distutils.command import config
import sys
import os
import click
import logging
from .config import *
from .configure_command import *
from .interrupt_command import *
from .version_command import *

# todo: change default logging level
logging.basicConfig(filename='esi.log', level=logging.INFO)


@click.group()
def main():
    pass



@click.command()
@click.option('-dbi', '--duration-before-interruption', default=2, help='The duration after which the Spot instances are interrupted, must be between 2 and 15 minutes', type=click.IntRange(2, 15))
@click.option('-c', '--count', default=1, help='Number of instances to interrupt', type=click.IntRange(1, 1000))
@click.option('-tk', '--tag-key', required=True, help='Filter instances tag key')
@click.option('-tv', '--tag-value', required=True, help='Filter instances tag value')
@click.option('-r', '--region', required=False, help='NOT USED | aws region')
@click.option('-i', '--instance-ids', required=False, help='NOT USED | List of instances ids to be interrupted')
@click.option('--confirm', is_flag=True,required=False, help='NOT USED | Boolean to auto confirm interruption')
@click.option('-ir', '--iam-role', required=False, help='ARN of IAM role for FIS')
@click.option('--dry-run', default=False, help='NOT USED | Checks whether you have the required  permissions  for  the  action, without actually making the request')
def interrupt(duration_before_interruption, count, tag_key, tag_value, region, dry_run, instance_ids, confirm, iam_role):
    if config.init():
        interruptCommand(duration_before_interruption, count,
                     tag_key, tag_value, region, dry_run, confirm, iam_role)


@click.command()
def version():
    versionCommand()


main.add_command(interrupt)
main.add_command(configure)
main.add_command(version)

if __name__ == '__main__':
    main()
