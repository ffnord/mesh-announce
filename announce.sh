#!/bin/sh

ALFRED_DATA_TYPE=158

"$(dirname "$0")"/announce.py -d "$(dirname "$0")"/announce.d/ | gzip | alfred -s ${ALFRED_DATA_TYPE}
