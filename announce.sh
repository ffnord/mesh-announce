#!/bin/sh

ALFRED_DATA_TYPE=158

DIR="$(dirname "$0")"

"${DIR}"/announce.py -d "${DIR}"/announce.d/ | gzip | alfred -s ${ALFRED_DATA_TYPE}
