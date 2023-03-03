#!/usr/bin/env python
""" A python script to deploy an Azure Bicep or ARM Template.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "Aaron Saikovski"
__contact__ = "asaikovski@outlook.com"
__date__ = "2023/03/03"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Testing"
__version__ = "0.0.1"

import os
import sys
import json
import pprint
from azure.cli.core import get_default_cli
from dotenv import load_dotenv
import console_helper


def check_azure_login(az_cli: object, subscription_id: str) -> None:
    """Checks to see if we are logged into Azure, will login if not logged in.
    Parameters
    ----------
    az_cli : object 
        Azure CLI Object
    subscription_id : string
        Azure Subscription ID

    Returns
    -------
    nothing
        Logs in if not logged on
    """
    # Check if Subscription is valid
    if len(subscription_id) == 0:
        console_helper.print_error_message("##ERROR - SubscriptionID is blank!")
        sys.exit(-1)

    # Get subscription info if logged in
    account_response = az_cli.invoke(['account', 'show', '--subscription', subscription_id])
    if account_response == 0:
        subscription_name: str = az_cli.result.result['name']
        # pylint: disable=line-too-long
        console_helper.print_confirmation_message(f"Deploying into subscription: '{subscription_name}' with Id: '{subscription_id}'")
    else:
        # pylint: disable=line-too-long
        console_helper.print_warning_message('You are not logged in to Azure CLI. Attempting to login...')
        az_cli.invoke(['login'])
        az_cli.invoke(['account', 'set', '--subscription', subscription_id])


def deploy_template(az_cli: object,
                    template_name: str,
                    location: str,
                    template_params: dict) -> None:
    """Deploys an ARM or Bicep template with given parameters.
    Parameters
    ----------
    az_cli : object 
        Azure CLI Object
    template_name : string
        Template name/path to deploy
    location : string
        Azure region to deploy to
    template_params: dict
        Parameter dictionary to pass into the deployment.

    Returns
    -------
    nothing
        Displays output status of the deployment.
    """
    # Do the deployment
    az_cli.invoke(['deployment',
            'sub',
            'create',
            '-l',
            location,
            '--template-file',
            template_name,
            '--parameters',
            json.dumps(template_params)
            ])

    # Check for deployment results.
    if not az_cli.result.result['properties']['error']:
        console_helper.print_ok_message("Successfully deployed the template deployment.")
    else:
        # pylint: disable=line-too-long
        console_helper.print_error_message("Failed to deploy the template deployment. Review the error message below:")
        pprint.pprint(az_cli.result.result)
        sys.exit(-1)


def main() -> None:
    """Main function.

    Returns
    -------
    None
    """
    # check we are running the deploy script from a virtual environment.
    if sys.prefix != sys.base_prefix:
        console_helper.print_confirmation_message("You are running in a virtual environment.")
    else:
        console_helper.print_warning_message("This is not a virtual environment!")
        print('Run the following command to create a virtual environment.')
        console_helper.print_command_message("python -m venv venv")
        print('Then activate the virtual environment')
        sys.exit()

    # take environment variables from .env.
    load_dotenv()

    # get the cli instance
    az_cli = get_default_cli()

    # Retrieve Azure values from environment variables.
    subscription_id: str = os.getenv("SUBSCRIPTION_ID")
    resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
    location = os.getenv("LOCATION")
    environment = os.getenv("ENVIRONMENT")

    # Login to Azure for the given Subscription
    check_azure_login(az_cli, subscription_id)

    # get the environment variables from the .env file.
    template_parameters = {
        'environment': {'value': environment},
        'location': {'value': location},
        'resource_group_name': {'value': resource_group_name}
    }

    #do the deployment
    deploy_template(az_cli,
                    "main.bicep", 
                    location,
                    template_parameters)

# Main check
if __name__ == "__main__":
    main()
    