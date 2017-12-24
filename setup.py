# After setting up the config.json, lambda-function.py, and trainer-script.sh files,
# run this script to create the necessary Lambda function. Execution of the Lambda
# function will be triggered manually by you from the AWS CLI or web console, a separate
# program of yours via the AWS SDK, an IoT button, or whatever other trigger you make use of
# for firing off your algorithm's training session.

import boto3
import json
import logging
import os
import zipfile


def lambda_packer():
    """
    To create the Lambda function we need to pack up a ZIP file to upload. Returns true if the ZIP archive is created,
    False is something goes wrong. If it succeeds, the second item in the returned tuple object is the 'lambdapack'
    filepath, or the relative filepath to the Lambda-ready ZIP file.
    :return:
    """
    try:
        # Create a ZIP archive, with compression. The files in `config/` and `src/` are the only ones we need to include
        # for the Lambda to function, but in case you have custom needs you can add the necessary directories under this
        # dict.
        directories_to_include = ['config', 'src']
        destination_filepath = 'target/Parris-v1-Lambda.zip'

        # Create the target directory if it doesn't exist.
        if not os.path.exists('target'):
            try:
                os.makedirs('target')
            except Exception as e:
                raise Exception('Tried to create target/ dir but failed. {}'.format(e))

        with zipfile.ZipFile(destination_filepath, mode='w') as lambdapack:
            # Crawl directories, and write their files into the ZIP with the structure of foldername/filename.
            # This should maintain subdirectory heirarchies.
            for dirname in directories_to_include:
                for root, dir, filename in os.walk(dirname):
                    for individual_file in filename:
                        composite_filename = os.path.join(root, individual_file)
                        logging.debug('Adding: {}'.format(composite_filename))

                        # AWS Lambda functions are expected to have the handler at the top level of the package.
                        # If you have other scripts like lambda-function.py that need to be in the root of the package,
                        # include them in the list below and they'll be put at the root of the ZIP archive.
                        if individual_file in ['lambda-function.py']:
                            lambdapack.write(filename=composite_filename, arcname=individual_file)
                        else:
                            lambdapack.write(filename=composite_filename, arcname=composite_filename)

        logging.info('Packed lambdapack to {}'.format(destination_filepath))
        return [True, destination_filepath]

    except Exception as e:
        msg = 'lambda_packer failure: {}'.format(e)
        logging.error(msg)
        return [False, msg]


def lambda_creation(lambda_config={}, lambdapack=''):
    """
    Create the lambda function, return the response, give the AWS CLI command to execute it.
    :return:
    """
    try:
        # Make a Lambda Boto3 client, upload lambdapack, return successful ARN to prove success.
        # TODO customize the method by which the AWS keys are decided. User may want to create this under a different
        # AWS account than their environment variables are set.
        client_lambda = boto3.client('lambda')

        # TODO Make the IAM role configurable by user for what they may need from it. Since this'll be job-agnostic,
        # assume it needs read/write to S3, CFN launch, EC2 tag describe, and nothing else.
        # TODO Allow training-job config to specify if this function should be noclobber if exists. Doesn't really
        # need to be in the training-job config if the Lambda function will be job-agnostic though.

        try:
            logging.warning('Uploading Lambdapack from {}'.format(lambdapack_filepath))
            creation_response = client_lambda.create_function(
                FunctionName='Parris-v1-Lambda',
                Runtime='python3.6',
                Role=lambda_config['lambda_role_arn'],
                Handler='lambda-function.lambda_handler',
                Code={
                    'ZipFile': open(lambdapack_filepath, mode='rb').read()
                },
                Description='Lambda function for Parris, the ML training automation tool.',
                Timeout=30,
                MemorySize=128,
                Tags={
                    'Name': 'Parris-v1-Lambda'
                }
            )

        except Exception as update_err:
            # If an error was thrown during the creation of the Lambda function, we want to intercept this and check if
            # it was because the function already exists. If it does, try an update to it. Otherwise pass it along.
            # Normally we would do an 'except ResourceConflictException:' block here, but for whatever reason this class
            # is not available in botocore or boto3 to use, so this'll have to do.
            if 'ResourceConflictException' in str(update_err):
                logging.error('lambda_creation encountered ResourceConflictException - attempting function update.')
                creation_response = client_lambda.update_function_code(
                    FunctionName='Parris-v1-Lambda',
                    ZipFile=open(lambdapack_filepath, mode='rb').read()
                )
            else:
                raise Exception(update_err)

        # Report success with the function's ARN!
        try:
            lambda_arn = creation_response['FunctionArn']
        except Exception as arn_err:
            raise Exception(
                'lambda_creation failure: Lambda ARN not pulled from response: {} \nResponse contents: {}'
                .format(arn_err, creation_response)
            )

        logging.warning('Successfully created function: \n{}'.format(lambda_arn))
        return [True, lambda_arn]
    
    except Exception as e:
        msg = 'lambda_creation failure: {}'.format(e)
        logging.error(msg)
        return [False, msg]


def parse_config():
    """
    Parse and return the config. This'll be a lot shorter than the _test function.
    :return:
    """
    try:
        config = json.load(open('config/lambda-config.json'))
        return config
    
    except Exception as e:
        msg = 'parse_config failure: {}'.format(e)
        logging.error(msg)
        return False


def _test_lambda_packer():
    """
    Try to pack up a Lambdapack with the current config.
    :return:
    """
    try:
        lambda_packer()
        return [True, '']

    except Exception as e:
        msg = '_test_lambda_packer failure: {}'.format(e)
        logging.error(msg)
        return [False, msg]


def _test_lambda_creation():
    """
    Parse and return the config. This'll be a lot shorter than the _test function.
    :return:
    """
    try:
        lambda_config = parse_config()
        lambda_creation(lambda_config)
        return [True, '']
    
    except Exception as e:
        msg = '_test_lambda_creation failure: {}'.format(e)
        logging.error(msg)
        return [False, msg]


def _test_parse_config():
    """
    Try parsing the JSON config. Check for file existence, valid parsing, and of course
    that valid inputs are configured. (Numerical inputs for time and cost, for example.)
    :return:
    """
    try:
        lambda_config = parse_config()
        logging.debug('Config parsed, training-job-name set to: {}'.format(lambda_config['lambda_role_arn']))
        return [True, '']
    
    except Exception as e:
        msg = '_test_parse_config failure: {}'.format(e)
        logging.error(msg)
        return [False, msg]


if __name__ == '__main__':
    """
    Parse the config, craft a CloudFormation template, create the Lambda function.
    """

    # TODO Go through this file and change the logger so not everything's a logging.warning() message.

    testresult = []
    testresult.append(_test_parse_config())
    testresult.append(_test_lambda_packer())
    # Disabling this test as I want to find a more suitable upload test approach.
    #testresult.append(_test_lambda_creation())
    for testresult, testmsg in testresult:
        if not testresult:
            raise Exception('Tests did not pass: {}'.format(testmsg))

    # If the tests have all passed, go ahead with function creation.
    # Lambdapack is your Lambda-ready ZIP file. You don't have to use the lambda_packer function if you already have one
    # made up, but this is likely the option you want.
    try:
        # TODO Move these to their own function, likely lambda_creation, name them for internal functions per PEP8.
        lambda_config = parse_config()
        lambdapack_successfail, lambdapack_filepath = lambda_packer()
        lambda_creation(lambda_config=lambda_config)
        #config=config, lambdapack=lambdapack_filepath)

    except Exception as e:
        msg = '_test_parse_config failure: {}'.format(e)
        logging.error(msg)

    logging.info('setup.py finished.')
