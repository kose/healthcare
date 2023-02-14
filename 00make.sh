#!/bin/sh

# 内容一覧
# https://qiita.com/swrn364/items/9a2ebe65b60e76c89be1

DATE=`date +%Y-%m-%d`

ORIG=/tmp/apple_health_export/apple_health_export_$DATE.csv

if test "$1" = "--clean"; then
    rm -f /tmp/*.csv
fi

mkdir -p images db

##
## 体温
##
CSV=/tmp/body-temperature.csv
IMG=images/body-temperature.png

if test -f $CSV; then
    echo "$CSV exist"
else
    head -1 $ORIG > $CSV
    grep "BodyTemperature" $ORIG >> $CSV
fi

if test $IMG -nt $CSV; then
    echo "$IMG exist"
else
    rm -f $IMG
    python body_temperature.py
fi


##
## 体重
##
CSV=/tmp/body-mass.csv
IMG=images/body-mass.png

if test -f $CSV; then
    echo "$CSV exist"
else
    head -1 $ORIG > $CSV
    grep "BodyMass," $ORIG >> $CSV
fi

if test $IMG -nt $CSV; then
    echo "$IMG exist"
else
    rm -f $IMG
    python body_mass.py
fi


##
## 歩行距離
##
CSV=/tmp/distance-walking.csv
IMG=images/distance-walking.png

if test -f $CSV; then
    echo "$CSV exist"
else
    head -1 $ORIG > $CSV
    # grep "DistanceWalkingRunning," $ORIG | grep "km,202" >> $CSV
    grep "DistanceWalkingRunning," $ORIG | grep "iPhone" >> $CSV
fi

if test $IMG -nt $CSV; then
    echo "$IMG exist"
else
    rm -f $IMG
    python distance_walking.py
fi

##
## 血圧
##
CSV=/tmp/blood-pressure-sbp.csv

if test -f $CSV; then
    echo "$CSV exist"
else
    head -1 $ORIG > $CSV
    grep "BloodPressureSystolic," $ORIG >> $CSV
fi

##
##
##
CSV=/tmp/blood-pressure-dbp.csv
IMG=images/blood-pressure.png

if test -f $CSV; then
    echo "$CSV exist"
else
    head -1 $ORIG > $CSV
    grep "BloodPressureDiastolic", $ORIG >> $CSV
fi

##
if test $IMG -nt $CSV; then
    echo "$IMG exist"
else
    rm -f $IMG
    python blood_pressure.py
fi

# join image
if test images/blood-pressure.png -nt images/helthcare.png; then
    python join-images.py
fi

# % grep "DistanceWalkingRunning" apple_health_export_2022-08-25.csv | awk -F "," '{pr2}' | sort | uniq
# Apple Watch S2
# Apple Watch S4
# Apple Watch S6
# Nike Run Club
# Pokémon GO
# Walkmetrix
# iPhoneSE
# iPhoneXs
# ヘルスケア

exit 0



# end
