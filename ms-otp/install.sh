#!/bin/bash

python3.10 -m venv .
source bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt