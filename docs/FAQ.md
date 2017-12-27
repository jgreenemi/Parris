# FAQ #

For everything that doesn't fit elsewhere in the documentation.

## Will this cost money to run? ##

Yes it will. If you are on an AWS Free Tier account, note that this could still cost you money to run, depending on the EC2 instance type used, and possibly other resources necessary for this tool. For example, I'm unfamiliar with the Free Tier usage limits of CloudFormation and Lambda, for example, but I expect those are not completely free to use. 

## This tool is in Python. Does my algorithm need to be written in Python to use it? ##

Nope! The tool may be written in Python, and the example trainer-script is written in Bash, but your algorithm need not be written in either. As long as your algorithm can be launched from a Linux

## Can I use an OS other than Amazon Linux? ##

Yes! You are free to use whichever OS your needs dictate. To change what your server is launched with, you'll need to find an appropriate AMI (Amazon Machine Image) and update the CloudFormation template with it.

## Can I use this tool with Python2.x instead of Python3.x? ##

I believe so, but this has not been tested. This was written, tested, and intended for use with Python versions 3+.

## There are a lot of instance types not listed in the CloudFormation template. Am I restricted to only using c4/c5/p2/p3/g3/etc. instances? ##

Nope! I added in instance types that are common/best-suited for use in machine learning (GPU, memory and compute-focused types), but there's no reason you can't add in others as they suit your needs or as new types come available. Generally speaking you should be set with what is listed, but one size does not fit all, so feel free to add new mappings into the `AWSInstanceType2Arch` dictionary in your template.

## Do I need to delete each CloudFormation stack by hand when training has finished? ##

Yes, for the time being. Later updates will introduce proper termination logic so you don't need to do this, but for now the stack will just shut itself down on completion based on the `termination-method` you set in the `training-config.json` file.

## I don't need a Lambda function for my use case, but still want to use this tool. Can I? ##

Yes! Although the main benefit of this tool is to give you a one-click launch capability for your training jobs, the Lambda component is not in itself necessary. As long as you can launch the CloudFormation stack from the template, you can launch your training jobs. 

The reason for having a Lambda function in place is to have extensible options for how you launch the stack. For example, if you have a one-liner CLI command or an IoT device that you want to use for launching training jobs on-demand, or if you want to have the training jobs occur on a set schedule (via CloudWatch), a Lambda function makes this possible.

## Why are you using AWS? Why not GCP, Azure, etc.? ##

I am most familiar with AWS and use it for my projects. I expect much or even all of this can be done in GCP or Azure, or other cloud providers, if you're inclined to port this tool to them.

## Where did the name come from? ##

"Parris" is in reference to the [Marine Corps training base at Parris Island](https://en.wikipedia.org/wiki/Marine_Corps_Recruit_Depot_Parris_Island). This is where recruits go to become US Marines, and my brother recently graduated from there. It came to mind as this tool is built to be the basis of a machine learning training pipeline capable of running many training jobs simultaneously, and the training base is there to act as a pipeline for producing new Marines week after week. It seems fitting.

## Is this a library? ##

No, this is a tool, a set of scripts, and as such is not intended to be imported into another package. There's no reason you can't, but the scripts will likely need some changes made to them to make that possible.