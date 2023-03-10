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


import sys
import re
#from azure.cli.core import get_default_cli
import console_helper

def check_valid_subscription_id(subscription_id: str) -> bool:
    '''
    checks for a valid Azure Subscription ID - Format 00000000-0000-0000-0000-000000000000
    '''
    # check if a string
    if isinstance(subscription_id, str):
        # pylint: disable=line-too-long
        # pylint: disable=anomalous-backslash-in-string
        re_result = re.search("^(\{{0,1}([0-9a-fA-F]){8}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}\}{0,1})$", subscription_id)
        if re_result:
            return True

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
    if check_valid_subscription_id(subscription_id):
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
    else:
        console_helper.print_error_message("##ERROR - Invalid SubscriptionID!")
        sys.exit(-1)
