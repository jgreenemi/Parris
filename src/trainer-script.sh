#!/usr/bin/env bash
# This script is what will run on the EC2 instance once it launches.
# You'll want to verify that this functions as expected before launching
# an expensive instance type with it, as simple typos can become costly
# if you're launching and terminating instances every time you have a
# bug. Starting with a t2.micro to test your first stack is a safe bet.

# The following line is for the "at-fixed-time" termination method. Do
# not change this line unless you know what you're doing.
printf "%s\n" "Received TERMINATION_TIME_LIMIT value of ${TERMINATION_TIME_LIMIT}, executing: shutdown -h +${TERMINATION_TIME_LIMIT} &"
shutdown -h +${TERMINATION_TIME_LIMIT} &

########################################################################
# Do not change the contents above this line unless you know what you're
# doing.
#
# Your custom training commands go below this comment! Everything below
# this line is just for example and can be deleted.
########################################################################


# Run setup of your training session. Your commands will invariably look different.
cd /tmp

yum update -y
yum install -y git python36 libgfortran libgomp
git clone https://github.com/jgreenemi/MXNet-Familiarity-Project.git
cd MXNet-Familiarity-Project
python3 -m pip install -r requirements.txt

# Pull down the necessary datasets. Keep in mind the EC2 instance needs an IAM
# role for s3:GetObject to pull data from S3.
mkdir data & cd data
aws s3 cp s3://com.jgreenemi.mlbucket/ml-datasets/example-tpp-data/ . --recursive

# Setup done - now run the training job.
python3 classifier/trainer.py

# If the script has completed, go ahead and turn off the server to eliminate any
# additional costs.
poweroff now
