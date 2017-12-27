# Getting Started with Parris #

Here's how you can go from launching training tasks by hand, to launching them with a single click of a button, single command, single script, etc.! 

## An Overview ##

Parris is a tool that:

* creates a Lambda function
* launches a CloudFormation stack when the Lambda function is invoked
* runs a UserData script on the stack's EC2 instance when it is first launched, that kicks off your training job
* stops the EC2 instance when it has finished.

The primary purpose of this tool is to reduce the amount of repetitive setup it takes for you to train your machine learning algorithms, and in doing so save some cost by utilizing your server's compute hours more effectively (server starts the training jobh as soon as it's launched, and stops when you've configured it to stop).

## What You Need Before Starting ##

Follow the setup notes in the README. You will need a machine learning algorithm with its dataset, ready to be trained, and a Bash script that will kick off that training job. 

If that sounds like a lot, don't worry - this package comes with an example trainer-script to give you an idea of what all is involved if you haven't yet made one. Now, if that sounds like a lot because your algorithm is not yet in a state to be trained or does not have a dataset prepared, then you will not be able to take advantage of this tool, so do make sure you have all that ready to go before starting.

### A Note About Retrieving Your Training Results ###

Your trainer-script, or the algorithm itself, needs to push its training results out to an external location (out to another server, an S3 bucket, etc.). The CloudFormation stack you launch is intended to be terminated after you're done training, and as such is ephemeral in nature. Storing the training results on that server for any stretch of time is not recommended.

## 0. Preparing Your Configs ##

Your main interactions with this tool, after it is properly set up, will be editing the `training-config.json` configuration file, and the `trainer-script.sh` script that actually runs your training job. Since we're getting set up for the first time, you'll want to also set up your `lambda-config.json` configuration file. (That one should be real easy since it's only two lines, one of which being optional.)

The configs as supplied are examples for a basic training job using one of the repositories on my Github, to give you an idea of what one will look like. With the exception of some account-specific things like IAM role ARN values and S3 bucket names, you could run this as-is. So let's start with some of those.

1. In the [`training-config`](/config/training-config.json): 
    1. Change your `subnet-id` to the ID of one of your Subnets. (Don't know what this is? Make sure you've [set up your AWS Account with a VPC, Subnet, Security Group, and EC2 Keypair.](http://docs.aws.amazon.com/AmazonVPC/latest/GettingStartedGuide/getting-started-ipv4.html) There should be some default resources in your account that you can use if this is your first time using AWS.)
    1. Change your `security-group-id` to a Security Group in your VPC.
    1. Change your `ec2-keypair-name` to an EC2 keypair of your own.
    1. All other parameters in the training-config can remain unchanged, unless you wish to. Consult [the CONFIGURATION document](/docs/CONFIGURATION.md) for what each parameter is about. 
1. In the [`lambda-config.json`](/config/lambda-config.json):
    1. Update the `lambda-role-arn` to the ARN value of an IAM role of your own. (Don't know what this is? [Have a look through the Lambda IAM Execution Role guide.](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html) An example policy you can use is below.) 

When setting up your IAM Role, you'll need to attach a Policy (or multiple Policies) to the Role to define what all your Lambda function can access. The one I use is as follows, and lets your Lambda function start up new CloudFormation stacks, get objects from your S3 buckets, and do a lot with EC2 instances: 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:ValidateTemplate",
                "ec2:DetachVolume",
                "ec2:AttachVolume",
                "ec2:ModifyVolume",
                "ec2:ModifyVolumeAttribute",
                "ec2:DescribeInstances",
                "ec2:TerminateInstances",
                "ec2:DescribeTags",
                "ec2:CreateTags",
                "ec2:DescribeVolumesModifications",
                "ec2:RunInstances",
                "ec2:StopInstances",
                "ec2:DescribeVolumeAttribute",
                "ec2:CreateVolume",
                "ec2:DeleteVolume",
                "ec2:DescribeVolumeStatus",
                "ec2:StartInstances",
                "ec2:DescribeVolumes",
                "ec2:ModifyInstanceAttribute",
                "ec2:DescribeInstanceStatus",
                "s3:GetObject"
            ],
            "Resource": "*"
        }
    ]
}
```

I highly recommend (though it's not required) having a Policy made up for allow Lambda to write to a CloudWatch logstream. When something goes wrong with your Lambda function, you'll want to be able to read the logs to find out what's going on. Here's one I use that's literally all the CloudWatch Write permissions in one Policy, 'cause that was easiest to set up with the visual editor:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:DeleteSubscriptionFilter",
                "logs:DeleteLogStream",
                "logs:CreateExportTask",
                "logs:DeleteResourcePolicy",
                "logs:CreateLogStream",
                "logs:DeleteMetricFilter",
                "logs:TagLogGroup",
                "logs:CancelExportTask",
                "logs:DeleteRetentionPolicy",
                "logs:GetLogEvents",
                "logs:AssociateKmsKey",
                "logs:FilterLogEvents",
                "logs:PutDestination",
                "logs:DisassociateKmsKey",
                "logs:UntagLogGroup",
                "logs:DeleteLogGroup",
                "logs:PutDestinationPolicy",
                "logs:TestMetricFilter",
                "logs:DeleteDestination",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:PutMetricFilter",
                "logs:PutResourcePolicy",
                "logs:PutSubscriptionFilter",
                "logs:PutRetentionPolicy"
            ],
            "Resource": "*"
        }
    ]
}
```

