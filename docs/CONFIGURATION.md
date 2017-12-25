# CONFIGURATION #

Here's the guide to configuring your training jobs. You will primarily be concerned with two configuration files: `lambda-config.json` for the one-time setup of your Lambda trainer function, and `training-config.json` which pertains to the individual training jobs you're looking to launch with said function.

All configuration options are required unless marked otherwise. 

## `lambda-config.json` Configuration Reference ##

You should only need to set this config once for the initial configuration of the Lambda function, and from here on out you should only need to update the `training-config.json` for each training job you're looking to run. The idea is that you'll use one Lambda function for launching multiple training stacks. 

### `lambda-role-arn` ###

A string of the ARN value for your Lambda function's IAM role. This defines what your Lambda function has permission to do within your AWS account, so it's pretty important you get this set up correctly. The ARN value will look something like this:

`arn:aws:iam::277012880214:role/Lambda_CFN_CreateAndValidate`

If you're trying to create one of those and are totally clueless as to what should go into the IAM policy on it, an example IAM policy that should work for most scenarios is as follows:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:TerminateInstances",
                "ec2:RunInstances",
                "cloudformation:CreateStack",
                "cloudformation:UpdateStack",
                "cloudformation:ValidateTemplate"
            ],
            "Resource": "*"
        }
    ]
}
```

When in doubt, always consult the AWS documentation.

### `s3_training_bucket` ###

**Optional.** A string value of an S3 bucket your Lambda function and CloudFormation stack will have access to. An example S3 bucket name value is as follows:

`"s3_training_bucket": "com.jgreenemi.mlbucket"`

Note that the name does not include a protocol prefix like `s3://` or `https://`, just the bucket name. 

Note that you have to update the IAM role on your Lambda function to be able to retrieve training configs from that S3 bucket, and modify the CloudFormation template to create/use an IAM role that also has access. Neither of these are implemented by default. 

If this value is not set, Lambda will look in the `src/` directory of the package you uploaded to use the one provided there. Opting not to use the S3 bucket means you'll have to upload a new Lambda package each time the `trainer-script.sh` needs updating, so do take this into account when deciding whether or not to use it.

## `training-config.json` Configuration Reference ##

### `training-job-name` ###

A string used to prefix your logs, Lambda function name, and CloudFormation stack.

* Example: `Test-Training-Job`

### `termination-method` ###

There are several termination options available. `on-complete` will run the script until it terminates. **If your script runs indefinitely, so too will the training job, and that can get very expensive. Choose this setup if you know your script will end eventually.** 

* Options: `[on-complete, at-fixed-time, around-cost-threshold]`

### `termination-options` ###

For the aforementioned termination methods, some will have parameters. Obviously, use the appropriate parameter set for the method you choose. (Having multiple options defined in the config file is valid, but only the optionset necessary for your chosen termination method will be used.) `time-limit` is measured in hours (decimals are valid), and `cost-limit` is the total anticipated cost in USD, based on the published AWS compute costs.

Do note that the `cost-limit` parameter is an estimation, and **is not a guarantee that your resource usage bill will remain under this limit.** 

* Options: 
```
"termination-options": {
  "time-limit": 10.0,
  "cost-limit": 300
}
``` 

### `training-script-filename` ###

A string describing the trainer-script filename that this particular training job will use. If your Lambda config is set to use a S3 bucket for storing your training job configurations, your trainer-script will need to live in that bucket as well. If you're not using the S3 bucket, the trainer-script in the `src/` directory of this package will be loaded instead. 
 
 In either case, Lambda will feed the trainer-script into the CloudFormation template for you when launching the CloudFormation stack, and it'll run as the EC2 instance userdata script - basically the first script that is run on the server after it has been spun up. 

* Example: `trainer-script.sh`


### `stack-replacement` ###

A Boolean value for deciding how to handle a pre-existing CloudFormation stack. Let's say you run the Lambda function twice for this particular training job. The Lambda function will, on its second execution, see that there's already a CloudFormation stack for your training job. With this value set to `true`, the Lambda function will fire an update of that stack, which can involve a terminate and replacement of that EC2 instance. In other words, if you're keeping your training results on the instance instead of having your trainer-script, you definitely do not want this to be set. 

On the other hand, if this parameter is set to `false` or if you omit it from the config altogether, the function will just error out and leave the existing stack in place. If you're saving your training results on the instance, this is likely the option you want.
