#!/bin/sh

#
ROOT=`dirname $0`

DBDIR=$ROOT/db

CDIR=/tmp/apple_health_export
cd $CDIR

if test ! -f export.xml.orig; then
    mv export.xml export.xml.orig
fi

if test "$1" = "--clean"; then
    rm -f apple_health_export_?????.csv
fi

if test "$1" = ""; then
    YEARS="2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024"
else
    YEARS="$1"
fi

SCRIPT=/tmp/script
CSVFILE=$HOME/python/healthcare/db/apple_health_export.csv

cat<<EOF> $SCRIPT.a
BEGIN{
    out = 1
}
{
   pos = index(\$0, "startDate=")
   str = substr(\$0, pos, 10)

   if (\$1 == "<Record" && str == "startDate=") {

      closepos = index(\$0, "/>")

      year = substr(\$0, pos + 11, 4)
      month = substr(\$0, pos + 16, 2)

      if ( !(year == YEAR && month < "07")) {
 	 if (closepos == 0) {
	   out = 0
	 } else {
	   out = 2
      	 }
      }
   }


   if (out == 1) {
      print \$0
   }

   if (out == 2) {
      out = 1
   }

   if (\$1 == "</Record>") {
      out = 1
   }

}
END{
}
EOF

cat<<EOF> $SCRIPT.b
BEGIN{
    out = 1
}
{
   pos = index(\$0, "startDate=")
   str = substr(\$0, pos, 10)

   if (\$1 == "<Record" && str == "startDate=") {

      closepos = index(\$0, "/>")

      year = substr(\$0, pos + 11, 4)
      month = substr(\$0, pos + 16, 2)

      if ( !(year == YEAR && month >= "07")) {
 	 if (closepos == 0) {
	   out = 0
	 } else {
	   out = 2
      	 }
      }
   }


   if (out == 1) {
      print \$0
   }

   if (out == 2) {
      out = 1
   }

   if (\$1 == "</Record>") {
      out = 1
   }

}
END{
}
EOF


DATE=`date +%Y-%m-%d`

for YEAR in $YEARS; do

    if test -f $DBDIR/apple_health_export_"$YEAR"a.csv; then
	cp $DBDIR/apple_health_export_"$YEAR"a.csv .
    fi
    
    if test ! -f apple_health_export_"$YEAR"a.csv; then
	echo "making... "$YEAR"a.csv"
	cat export.xml.orig | awk -v YEAR=$YEAR -f $SCRIPT.a > export.xml
	python $ROOT/Simple-Apple-Health-XML-to-CSV/apple_health_xml_convert.py
	cat apple_health_export_$DATE.csv | awk -F '[,]' '{if($1!="" && $3!=""){printf "%s,%s,%s,%s,%s\n", $1,$2,$3,$4,$5}}' > apple_health_export_"$YEAR"a.csv
	rm -f apple_health_export_$DATE.csv
    fi

    ####
    
    if test -f $DBDIR/apple_health_export_"$YEAR"b.csv; then
	cp $DBDIR/apple_health_export_"$YEAR"b.csv .
    fi
    
    if test ! -f apple_health_export_"$YEAR"b.csv; then
	echo "making... "$YEAR"b.csv"
	cat export.xml.orig | awk -v YEAR=$YEAR -f $SCRIPT.b > export.xml
	python $ROOT/Simple-Apple-Health-XML-to-CSV/apple_health_xml_convert.py
	cat apple_health_export_$DATE.csv | awk -F '[,]' '{if($1!="" && $3!=""){printf "%s,%s,%s,%s,%s\n", $1,$2,$3,$4,$5}}' > apple_health_export_"$YEAR"b.csv
	rm -f apple_health_export_$DATE.csv
    fi
done

echo "type,sourceName,value,unit,startDate" > $CSVFILE

for F in apple_health_export_?????.csv; do
    grep -v "^type," $F >> $CSVFILE
done

exit 0

# end
