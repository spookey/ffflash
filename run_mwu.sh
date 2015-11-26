#!/bin/bash

CDIR=$(cd "$(dirname "$0")"; pwd)
FLASH="$CDIR/ffflash.py"

function run()
{
    WWWDIR="$1"
    APIFILE="$2"
    NODELIST="$3"

    $FLASH \
        "$WWWDIR/$APIFILE" \
        "-n" "$NODELIST" \
        "-s" \
            "$WWWDIR/inc/contact.yaml" \
            "$WWWDIR/inc/services.yaml" \
            "$WWWDIR/inc/support.club.yaml" \
            "$WWWDIR/inc/support.donations.campaigns.yaml" \
            "$WWWDIR/inc/timeline.yaml"

    if [ $? -ne 0 ]; then echo "# error processing $APIFILE"; fi
}


run "/var/www/ffapi-wiesbaden" "ffapi_wi.json" "/var/www/meshviewer-extern-wi/build/data/nodelist.json"
run "/var/www/ffapi-mainz" "ffapi_mz.json" "/var/www/meshviewer-extern-mz/build/data/nodelist.json"
