#!/bin/sh

#
ROOT=`dirname $0`

if test "$1" = "--clean"; then
    rm -f apple_health_export_????a.csv
fi

SCRIPT=/tmp/script

cat<<EOF> $SCRIPT
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

      # if ( !(year == YEAR && month < "07")) {
      # if ( !(year == YEAR && month >= "07")) {
      if ( year != YEAR) {

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

# YEAR=2017
# head -1000000 export.xml.orig | awk -v YEAR=$YEAR -f $SCRIPT
# exit 0

DATE=`date +%Y-%m-%d`

# for YEAR in 2017; do
for YEAR in 2013 2014 2015 2016     2018 2019 2020 2021 2022 2023; do
    if test ! -f apple_health_export_"$YEAR"a.csv; then
	cat export.xml.orig | awk -v YEAR=$YEAR -f $SCRIPT > export.xml
	python $ROOT/Simple-Apple-Health-XML-to-CSV/apple_health_xml_convert.py
	mv apple_health_export_$DATE.csv apple_health_export_"$YEAR"a.csv
    fi
done

cat<<EOF > apple_health_export_$DATE.csv
type,sourceName,value,unit,startDate,endDate,creationDate,HKMetadataKeyHeartRateRecoveryMaxObservedRecoveryHeartRate,HKMetadataKeySessionEstimate,HKWeatherTemperature,HKMetadataKeyBarometricPressure,Asleep,HKDeviceSerialNumber,HKMetadataKeySyncIdentifier,Withings Link,stagesLight,HKWorkoutEventTypePause,Lights,stagesDeep,HKWeatherHumidity,HKDeviceManufacturerName,WorkoutSource,HKMetadataKeyHeartRateRecoveryActivityDuration,HKExternalUUID,HKWorkoutEventTypeResume,Deep Sleep,appleMoveTimeGoal,Daytime HR,appleStandHours,HKMetadataKeyAppleDeviceCalibrated,FitzpatrickSkinType,HKElevationAscended,HKAlgorithmVersion,DateOfBirth,HKDeviceName,CompanionActivityStoreID,CompanionGeolocationID,HKVO2MaxTestType,appleMoveTime,Max RespRate,SequenceNumber,duration,Withings User Identifier,HKTimeZone,HKAverageMETs,activeEnergyBurnedGoal,HKMetadataKeyUserMotionContext,HKMetadataKeyHeartRateRecoveryActivityType,Rating,StartDateLocal,appleExerciseTimeGoal,appleStandHoursGoal,device,sourceVersion,appleExerciseTime,Recharge,HKWorkoutBrandName,HKMetadataKeyHeartRateRecoveryTestType,HKDateOfEarliestDataUsedForEstimate,stagesREM,dateComponents,UserNumber,Min RespRate,Average HR,workoutActivityType,CardioFitnessMedicationsUse,Modified Date,stagesAwake,HKHeartRateEventThreshold,durationUnit,Energy Threshold,Average RespRate,Health Mate App Version,activeEnergyBurned,stagesSleep,HKMetadataKeyHeartRateMotionContext,HKWasUserEntered,BiologicalSex,HKMetadataKeySyncVersion,HKMetadataKeyDevicePlacementSide,Nap,HKIndoorWorkout,activeEnergyBurnedUnit,BloodType,meta
EOF

for F in apple_health_export_?????.csv; do
    grep -v "^type," $F >> apple_health_export_$DATE.csv
done

exit 0

# end
