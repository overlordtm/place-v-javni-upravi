#!/usr/bin/env bash

fetch() {
    YEAR=$1
    MONTH=$2
    FILE=$(printf "data/%d/%d-%02d-DM" $YEAR $YEAR $MONTH)
    mkdir -p $(dirname $FILE)
    curl -s http://www.pportal.gov.si/ISPAP_${YEAR}/${MONTH}_${YEAR}/DM/DM_VSI_BRUTOPLACA${MONTH}.txt | recode html.. | jq '.aaData' > ${FILE}.json
    echo "Podskupina,Šifra PU,Naziv PU,Šifra DM,Naziv DM,Zaposlitve plača,Bruto plača,Tip C,Tip D,Tip E,Tip F,Tip I,Tip J,Tip O" > ${FILE}.csv
    in2csv -I -H ${FILE}.json | tail -n +2 >> ${FILE}.csv
    rm ${FILE}.json
}

fetch $1 $2