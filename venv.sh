#!/bin/bash

# Setup python Virtual Environment.
python -m venv venv
source venv/bin/activate

# Install Dependencies.
pip install wayfire
pip install git+https://github.com/ignis-sh/ignis.git



