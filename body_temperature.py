#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import japanize_matplotlib

from datetime import date
this_month = date.today().strftime("%Y%m")
begin_month = "202004"
begin_date = "2013-08-25"

pngfile="images/body-temperature.png"

def body_temperature():
    csvfile="/tmp/body-temperature.csv"
    savecsvfile="db/body-temperature_" + begin_month + "-" + this_month + ".csv"

    df = pd.read_csv(csvfile)

    date = pd.to_datetime(df.startDate).values
    value = df.value.values

    # 時系列を最長に合わせる
    length = len(date)
    date = np.insert(date, length, pd.to_datetime(begin_date))
    value = np.insert(value, length, np.nan)

    df2 = pd.DataFrame(index=date, data={"BodyTemperature":value})

    # 日ごと平均 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").mean()

    # csvファイル書き出し（データバックアップのため）
    df2.to_csv(savecsvfile)

    return df2


def main():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 3), dpi=144)

    df = body_temperature()

    # Nanを補完
    df = df.interpolate()

    df['month'] = pd.to_datetime(df.index).strftime('%Y-%m-%W')
    df.boxplot(column="BodyTemperature", by='month', rot=70, ax=ax, whis=10.0, color='#1f77b4') 

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
    # import pdb; pdb.set_trace()

    # plt.show()



if __name__ == '__main__':
    main()


### Local Variables: ###
### truncate-lines:t ###
### End: ###
