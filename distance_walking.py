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
begin_month = "201405"
begin_date = "2013-08-25"

pngfile="images/distance-walking.png"

def distance_walking():
    
    csvfile="/tmp/distance-walking.csv"
    savecsvfile="db/distance-walking_" + begin_month + "-" + this_month + ".csv"

    df = pd.read_csv(csvfile)

    date = pd.to_datetime(df.startDate).values
    value = df.value.values

    # 時系列を最長に合わせる
    date = np.insert(date, -1, pd.to_datetime(begin_date))
    value = np.insert(value, -1, np.nan)

    df2 = pd.DataFrame(index=date, data={"Distance by day":value})

    # 毎日の和 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").sum()

    # データのないところ(0.0000)をNanに
    df2[df2["Distance by day"] == 0] = np.nan

    # csvファイル書き出し（データバックアップのため）
    df2.to_csv(savecsvfile)

    return df2


def main():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 3), dpi=144)

    df = distance_walking()

    # 箱髭図
    df["month"] = pd.to_datetime(df.index).strftime('%Y-%m')
    df.boxplot(column="Distance by day", by='month', rot=80, ax=ax, whis=10.0, color='#1f77b4') 
    
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
    # import pdb; pdb.set_trace()

    # plt.show()


if __name__ == '__main__':
    main()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
