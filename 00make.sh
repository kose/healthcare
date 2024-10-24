#!/bin/sh

# 内容一覧
# https://qiita.com/swrn364/items/9a2ebe65b60e76c89be1

DBFILE=$HOME/python/healthcare/db/apple_health_export.csv

if test "$1" = "--clean"; then
    rm -f images/*.png
    rm -f db/*2024*.csv
fi

##
DATE=`date +%Y`

if test ! -f /tmp/apple_health_export/apple_health_export_"$DATE"b.csv; then
    echo "Do 01make_DB.sh"
    sh $HOME/python/healthcare/01make_DB.sh
fi

cd $HOME/python/healthcare

mkdir -p images db

if test $DBFILE -nt images/healthcare.png; then
    rm -f images/*.png

    echo "make healthcare.png"
    python healthcare.py
fi

if test images/healthcare.png -nt $HOME/GoogleDrive/データ/healthcare.png; then
    echo "cp images/healthcare.png $HOME/GoogleDrive/データ/healthcare.png"
    cp images/healthcare.png $HOME/GoogleDrive/データ/healthcare.png
else
    echo "healthcare.png upto date"
fi

exit 0

# end
