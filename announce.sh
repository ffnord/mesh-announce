#!/bin/sh

DIR="$(dirname "$0")"

case $1 in
  -i)
    shift
    ip link show dev $1 > /dev/null
    test $? -ne 0 && exit
    INTERFACE="-I $1"
    ;;
  -h|--help)
    echo "Usage: $0 [-i <ifname>]"
    exit
    ;;
esac

"${DIR}"/announce.py -d "${DIR}"/nodeinfo.d/ | gzip | alfred $INTERFACE -s 158
"${DIR}"/announce.py -d "${DIR}"/statistics.d/ | gzip | alfred $INTERFACE -s 159
