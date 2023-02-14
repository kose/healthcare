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

pngfile="images/body-mass.png"

def body_mass():
    csvfile="/tmp/body-mass.csv"
    savecsvfile="db/body-mass_" + begin_month + "-" + this_month + ".csv"

    df = pd.read_csv(csvfile)

    date = pd.to_datetime(df.startDate).values
    value = df.value.values

    df2 = pd.DataFrame(index=date, data={"mean weekly":value})

    # 日ごと平均 (日付順に並べ替えられる）
    df2 = df2.resample(rule="D").mean()

    # csvファイル書き出し（データバックアップのため）
    df2.to_csv(savecsvfile)

    return df2


def main():
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 2.5), dpi=144)

    df = body_mass()

    # Nanを補完
    df = df.interpolate()

    # 週平均
    df = df.resample(rule="W").mean()
    plt.suptitle("体重（週の平均）")

    # 月平均
    # df = df.resample(rule="M").mean()
    # plt.suptitle("体重（月平均）")

    df.plot(ax=ax)

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
    # import pdb; pdb.set_trace()

    # plt.show()


if __name__ == '__main__':
    main()

### Local Variables: ###
### truncate-lines:t ###
### End: ###
