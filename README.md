# README #

Parris, the automated training tool for machine learning algorithms.

### Roadmap ###

#### MVP ####

* Launches an EC2 instance in your AWS account, via CloudFormation template. That instance then runs your training routine until completion, then terminates.
* A Lambda function kicks off the CFN training instance launch.
* Lambda function takes a JSON config for the training job, dynamically creates CFN template for launch.
* The logs from that training job are reported to CloudWatch.
* Time-limit and cost-limit termination routines are implemented in the launched instance.

#### Iteration I ####

* Testing capabilities are implemented, so checks of the training routine are done before the instance is launched. (Catch failures early to save on costs from finding them after the instance has been launched.)
* IoT button integration with a demo Lambda function and trainer routine.
* IoT button is set up for public demo.

#### Iteration II ####

* .

### Setup ###

You'll need an AWS account.


```bash
$ git clone https://*/parris.git && cd parris
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt 
```

### FAQ ###

#### Will this cost money to run? ####

Yes, it will, even on an AWS Free Tier account (due to the instance type used).

### Contact ###

* Joseph Greene, jgreenemi@gmail.com

