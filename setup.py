from setuptools import setup

setup(
    name = 'ec2-spot-interrupter-cli',
    version = '0.0.1',
    description='A CLI tool to simulate EC2 Spot Instances interruptions using AWS Fault Injection Simulator',
    author='Ahmed Nada',
    author_email='',
    license='This library is licensed under the MIT-0 License. See the LICENSE file',
    url='https://github.com/aws-samples/ec2-spot-interrupter-cli',
    packages = ['ec2spotinterrupter'],
    install_requires=[
        'boto3>=1.18.25',
        'botocore>=1.21.25',
        'tenacity==8.0.1',
        'click==8.0.3'
    ],
    entry_points = {
        'console_scripts': [
            'esi = ec2spotinterrupter.__main__:main'
        ]
    })