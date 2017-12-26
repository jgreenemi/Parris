# Getting Started with Parris #

Here's how you can go from 

## What You Need Before Starting ##

Follow the setup notes in the README. Also, you will need a machine learning algorithm with its dataset, ready to be trained, and a Bash script that will kick off that training job. 

If that sounds like a lot, don't worry - this package comes with an example trainer-script to give you an idea of what all is involved if you haven't yet made one. Now, if that sounds like a lot because your algorithm is not yet in a state to be trained or does not have a dataset prepared, then you will not be able to take advantage of this tool, so do make sure you have all that ready to go before starting.

### A Note About Retrieving Your Training Results ###

Your trainer-script, or the algorithm itself, needs to push its training results out to an external location (out to another server, an S3 bucket, etc.). The CloudFormation stack you launch is intended to be terminated after you're done training, and as such is ephemeral in nature. Storing the training results on that server for any stretch of time is not recommended.

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