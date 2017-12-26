# FAQ #

For everything that doesn't fit elsewhere in the documentation.

## This tool is in Python. Does my algorithm need to be written in Python to use it? ##

Nope! The tool may be written in Python, and the example trainer-script is written in Bash, but your algorithm need not be written in either. As long as your algorithm can be launched from a Linux

## Can I use an OS other than Amazon Linux? ##

Yes! You are free to use whichever OS your needs dictate. To change what your server is launched with, you'll need to find an appropriate AMI (Amazon Machine Image) and update the CloudFormation template with it.

## Can I use this tool with Python2.x instead of Python3.x? ##

I believe so, but this has not been tested. This was written, tested, and intended for use with Python versions 3+.

## I don't need a Lambda function for my use case, but still want to use this tool. Can I? ##

Yes! Although the main benefit of this tool is to give you a one-click launch capability for your training jobs, the Lambda component is not in itself necessary. As long as you can launch the CloudFormation stack from the template, you can launch your training jobs. 

The reason for having a Lambda function in place is to have extensible options for how you launch the stack. For example, if you have a one-liner CLI command or an IoT device that you want to use for launching training jobs on-demand, or if you want to have the training jobs occur on a set schedule (via CloudWatch), a Lambda function makes this possible.

## Is this a library? ##

No, this is a tool, a set of scripts, and as such is not intended to be imported into another package. There's no reason you can't, but the scripts will likely need some changes made to them to make that possible.    