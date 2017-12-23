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


def lambda_packer(config={}):
    """
    To create the Lambda function we need to pack up a ZIP file to upload. Returns true if the ZIP archive is created,
    False is something goes wrong.
    :return:
    """
    try:
        if not config:
            raise Exception('lambda_packer is missing a config. Needed for setting a Lambda function name.')

        # Create a ZIP archive, with compression. The files in `config/` and `src/` are the only ones we need to include
        # for the Lambda to function, but in case you have custom needs you can add the necessary directories under this
        # dict.
        directories_to_include = ['config', 'src']
        destination_filepath = 'target/lambdapack-{}.zip'.format(config['training-job-name'])

        # Create the target directory if it doesn't exist.
        if not os.path.exists('target'):
            try:
                os.makedirs('target')
            except:
                raise Exception('Tried to create target/ dir but failed.')

        with zipfile.ZipFile(destination_filepath, mode='w') as lambdapack:
            # Crawl directories, and write their files into the ZIP with the structure of foldername/filename.
            # This should maintain subdirectory heirarchies.
            for dirname in directories_to_include:
                for root, dir, filename in os.walk(dirname):
                    for individual_file in filename:
                        composite_filename = os.path.join(root, individual_file)
                        logging.warning('Adding: {}'.format(composite_filename))
                        lambdapack.write(filename=composite_filename, arcname=composite_filename)

        logging.info('Packed lambdapack to {}'.format(destination_filepath))
        return True, destination_filepath

    except Exception as e:
        msg = 'lambda_packer failure: {}'.format(e)
        logging.error(msg)
        return False, msg


def lambda_creation(config={}):
    """
    Create the lambda function, return the response, give the AWS CLI command to execute it.
    :return:
    """
    try:
        return True
    
    except Exception as e:
        msg = 'lambda_creation failure: {}'.format(e)
        logging.error(msg)
        return False


def parse_config():
    """
    Parse and return the config. This'll be a lot shorter than the _test function.
    :return:
    """
    try:
        config = json.load(open('config/config.json'))
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
        config = parse_config()
        lambda_packer(config)
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
        raise Exception('uhoh!')
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
        config = parse_config()
        logging.debug('Config parsed, training-job-name set to: {}'.format(config['training-job-name']))
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
    testresult.append(_test_lambda_creation())
    for testresult, testmsg in testresult:
        if not testresult:
            raise Exception('Tests did not pass: {}'.format(testmsg))


    # If the tests have all passed, go ahead with function creation.
    
    #lambda_creation(config=parse_config())

    logging.info('setup.py finished.')
