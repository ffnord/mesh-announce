#!/bin/sh

ALFRED_DATA_TYPES="158"

DIR="$(dirname "$0")"

for ALFRED_DATA_TYPE in ${ALFRED_DATA_TYPES}; do
	"${DIR}"/announce.py -d "${DIR}"/announce.${ALFRED_DATA_TYPE}.d/ | gzip | alfred -s ${ALFRED_DATA_TYPE}
done
