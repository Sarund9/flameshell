#!/bin/bash

source venv/bin/activate

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "$SCRIPT_DIR/config.py"

ignis init -c "$SCRIPT_DIR/config.py"

