# Create the CloudFormation stack with the trainer-script loaded.

import boto3
import json
import logging
import os
from pprint import pprint


def parse_training_config(training_config_path=''):
    """
    Pull in a training config and return its contents.
    :return:
    """
    try:
        # Default to the existing training config file in the Lambda function if a specific filename wasn't passed in.
        if not training_config_path:
            training_config_path = 'config/training-config.json'
            config = json.load(open(training_config_path))

        else:
            client_s3 = boto3.client('s3')
            s3_response = client_s3.get_object(
                Bucket=training_config_path,
                Key='training-config.json'
            )

            config = json.loads(s3_response['Body'].read().decode('utf-8'))

        return config

    except Exception as e:
        msg = 'parse_config failure: {}'.format(e)
        logging.error(msg)
        return False


def template_loader(template_path='', cloudformation_template_filename=''):
    """
    Given the filepath for the CloudFormation template, load and return it as a dict.
    :return:
    """
    try:
        if not template_path:
            template_path = 'config/cloudformation.json'
            cfn_template_contents = json.load(open(template_path))

        else:
            client_s3 = boto3.client('s3')
            s3_response = client_s3.get_object(
                Bucket=template_path,
                Key=cloudformation_template_filename
            )

            cfn_template_contents = s3_response['Body'].read().decode('utf-8')

        return cfn_template_contents

    except Exception as e:
        msg = 'template_loader failure: {}'.format(e)
        logging.error(msg)
        return False


def userdata_loader(s3_training_bucket='', trainer_script_name='trainer-script.sh'):
    """
    Given the filepath for the trainer-script, load and return its contents as a str.
    :param s3_training_bucket:
    :param trainer_script_name:
    :return:
    """

    try:
        # If the user didn't pass in another location to pull in the trainer-script from, grab the one in this package.
        if not s3_training_bucket:
            userdata_filepath = 'src/{}'.format(trainer_script_name)
            with open(userdata_filepath, 'r') as f:
                userdata_script = f.read()

        else:
            # If a value was passed in, assume it to be an S3 key - retrieve its contents.
            client_s3 = boto3.client('s3')
            s3_response = client_s3.get_object(
                Bucket=s3_training_bucket,
                Key=trainer_script_name
            )

            userdata_script = s3_response['Body'].read().decode('utf-8')

        return userdata_script

    except Exception as e:
        err = 'userdata_loader failure: {}'.format(e)
        logging.error(err)
        return False


def stack_creator(testmode=False):
    """
    The meat of this script, this launches the CFN stack based on the template and userdata script passed in.
    If this was launched with the testmode parameter set, validate the CFN template instead. Note that this does NOT
    check the use of the userdata script.
    :param testmode:
    :return:
    """
    try:
        logging.debug('stack_creator starting.')
        msg = ''

        # It's okay if you're not planning to use an S3 bucket - this will be a blank string and the functions will
        # handle that properly.
        s3_training_bucket = os.environ.get('s3_training_bucket', '')

        # Get the training config, either from the S3 training bucket or from the Lambda package.
        training_config = parse_training_config(
            training_config_path=s3_training_bucket
        )

        cfn_template_contents = template_loader(
            template_path=s3_training_bucket,
            cloudformation_template_filename=training_config.get('cloudformation_template_filename', ''))

        userdata_script = userdata_loader(
            s3_training_bucket=s3_training_bucket,
            trainer_script_name=training_config.get('training-script-filename', '')
        )

        client_cfn = boto3.client('cloudformation')

        if testmode:
            create_stack_response = client_cfn.validate_template(
                TemplateBody='{}'.format(cfn_template_contents)
            )

            msg = 'CloudFormation template passed validation!'
        else:
            create_stack_response = client_cfn.create_stack(
                StackName='parris-stack',
                TemplateBody='{}'.format(cfn_template_contents),
                OnFailure='DELETE',
                Parameters=[
                    {
                        'ParameterKey': 'UserDataScript',
                        'ParameterValue': str(userdata_script)
                    },
                    {
                        'ParameterKey': 'InstanceType',
                        'ParameterValue': training_config.get('instance-type', '')
                    },
                    {
                        'ParameterKey': 'SecurityGroupId',
                        'ParameterValue': training_config.get('security-group-id', '')
                    },
                    {
                        'ParameterKey': 'SubnetId',
                        'ParameterValue': training_config.get('subnet-id', '')
                    },
                    {
                        'ParameterKey': 'KeyPairNames',
                        'ParameterValue': training_config.get('ec2-keypair-name', '')
                    }
                ]
            )

            msg = 'CloudFormation stack has started launching successfully!'

        logging.warning(msg)
        return True, msg
    except Exception as e:
        err = 'stack_creator failure: {}'.format(e)
        logging.error(err)
        return False, err


def _test_stack_creator():
    """
    Launch a stack with a test userdata script.
    :return:
    """
    stack_creator_passfail, stack_creator_msg = stack_creator(testmode=True)
    if not stack_creator_passfail:
        logging.error('_test_stack_creator() Failed: {}'.format(stack_creator_msg))
    return


def lambda_handler(event, context):
    """
    The function intended to be kicked off when loaded up by AWS Lambda. Takes the expected event and context arguments.
    :param event:
    :ptype event: dict, list, str, int, float, or NoneType
    :param context:
    :ptype context: LambdaContext
    :return:
    """

    logging.debug('Got invocation from Lambda event: {}'.format(str(event)))

    # If you'd like to have the handler return some values (for example, for integration into a custom training-job
    # dashboard from which one can launch new training stacks), you can set those here. For now, it just returns an
    # empty dict.
    return_values = {}

    stack_creator_passfail, stack_creator_msg = stack_creator()
    if not stack_creator_passfail:
        err_msg = 'stack_creator() Failed: {}'.format(stack_creator_msg)
        logging.error(err_msg)
        raise Exception(err_msg)

    return return_values


def _test_userdata_loader():
    """
    Test that the trainer-script.sh file is loaded properly. Particularly handy for verifying S3 files are reachable.
    :return:
    """
    try:
        s3_training_bucket = 'com.jgreenemi.mlbucket'
        training_config = parse_training_config(s3_training_bucket)
        userdata_script = userdata_loader(
            s3_training_bucket,
            training_config.get('training-script-filename', '')
        )

        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    _test_userdata_loader()
    _test_stack_creator()
    logging.warning('Tests finished!')
