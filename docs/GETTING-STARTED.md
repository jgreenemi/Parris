# Getting Started with Parris #

Here's how you can go from launching training tasks by hand, to launching them with a single click of a button, single command, single script, etc.!

## An Overview ##

Parris is a tool that:

* creates a Lambda function
* launches a CloudFormation stack when the Lambda function is invoked
* runs a UserData script on the stack's EC2 instance when it is first launched, that kicks off your training job
* stops the EC2 instance when it has finished.

The primary purpose of this tool is to reduce the amount of repetitive setup it takes for you to train your machine learning algorithms, and in doing so save some cost by utilizing your server's compute hours more effectively (server starts the training job as soon as it's launched, and stops when you've configured it to stop).

## What You Need Before Starting ##

Follow the setup notes [in the README](/README.md). You will need a machine learning algorithm with its dataset, ready to be trained, and a Bash script that will kick off that training job.

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
    1. Change your `instance-type` to `t2.micro` or another small instance type. Since we're just launching this stack for the sake of the tutorial, we'll want to go for an inexpensive instance type that we can launch and terminate quickly. `t2.micro` is the mainstay for this purpose.
        1. Concerned about how much an EC2 instance type will cost you? Consult the ever-popular [AWS Simple Monthly Calculator](https://calculator.s3.amazonaws.com/index.html) to estimate what kinds of costs you can expect.
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
+---your-s3-bucket
|   \---trainer-script.sh
|   \---training-config.json
|   \---lambda-config.json
```

Once that's ready to go, then you can proceed to the next step.

## 1. Preparing Your Lambda Function ##

Before we can launch a training job, we need a way to kick that off - that's where your Lambda config will get used. This step will have you creating an AWS Lambda function that can be used for multiple training jobs of the same algorithm, or multiple training jobs of different algorithms.

1. In the Parris package root, activate your virtualenv if you haven't already.
1. Create your Lambda function with: `$ python setup.py`
    1. If you already have a Lambda function this will update the code package for it.
1. If all goes well, the log will print out an ARN value for confirmation.

## 2. Launching Your First Training Stack ##

**Note: This step can cost you money, so make sure to give this and the "Terminating Your CloudFormation Stack" a good read-through before getting started.**

1. Open the AWS console and navigate to your Lambda function.
1. Click the "Test" button, at the top of the page, to invoke the function manually. If you don't have a test configured, you will need to do so.
    1. In the Saved Test Events dropdown next to the Test button, click "Configure test events" to create a new one.
    1. Since the Lambda function only has one activity (to launch a new CloudFormation stack when it's invoked), we don't need to pass it any parameters. (If you pass it some it'll accept them, but they won't get used.)
    1. Create a test with Event Name `Parris-Test-Event` and a body of `{}`. Click Save.
    1. Upon closing the creation dialogue, click Test with your new Test Event in the dropdown and watch for the Execution Result to update.
1. When your function has run, the Execution Result should read "succeeded" and give an output of `{}`.
    1. If the function had an error, expand the Exection Result heading to read the errors. Common issues here are around missing IAM permissions on the Lambda function's IAM role.
1. Switch to the CloudFormation view of the AWS Console to watch as your new CloudFormation stack launches. This should only take a minute or two, but is highly dependent on what kind of instance you're launching.
    1. Don't see your CloudFormation stack? Make sure you're in the right Region!
    1. Note that the stack should have a name matching your training job name (the one you set in `training-config.json`.) If for some reason you didn't set a training job name, the stack should assume the default name "parris-stack".
1. Switch to the EC2 Instance view of the AWS Console to take a look at the new instance you've launched. It should soon get to the "Running" state and will be running your training job.

**Note: In the current build of this tool, the CloudFormation stack will not terminate upon completion of the training job. Instead, the EC2 Instance will power itself off. You will be saved from accruing additional costs, since the instance will no longer be running, but to clean it up you'll need to navigate back to the CloudFormation view of the console and click the Delete Stack option under the Actions dropdown to actually delete it.**

## 3. Getting Training Results ##

This largely depends on how you have your algorithm set to save the resulting parameters. In most cases these results will be saved to a local directory (i.e. somewhere on the server, likely in the same package that's doing the training). But, since we'll be terminating the stack at the end of this guide, we'll want to push those out to a more permanent location.

## 4. Terminating Your CloudFormation Stack ##

Now that you've created your CloudFormation stack and confirmed that it is working as expected, we can safely terminate the stack to save on costs.

1. Open the AWS Console and navigate to the CloudFormation view.
1. Select the CloudFormation stack that you launched, from the list.
1. Click the Actions dropdown at the top of the page, and click Delete Stack. It'll ask you to confirm the deletion - click Delete to get rid of it.
1. Watch the Events tab of the stack (bottom of the page) to track its progress. You'll have to refresh the page to populate in new events.
1. When it has terminated, it will disappear from the list. You can confirm it deleted properly (if it being missing from the Active list isn't enough confirmation for you) by clicking in the top-left corner of the list to change the view's Filter from Active to Deleted. You should see the stack's name present, with a Status of "DELETE_COMPLETE". At this point you should not longer have any costs accruing from this training job's resources.

Generally speaking, you should plan on terminating your CloudFormation stack every time a training job completes. Although you *can* update a CloudFormation stack, this tool operates on the idea that the training job is kicked off by the UserData script on the EC2 instance - which only runs when the instance is first being launched. Updating the CloudFormation stack doesn't relaunch the instance except in a few circumstances, depending on what parameters of the stack are being updated. In most cases the instance will simply be Stopped then Started again, which isn't enough to relaunch the training job. Since it doesn't cost anything additional to terminate and launch new instances versus keeping an existing one updated, the best practice for reliable training for your algorithms is to terminate your stacks and relaunch them anytime you need to re-run a training job.

## 5. Updating Your Lambda Function ##

Updating your Lambda function is as easy as making your changes in the `lambda-function.py` file, and re-running `$ python setup.py`. The script will first attempt to create the Lambda function, and if it fails with an error that the function already exists, it'll run an update of the function's code.

Note that certain details about the Lambda function configuration (i.e. the amount of memory it is given) won't be updated by this script - you'll need to either add additional logic into the script to update the function metadata, or just delete and re-recreate your Lambda function with the updated metadata. This is because there are multiple update methods for Lambda functions, and no one update method that covers all possible scenarios, so I put in the one that is most likely to be used right away. Future builds of the tool may include additional update behaviours to cover all scenarios.

You can test the update behaviour by:

1. Open `lambda-function.py` and scroll down to line 272, the `return return-values` statement.
1. Insert a new line just above the return statement so your function ends with:
    ```python
       logging.warning('This is a synthetic warning message!')
       
       return return_values
    ```
    1. Any kind of message will work here, and it can occur most anywhere in that function - just so long as we make some change to the code we can demonstrate that the Lambda function updated.
1. Once the change has been made, simply run `$ python setup.py` again and watch the logging output for the updated ARN being reported.
1. Trigger your Lambda function again with the Test button, and expand out the Execution Result heading. The log output box should include the usual logging output from the Lambda function, and among those messages should be your test message from above.
1. Make sure to terminate your CloudFormation stack to save on costs here.

## 6. Updating Your Training Stack ##

**Updating CloudFormation stacks are in limited functionality in this build as updating a CloudFormation stack will not force a training job to restart. For this reason it's recommended not to update CloudFormation stacks, but rather delete and re-launch them when you have to re-run a training job.**

## 7. Triggering Training Jobs Outside the AWS Console ##

At this point you've completed the general walkthrough for Parris! Nice work - everything from here on out is more for improving the convenience factor for you when using this tool. Our first example will be setting up an IoT device for triggering new training jobs on-demand. Further examples will include setting up a schedule for regular retraining (i.e. for when you have an application that depends on an algorithm that needs to be retrained on new datasets regularly to stay effective).

### a. Setting Up An IoT Device ###

For this example we'll be using the AWS IoT button as our device.

### b. Setting Up A Regular Training Schedule via CloudWatch ###

More on this in a future update! 
