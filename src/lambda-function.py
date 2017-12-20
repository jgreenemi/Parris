# Create

import base64
import boto3
import json
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

        return True, msg
    except Exception as e:
        err = 'Exception: {}'.format(e)
        return False, err


def _test_stack_creator():
    """
    Launch a stack with a test userdata script.
    :return:
    """
    stack_creator_passfail, stack_creator_msg = stack_creator(testmode=True)
    if not stack_creator_passfail:
        print('_test_stack_creator() Failed: {}'.format(stack_creator_msg))
    return


def lambda_handler():
    """
    The function intended to be kicked off when loaded up by AWS Lambda.
    :return:
    """

    stack_creator_passfail, stack_creator_msg = stack_creator()
    if not stack_creator_passfail:
        print('stack_creator() Failed: {}'.format(stack_creator_msg))
    return


if __name__ == '__main__':
    _test_stack_creator()
    print('_test_stack_creator() passed!')
