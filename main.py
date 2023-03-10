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
from azure.cli.core import get_default_cli
from dotenv import load_dotenv
import console_helper

import azlogin
import azdeploy



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
    azlogin.check_azure_login(az_cli, subscription_id)

    # get the environment variables from the .env file.
    template_parameters = {
        'environment': {'value': environment},
        'location': {'value': location},
        'resource_group_name': {'value': resource_group_name}
    }

    #do the deployment
    azdeploy.deploy_template(az_cli,
                    "main.bicep", 
                    location,
                    template_parameters)

# Main check
if __name__ == "__main__":
    main()
    