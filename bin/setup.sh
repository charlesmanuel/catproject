#!/bin/bash
#
#scrape
#
#
python3 -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install schedule
python3 scraper.py