#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import japanize_matplotlib

import cv2 as cv

csvfile = "db/apple_health_export.csv"

from datetime import date
this_month = date.today().strftime("%Y%m")
begin_date = "2013-08-25"



def blood_pressure(df_sbp, df_dbp):

    pngfile="images/blood-pressure.png"

    ##
    ## 集計したDataFrameを作る
    ##
    begin_month = "201308"
    savecsvfile="db/blood-pressure_" + begin_month + "-" + this_month + ".csv"

    
    def make_df(df, name):

        date = pd.to_datetime(df.startDate).values
        value = df.value.values
        value = value.astype(None)  # なぜかtypeがobjectになってるので。

        df2 = pd.DataFrame(index=date, data={name:value})

        # 日ごと平均 (日付順に並べ替えられる）
        # df2 = df2.resample(rule="D").mean()

        # 日ごとmax() (日付順に並べ替えられる）
        df2 = df2.resample(rule="D").max()

        return df2

    
    df = make_df(df_sbp, "SBP")
    df_dbp = make_df(df_dbp, "DBP")

    # 列で結合
    df["DBP"] = df_dbp.DBP.values

    # csvファイル書き出し（データバックアップのため）
    # df.to_csv(savecsvfile)

    ##
    ## グラフ
    ##
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 4), dpi=144)

    df['month'] = pd.to_datetime(df.index).strftime('%Y-%m')
    df.boxplot(column="SBP", by='month', rot=90, ax=ax, whis=10.0, color='#1f77b4')
    df.boxplot(column="DBP", by='month', rot=90, ax=ax, whis=10.0, color='#ff7f0e')

    ax.set_title("")
    ax.set_xlabel("")
    ax.grid(which="major", axis="x", color="gray", alpha=0.5, linestyle=":", linewidth=1)
    ax.grid(which="major", axis="y", color="gray", alpha=0.5, linestyle=":", linewidth=1)
    plt.suptitle("血圧（月ごとの箱髭図）")
    ax.set_ylabel("mmHg")

    plt.locator_params(axis='x', nbins=35) #x軸，x個以内．
    plt.subplots_adjust(left=0.04, right=0.98, bottom=0.2, top=0.92)

    if not(os.path.isfile(pngfile)):
        plt.savefig(pngfile)

    plt.pause(5)



