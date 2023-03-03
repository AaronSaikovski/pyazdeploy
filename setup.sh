#!/bin/sh

#create a blank .env file
touch .env
echo "SUBSCRIPTION_ID=''" > .env

#setup the virtual environment
python3 -m venv .venv 

#activate the virtual environment
source .venv/bin/activate

#install packages
pip install -r requirements.txt

#upgrade PIP
pip install --upgrade pip

#activate the virtual environment
source .venv/bin/activate

