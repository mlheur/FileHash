#!/bin/ksh
clear
cd `dirname $0`
for F in *py; do
  echo '########################################'
  echo '### '"$F"
  echo '########################################'
  ./"$F"
  echo
  echo
done
cd ->/dev/null
