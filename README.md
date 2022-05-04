# ec2-spot-interrupter-cli

A CLI tool to simulate EC2 Spot Instances interruptions using AWS Fault Injection Simulator (FIS).

Since October 2021, You can trigger the interruption of an Amazon EC2 Spot Instance using AWS Fault Injection Simulator. When using Spot Instances, you need to be prepared to be interrupted. With FIS, you can test the resiliency of your workload and validate that your application is reacting to the interruption notices that EC2 sends before terminating your instances. You can target individual Spot Instances or a subset of instances in clusters managed by services that tag your instances such as Auto Scaling group, EC2 Fleet and EMR.

## Install (macOS, Linux)

* Use [AWS CloudShell](https://aws.amazon.com/cloudshell/) or your favorite terminal, clone this repository.

```bash
git clone https://github.com/aws-samples/ec2-spot-interrupter-cli.git
```

* Change current directory to the downloaded repository folder.
* Run the install script:

```bash
sudo bash install.sh
```

## Getting started

To use this tool, you will need AWS credentials configured. Take a look at the [AWS CLI configuration documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#config-settings-and-precedence) for details on the various ways to configure credentials.

Populate the following environment variables with your AWS API credentials.

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

Set the AWS_REGION environment variable if it's not configured.

```bash
export AWS_REGION="..."
```

## Synopsis

esi interrupt

-tk, --tag-key | Filter instances tag key  [required]  
-tv, --tag-value | Filter instances tag value  [required]  
[-dbi, --duration-before-interruption] | Number of minutes represents the duration after which the Spot instances are interrupted, must be between 2 and 15. Default is 2.  
[-c, --count] | Number of instances to interrupt, between 1 and 1000. Default is 1.  
[--confirm] | Flag to auto confirm interruption.  
[-ir, --iam-role] | ARN of IAM role for FIS.  
[--help] | Show help message.

## Examples

1. Interrupt 10 Spot instances filtering by instance tags, with parameters **--tag-key** and **--tag-value**

```bash
esi interrupt --duration-before-interruption 2 --count 10 --tag-key fis --tag-value yes
```

## Uninstall

* Using a terminal, change current directory to the downloaded repository folder.
* Run the uninstall script:

```bash
sudo bash uninstall.sh
```

* Delete the repository folder.

* You may have to manually remove the installation files if it persist.

```bash
sudo rm -rf /usr/local/bin/esi
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
