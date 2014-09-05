#!/bin/sh

DIR="$(dirname "$0")"

"${DIR}"/announce.py -d "${DIR}"/nodeinfo.d/ | gzip | alfred -s 158
"${DIR}"/announce.py -d "${DIR}"/statistics.d/ | gzip | alfred -s 159
