#!/bin/sh

# 内容一覧
# https://qiita.com/swrn364/items/9a2ebe65b60e76c89be1

if test "$1" = "--clean"; then
    rm -f images/*.png
    rm -f db/*2023*.csv
fi

mkdir -p images db

python healthcare.py

exit 0

# end
