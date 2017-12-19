# After setting up the config.json, lambda-function.py, and trainer-script.sh files,
# run this script to create the necessary Lambda function. Execution of the Lambda
# function will be triggered manually by you from the AWS CLI or web console, a separate
# program of yours via the AWS SDK, an IoT button, or whatever other trigger you make use of
# for firing off your algorithm's training session.

import boto3
import json
import logging


def lambda_creation(config={}):
    """
    Create the lambda function, return the response, give the AWS CLI command to execute it.
    :return:
    """
    try:
        return True
    
    except Exception as e:
        return False


def parse_config():
    """
    Parse and return the config. This'll be a lot shorter than the _test function.
    :return:
    """
    try:
        config = {}
        return config
    
    except Exception as e:
        return False


def _test_lambda_creation():
    """
    Parse and return the config. This'll be a lot shorter than the _test function.
    :return:
    """
    try:
        return True
    
    except Exception as e:
        return False


def _test_parse_config():
    """
    Try parsing the JSON config. Check for file existence, valid parsing, and of course
    that valid inputs are configured. (Numerical inputs for time and cost, for example.)
    :return:
    """
    try:
        return True
    
    except Exception as e:
        return False


if __name__ == '__main__':
    """
    Parse the config, craft a CloudFormation template, create the Lambda function.
    """

    parse_config_test_result = _test_parse_config()
    lambda_creation_test_result = _test_lambda_creation()

    # If the test have all passed, go ahead with function creation.
    
    lambda_creation(config=parse_config())

    logging.info('setup.py finished.')
