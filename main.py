#!/usr/bin/env python
""" Short description of this Python module.

Longer description of this module.

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

__author__ = "One solo developer"
__authors__ = ["One developer", "And another one", "etc"]
__contact__ = "mail@example.com"
__copyright__ = "Copyright $YEAR, $COMPANY_NAME"
__credits__ = ["One developer", "And another one", "etc"]
__date__ = "YYYY/MM/DD"
__deprecated__ = False
__email__ =  "mail@example.com"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"

import os
import sys
from azure.cli.core import get_default_cli
from dotenv import load_dotenv

import console_helper


def check_azure_login(az_cli, subscription_id):
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
    #Get subscription info if logged in
    account_response = az_cli.invoke(['account', 'show', '--subscription', subscription_id])
    if account_response == 0:
        subscription_name = az_cli.result.result['name']
        # pylint: disable=line-too-long
        console_helper.print_confirmation_message(f"Deploying into subscription: '{subscription_name}' with Id: '{subscription_id}'")
    else:
        # pylint: disable=line-too-long
        console_helper.print_warning_message('You are not logged in to Azure CLI. Attempting to login...')
        az_cli.invoke(['login'])
        az_cli.invoke(['account', 'set', '--subscription', subscription_id])



def main():
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/
    
    """
    #check we are running the deploy script from a virtual environment.
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

    #get the cli instance
    az_cli = get_default_cli()

    # Retrieve Azure values from environment variables.
    subscription_id = os.getenv("SUBSCRIPTION_ID")
    #source_resource_group = os.getenv("SOURCE_RESOURCE_GROUP_NAME")
    #target_subscription_id = os.getenv("TARGET_AZURE_SUBSCRIPTION_ID")
    #target_resource_group = os.getenv("TARGET_RESOURCE_GROUP_NAME")

    #account_response = az_cli.invoke(['account', 'show', '--subscription', subscription_id])
    #Login to Azure for the given Subscription
    #check_azure_login(az_cli, subscription_id)



if __name__ == "__main__":
    main()
    