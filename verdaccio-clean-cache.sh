#!/bin/bash
set -e

PATH=/home/user/bin
FOLDER_PATH=""
MODULE=""
SIDEUSER=""

/bin/mv "$FOLDER_PATH"/"$MODULE"/ /tmp/
/bin/rm -rf "$FOLDER_PATH"/*
/bin/mv /tmp/"$MODULE" "$FOLDER_PATH"


/usr/bin/su - $SIDEUSER -c 'pm2 stop verdaccio'
/usr/bin/su - $SIDEUSER -c 'pm2 start verdaccio'