def body_temperature(df):

    pngfile="images/body-temperature.png"

    ##
    ## 集計したDataFrameを作る
    ##
    begin_month = "202004"
    savecsvfile="db/body-temperature_" + begin_month + "-" + this_month + ".csv"

    date = pd.to_datetime(df.startDate).values
    value = df.value.values
    value = value.astype(None)  # なぜかtypeがobjectになってるので。

    # 時系列を最長に合わせる
    length = len(date)
    date = np.insert(date, length, pd.to_datetime(begin_date))
    value = np.insert(value, length, np.nan)

    df2 = pd.DataFrame(index=date, data={"BodyTemperature":value})

    # 日ごと平均 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").mean()

    # csvファイル書き出し（データバックアップのため）
    # df2.to_csv(savecsvfile)

    ##
    ## グラフ
    ##
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 3), dpi=144)

    # Nanを補完
    df2 = df2.interpolate()

    df2['month'] = pd.to_datetime(df2.index).strftime('%Y-%m-%W')
    df2.boxplot(column="BodyTemperature", by='month', rot=70, ax=ax, whis=10.0, color='#1f77b4') 

    ax.set_title("")
    ax.set_xlabel("")
    ax.set_ylim([35.0, 37.0])
    ax.grid(which="major", axis="x", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    ax.grid(which="major", axis="y", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    plt.suptitle("体温（週ごとの箱髭図）")
    ax.set_ylabel("°C")

    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.33, top=0.90)
    plt.locator_params(axis='x', nbins=16) #x軸，x個以内．

    if not(os.path.isfile(pngfile)):
        plt.savefig(pngfile)

    plt.pause(5)


def body_mass(df):

    pngfile="images/body-mass.png"
    
    ##
    ## 集計したDataFrameを作る
    ##

    begin_month = "201308"
    savecsvfile="db/body-mass_" + begin_month + "-" + this_month + ".csv"

    date = pd.to_datetime(df.startDate).values
    value = df.value.values
    value = value.astype(None)  # なぜかtypeがobjectになってるので。

    # 時系列を最長に合わせる
    length = len(date)
    date = np.insert(date, length, pd.to_datetime(begin_date))
    value = np.insert(value, length, np.nan)

    df2 = pd.DataFrame(index=date, data={"mean weekly":value})

    # 日ごと平均 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").mean()

    # csvファイル書き出し（データバックアップのため）
    # df2.to_csv(savecsvfile)

    ##
    ## グラフ
    ##
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 2.5), dpi=144)

    # Nanを補完
    df2 = df2.interpolate()

    # 週平均
    df2 = df2.resample(rule="W").mean()
    plt.suptitle("体重（週の平均）")

    # 月平均
    # df2 = df2.resample(rule="M").mean()
    # plt.suptitle("体重（月平均）")

    df2.plot(ax=ax)

    ax.set_title("")
    ax.set_xlabel("")
    ax.grid(which="major", axis="x", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    ax.grid(which="major", axis="y", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    ax.set_ylabel("kg")

    plt.subplots_adjust(left=0.04, right=0.98, bottom=0.15, top=0.89)
    plt.locator_params(axis='x', nbins=16) #x軸，x個以内．

    if not(os.path.isfile(pngfile)):
        plt.savefig(pngfile)

    plt.pause(5)



def distance_walking(df):

    pngfile="images/distance-walking.png"

    ##
    ## 集計したDataFrameを作る
    ##
    
    begin_month = "201405"
    savecsvfile="db/distance-walking_" + begin_month + "-" + this_month + ".csv"

    date = pd.to_datetime(df.startDate).values
    value = df.value.values
    value = value.astype(None)  # なぜかtypeがobjectになってるので。

    # 時系列を最長に合わせる
    date = np.insert(date, -1, pd.to_datetime(begin_date))
    value = np.insert(value, -1, np.nan)

    df2 = pd.DataFrame(index=date, data={"DistanceWalkingRunning":value})

    # 毎日の和 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").sum()

    # データのないところ(0.0000)をNanに
    df2[df2["DistanceWalkingRunning"] == 0] = np.nan

    # csvファイル書き出し（データバックアップのため）
    # df2.to_csv(savecsvfile)

    ##
    ## グラフ
    ##
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 3), dpi=144)

    # 箱髭図
    df2["month"] = pd.to_datetime(df2.index).strftime('%Y-%m')
    df2.boxplot(column="DistanceWalkingRunning", by='month', rot=80, ax=ax, whis=10.0, color='#1f77b4') 
    
    ax.set_title("")
    ax.set_xlabel("")
    ax.grid(which="major", axis="x", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    ax.grid(which="major", axis="y", color="gray", alpha=0.3, linestyle=":", linewidth=1)
    plt.suptitle("歩行距離（月ごとの箱髭図）")
    ax.set_ylabel("km")

    plt.subplots_adjust(left=0.04, right=0.98, bottom=0.27, top=0.92)
    plt.locator_params(axis='x', nbins=16) #x軸，x個以内．

    if not(os.path.isfile(pngfile)):
        plt.savefig(pngfile)

    plt.pause(5)
    

def main():

    df = pd.read_csv(csvfile)
    
    index_sbp = df.type == "BloodPressureSystolic"
    index_dbp = df.type == "BloodPressureDiastolic"
    blood_pressure(df[index_sbp], df[index_dbp])
    
    index = df.type == "DistanceWalkingRunning"
    distance_walking(df[index])

    index = df.type == "BodyMass"
    body_mass(df[index])
    
    index = df.type == "BodyTemperature"
    body_temperature(df[index])

    ##
    ## join image
    ##

    pngfile = "images/helthcare.png"
    
    image_proc = np.array([], dtype=np.uint8)

    for filename in ["images/blood-pressure.png", "images/body-mass.png", "images/body-temperature.png", "images/distance-walking.png"]:

        if not(os.path.isfile(filename)):
            continue

        if (len(image_proc) == 0):
            image_proc = cv.imread(filename)
            continue
        
        image = cv.imread(filename)
        image_proc = cv.vconcat([image_proc, image])

    if not(os.path.isfile(pngfile)):
        cv.imwrite(pngfile, image_proc)
        print("create " + pngfile)

    cv.imshow("healthcare", image_proc)
    cv.waitKey(10000)
        
    
if __name__ == '__main__':
    main()

# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
