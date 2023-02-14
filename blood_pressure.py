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
begin_month = "201308"

pngfile="images/blood-pressure.png"

def blood_pressure():

    csvfile_sbp="/tmp/blood-pressure-sbp.csv"
    csvfile_dbp="/tmp/blood-pressure-dbp.csv"
    savecsvfile="db/blood-pressure_" + begin_month + "-" + this_month + ".csv"

    def make_df(csvfile, name):

        df = pd.read_csv(csvfile)

        date = pd.to_datetime(df.startDate).values
        value = df.value.values

        df2 = pd.DataFrame(index=date, data={name:value})

        # 日ごと平均 (日付順に並べ替えられる）
        # df2 = df2.resample(rule="D").mean()

        # 日ごとmax() (日付順に並べ替えられる）
        df2 = df2.resample(rule="D").max()

        return df2

    df = make_df(csvfile_sbp, "SBP")
    df_dbp = make_df(csvfile_dbp, "DBP")

    # 列で結合
    df["DBP"] = df_dbp.DBP.values

    # csvファイル書き出し（データバックアップのため）
    df.to_csv(savecsvfile)

    return df

def main():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 4), dpi=144)

    df = blood_pressure()

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

    # plt.show()


if __name__ == '__main__':
    main()

# import pdb; pdb.set_trace()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
