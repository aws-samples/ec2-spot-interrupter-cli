# ec2-spot-interrupter-cli

A CLI tool to simulate EC2 Spot Instances interruptions using AWS Fault Injection Simulator (FIS).

Since October 2021, You can trigger the interruption of an Amazon EC2 Spot Instance using AWS Fault Injection Simulator. When using Spot Instances, you need to be prepared to be interrupted. With FIS, you can test the resiliency of your workload and validate that your application is reacting to the interruption notices that EC2 sends before terminating your instances. You can target individual Spot Instances or a subset of instances in clusters managed by services that tag your instances such as ASG, Fleet and EMR.

## Install (macOS, Linux)

* Clone this repository.
* Use your favorite terminal, change current directory to the downloaded repository folder.
* Run the install script:

```bash
sudo bash install.sh
```

## Getting started

To use this tool, you will need AWS credentials configured. Take a look at the [AWS CLI configuration documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#config-settings-and-precedence) for details on the various ways to configure credentials. An easy way to try out the ec2-instance-interrupter CLI is to populate the following environment variables with your AWS API credentials.

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

You can set the AWS_REGION environment variable if you don't want to pass in `--region` on each run.

```bash
export AWS_REGION="us-east-1"
```

## Examples

1. To interrupt Spot instances using tags, use parameters **--tag-key** and **--tag-value**

```bash
esi interrupt --duration-before-interruption 2 --count 10 --tag-key fis --tag-value yes
```

## Uninstall

* Use your favorite terminal, change current directory to the downloaded repository folder.
* Run the install script:

```bash
sudo bash uninstall.sh
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
