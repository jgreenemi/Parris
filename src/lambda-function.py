# Create the CloudFormation stack with the trainer-script loaded.

import boto3
import json
import logging
from pprint import pprint


def template_loader():
    """
    Given the filepath for the CloudFormation template, load and return it as a dict.
    :return:
    """
    cfn_template_contents = json.load(open('config/cloudformation.json'))

    return cfn_template_contents


def userdata_loader(testmode=False):
    """
    Given the filepath for the trainer-script, load and return its contents as a str.
    :param testmode:
    :return:
    """
    if testmode:
        userdata_filepath = 'target/userdata-confirmation-example.sh'
    else:
        userdata_filepath = 'src/trainer-script.sh'

    with open(userdata_filepath, 'r') as f:
        userdata_script = f.read()

    return userdata_script


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

        if testmode:
            cfn_template_contents = template_loader()
            userdata_script = userdata_loader(testmode)
            client_cfn = boto3.client('cloudformation')
            create_stack_response = client_cfn.validate_template(
                TemplateBody='{}'.format(cfn_template_contents)
            )

            msg = 'CloudFormation template passed validation!'

        else:
            cfn_template_contents = template_loader()
            userdata_script = userdata_loader(testmode)
            client_cfn = boto3.client('cloudformation')
            create_stack_response = client_cfn.create_stack(
                StackName='parris-stack',
                TemplateBody='{}'.format(cfn_template_contents),
                OnFailure='DELETE',
                Parameters=[
                    {
                        'ParameterKey': 'UserDataScript',
                        'ParameterValue': str(userdata_script)
                    }
                ]
            )

            msg = 'CloudFormation stack has started launching successfully!'

        logging.warning(msg)
        return True, msg
    except Exception as e:
        err = 'Exception: {}'.format(e)
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


if __name__ == '__main__':
    _test_stack_creator()
    logging.warning('_test_stack_creator() passed!')
