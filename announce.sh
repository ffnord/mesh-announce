#!/bin/bash

DIR="$(dirname "$0")"

while test $# -gt 0; do
  case $1 in
    -i)
      shift
      ip link show dev $1 > /dev/null
      test $? -ne 0 && exit
      INTERFACE="-i $1"
      ;;
    -b)
      shift
      ip link show dev $1 > /dev/null
      test $? -ne 0 && exit
      BATADV="-b $1"
      ;;
    -h|--help)
      echo "Usage: $0 [-i <ifname>] [-b <batadv-dev>]"
      exit
      ;;
  esac
  shift
done

"${DIR}"/announce.py -d "${DIR}"/nodeinfo.d/ ${BATADV} | gzip | alfred $INTERFACE -s 158
"${DIR}"/announce.py -d "${DIR}"/statistics.d/ ${BATADV} | gzip | alfred $INTERFACE -s 159
