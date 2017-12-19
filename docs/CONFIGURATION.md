# CONFIGURATION #

Here's the guide to configuring your training jobs.

## `training-job-name` ##

A string used to prefix your logs, Lambda function name, and CloudFormation stack.

* Example: `Test-Training-Job`

## `termination-method` ##

There are several termination options available. `on-complete` will run the script until it terminates. **If your script runs indefinitely, so too will the training job, and that can get very expensive. Choose this setup if you know your script will end eventually.** 

* Options: `[on-complete, at-fixed-time, around-cost-threshold]`

## `termination-options` ##

For the aforementioned termination methods, some will have parameters. Obviously, use the appropriate parameter set for the method you choose. (Having multiple options defined in the config file is valid, but only the optionset necessary for your chosen termination method will be used.) `time-limit` is measured in hours (decimals are valid), and `cost-limit` is the total anticipated cost in USD, based on the published AWS compute costs.

Do note that the `cost-limit` parameter is an estimation, and **is not a guarantee that your resource usage bill will remain under this limit.** 

* Options: 
```
"termination-options": {
  "time-limit": 10.0,
  "cost-limit": 300
}
``` 

