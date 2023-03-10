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
import json
import pprint

import console_helper


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
        console_helper.print_ok_message("Successfully deployed the template.")
    else:
        # pylint: disable=line-too-long
        console_helper.print_error_message("Failed to deploy the template deployment. Review the error message below:")
        pprint.pprint(az_cli.result.result)
        sys.exit(-1)
        