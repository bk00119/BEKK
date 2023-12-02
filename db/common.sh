#!/bin/sh
# Some common shell stuff.

# 1) NEED MongoDB Database Tools (https://www.mongodb.com/try/download/database-tools)
# 2) run `ln -s [MongoDB Database Tools Directory]/mongoexport /usr/local/bin/mongoexport`
# 3) run `ln -s [MongoDB Database Tools Directory]/mongoimport /usr/local/bin/mongoimport`

echo "Importing from common.sh"

DB=BEKK
# USER=bekk-developers
# CONNECT_STR="bekk.ugoqoaw.mongodb.net/?retryWrites=true&w=majority"
if [ -z $DATA_DIR ]
then
    # DATA_DIR=/Users/briankim/Documents/GitHub/BEKK/db
    DATA_DIR=$PYTHONPATH/db
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $CLOUD_MONGO_PW ]
then
    echo "You must set CLOUD_MOGNO_PW in your env before running this script."
    exit 1
fi


declare -a DBCollections=("tasks" "users")