It's way more than necessary, but that's what I have in use at the moment.

Finally, we need to set up the `trainer-script.sh` so it'll actually run your training job. This part should be almost entirely written by you, as your algorithm's dependencies and your method for pushing out the training results will invariably differ from what I have shown.

1. In `trainer-script.sh`:
    1. Scroll to the section below the very obvious comment saying to edit everything below it. Add in your complete training script below that line. Keep in mind that your training script is being launched on a fresh server, so all setup of dependencies, directory structure, etc. needs to be done before launching your training job. For example, if you need a different version of Python installed or if you need to clone a Git repo, make sure all those steps are included.
    
Once that is done, you are nearly set to get started using the tool! If you are **NOT** using an `s3-training-bucket` value in your `lambda-config.json`, then you are ready to go - proceed to the next step. If you are using an S3 bucket for loading your configs, you'll need to load the following files in your S3 bucket such that its resulting structure looks like so (as in no subdirectories or differing filenames):

```bash
+---MyS3Bucket
|   \---trainer-script.sh
|   \---training-config.json
|   \---lambda-config.json
```

Once that's ready to go, then you can proceed to the next step.

## 1. Preparing Your Lambda Function ##

Before we can launch a training job, we need a way to kick that off. This step will have you creating an AWS Lambda function that can be used for multiple training jobs of the same algorithm, or multiple training jobs of different algorithms.

## 2. Launching Your First Training Stack ##

## 3. Updating Your Training Stack ##

## 4. Getting Training Results ##

This largely depends on how you have your algorithm set to save the resulting parameters. For our example, those will be stored locally in the `target/` directory. But, since we'll be terminating the stack at the end of this guide, we'll want to push those out to a more permanent location. 

## 5. Terminating Your CloudFormation Stack ##

## 6. Updating Your Lambda Function ##

## 7. Triggering Training Jobs Outside the AWS Console ##

At this point you've completed the general walkthrough for Parris! Nice work - everything from here on out is more for improving the convenience factor for you when using this tool. Our first example will be setting up an IoT device for triggering new training jobs on-demand. Further examples will include setting up a schedule for regular retraining (i.e. for when you have an application that depends on an algorithm that needs to be retrained on new datasets regularly to stay effective). 

### a. Setting Up An IoT Device ###

For this example we'll be using the AWS IoT button as our device.

### b. Setting Up A Regular Training Schedule via CloudWatch ###

More on this in a future update! 