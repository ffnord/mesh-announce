#!/bin/sh

DIR="$(dirname "$0")"

"${DIR}"/announce.py -d "${DIR}"/announce.d/nodeinfo/ | gzip | alfred -s 158
"${DIR}"/announce.py -d "${DIR}"/announce.d/statistics/ | gzip | alfred -s 159
