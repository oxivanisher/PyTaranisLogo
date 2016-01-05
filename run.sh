#!/bin/bash

# Getting script directory.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Saving origin path.
ORIGDIR=$(pwd)

# Cleaning old .pyc files to not run into the "importing seems to work" trap again!
find ${DIR} -name "*.pyc" -exec rm {} \;

# Changing to the root path of th application.
cd ${DIR}

# Checking if TARANISLOGO_CFG is set. If not, use the provided example file.
if [ -z "$TARANISLOGO_CFG" ]; then
	if [ -f "dist/pytaranislogo.cfg" ]; then
		echo "Setting TARANISLOGO_CFG for you. Please use your own settings for production!"
		export TARANISLOGO_CFG="../dist/pytaranislogo.cfg"
	else
		export TARANISLOGO_CFG="../dist/pytaranislogo.cfg.example"
	fi
fi

# Actually starting the application.
python pytaranislogo.py

# Changing back to origin path.
cd ${ORIGDIR}