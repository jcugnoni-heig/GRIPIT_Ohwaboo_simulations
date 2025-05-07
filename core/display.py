# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import pandas as pd
import matplotlib.pyplot as plt

import scenarios.datas as dt
import core.simulation as sim
import core.sauvegarde as save
import numpy as np

###Colors
orange =     '#ffc107'
ligthGreen = "#cddc39"
green =      "#009688"
blue =       '#2196f3'
violet =     '#9c27b0'
red =        '#f44336'
black =      '#000000'

#Standard DPI = 100
DPI = 100
maxW = 19.20
maxH = 10.80


#_____________________________________________________________________________________________________________________________________________________________________
def read_file(fileName, fields = sim.fieldNames):
    if dt.runSimu == False:
        save.img_dir()
    try:
        df = pd.read_csv(fileName, delimiter=';', usecols = fields)
        return df
    except:
        print("Failed to find folder. Terminate program...")
        exit()


#_____________________________________________________________________________________________________________________________________________________________________
def calc_vit(df):
    lstvLrAvGy = [0]
    lstvLrArGy = [0]
    lstvLrArDy = [0]
    lstvLrAvDy = [0]
    lstvLrAvGz = [0]
    lstvLrArGz = [0]
    lstvLrArDz = [0]
    lstvLrAvDz = [0]
    for i in range(len(df['t'])):
        if i == 0:
            vLrAvGy = 0
            vLrArGy = 0
            vLrArDy = 0
            vLrAvDy = 0

            vLrAvGz = 0
            vLrArGz = 0
            vLrArDz = 0
            vLrAvDz = 0
        else:
            Dt = (df['t'][i] - df['t'][i-1]) / np.single(60)    #[min]
            vLrAvGy = (df['lrAvGy'][i] - df['lrAvGy'][i-1]) *1000 / Dt #[mm/min]
            vLrArGy = (df['lrArGy'][i] - df['lrArGy'][i-1]) *1000 / Dt #[mm/min]
            vLrArDy = (df['lrArDy'][i] - df['lrArDy'][i-1]) *1000 / Dt #[mm/min]
            vLrAvDy = (df['lrAvDy'][i] - df['lrAvDy'][i-1]) *1000 / Dt #[mm/min]

            vLrAvGz = (df['lrAvGz'][i] - df['lrAvGz'][i-1]) *1000 / Dt #[mm/min]
            vLrArGz = (df['lrArGz'][i] - df['lrArGz'][i-1]) *1000 / Dt #[mm/min]
            vLrArDz = (df['lrArDz'][i] - df['lrArDz'][i-1]) *1000 / Dt #[mm/min]
            vLrAvDz = (df['lrAvDz'][i] - df['lrAvDz'][i-1]) *1000 / Dt #[mm/min]

            lstvLrAvGy.append(vLrAvGy)
            lstvLrArGy.append(vLrArGy)
            lstvLrArDy.append(vLrArDy)
            lstvLrAvDy.append(vLrAvDy)
            lstvLrAvGz.append(vLrAvGz)
            lstvLrArGz.append(vLrArGz)
            lstvLrArDz.append(vLrArDz)
            lstvLrAvDz.append(vLrAvDz)

    df['vLr_AvG_y'] = pd.Series(lstvLrAvGy)
    df['vLr_ArG_y'] = pd.Series(lstvLrArGy)
    df['vLr_ArD_y'] = pd.Series(lstvLrArDy)
    df['vLr_AvD_y'] = pd.Series(lstvLrAvDy)
    df['vLr_AvG_z'] = pd.Series(lstvLrAvGz)
    df['vLr_ArG_z'] = pd.Series(lstvLrArGz)
    df['vLr_ArD_z'] = pd.Series(lstvLrArDz)
    df['vLr_AvD_z'] = pd.Series(lstvLrAvDz)
    print(df)
    return df


#_____________________________________________________________________________________________________________________________________________________________________
def all_graphs(df):
    df = calc_vit(df)
    integration_results_in_time(df)
    integration_results_for_distance(df)
    forces_module(df)
    entrefers_Y_temps(df)
    entrefers_Z_temps(df)
    entrefers_Y_distance(df)
    entrefers_Z_distance(df)
    lRes_Y(df)
    lRes_Z(df)
    vLRes_Y(df)
    vLRes_Z(df)
    #positions_2d_distance(df)
    positions_2d_temps(df)
    integration_Y_modules_temps(df)
    integration_Z_modules_temps(df)
    NFdlRes_Y(df)
    NFdlRes_Z(df)
    dlRes_Y(df)
    dlRes_Z(df)
    NFVRes_Y(df)
    NFVRes_Z(df)
    FRes_Y(df)
    FRes_Z(df)
    #plt.show()


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Résutats généraux
def integration_results_in_time(df):
    safeStop = dt.posXCgStop * np.ones(len(df["t"]))
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2, ax3, ax4, ax5, ax16), (ax6, ax7, ax8, ax9, ax10, ax17), (ax11, ax12, ax13, ax14, ax15, ax18)) = plt.subplots(3,6, num='Résultats integration [s]', sharex=True, figsize=(maxW, maxH))
    #plt.title("Simu_rail_L__kZ %.0f_k %.0f__ksiZ %.3f_ksiY %.3f"%(DATA.kz, DATA.ky, DATA.ksiZ, DATA.ksiY))
    ax1.plot(df["t"], safeStop, "r-")
    df.plot(x='t', y='xCg',      kind='line', ax=ax1,  grid = True, color= blue,    xlabel="[s]", ylabel="m", ylim=[0,dt.pisteLongueur])
    df.plot(x='t', y='yCg',      kind='line', ax=ax2,  grid = True, color= orange,  xlabel="[s]", ylabel="m")
    df.plot(x='t', y='zCg',      kind='line', ax=ax3,  grid = True, color= green,   xlabel="[s]", ylabel="m", ylim=[0,0.2])
    df.plot(x='t', y='tangage',  kind='line', ax=ax4,  grid = True, color= red,     xlabel="[s]", ylabel="°")
    df.plot(x='t', y='lacet',    kind='line', ax=ax5,  grid = True, color= ligthGreen,   xlabel="[s]", ylabel="°")
    df.plot(x='t', y='vXCg',     kind='line', ax=ax6,  grid = True, color= blue,    xlabel="[s]", ylabel="m/s")
    df.plot(x='t', y='vYCg',     kind='line', ax=ax7,  grid = True, color= orange,  xlabel="[s]", ylabel="m/s")
    df.plot(x='t', y='vZCg',     kind='line', ax=ax8,  grid = True, color= green,   xlabel="[s]", ylabel="m/s")
    df.plot(x='t', y='vTangage', kind='line', ax=ax9,  grid = True, color= red,     xlabel="[s]", ylabel="rad/s")
    df.plot(x='t', y='vLacet',   kind='line', ax=ax10, grid = True, color= ligthGreen,   xlabel="[s]", ylabel="rad/s")
    df.plot(x='t', y='aXCg',     kind='line', ax=ax11, grid = True, color= blue,    xlabel="[s]", ylabel="m/s2")
    df.plot(x='t', y='aYCg',     kind='line', ax=ax12, grid = True, color= orange,  xlabel="[s]", ylabel="m/s2")
    df.plot(x='t', y='aZCg',     kind='line', ax=ax13, grid = True, color= green,   xlabel="[s]", ylabel="m/s2")
    df.plot(x='t', y='aTangage', kind='line', ax=ax14, grid = True, color= red,     xlabel="[s]", ylabel="rad/s2")
    df.plot(x='t', y='aLacet',   kind='line', ax=ax15, grid = True, color= ligthGreen,   xlabel="[s]", ylabel="rad/s2")
    df.plot(x='t', y='roulis',   kind='line', ax=ax16, grid = True, color=violet ,     xlabel="[s]", ylabel="°")
    df.plot(x='t', y='vRoulis',  kind='line', ax=ax17, grid = True, color=violet ,   xlabel="[s]", ylabel="rad/s")
    df.plot(x='t', y='aRoulis',  kind='line', ax=ax18, grid = True, color=violet ,   xlabel="[s]", ylabel="rad/s2")
    plt.xlim(0, max(df["t"]))
    #plt.get_current_fig_manager().window.showMaximized()
    plt.savefig(dt.img0_path)
    return fig


#_____________________________________________________________________________________________________________________________________________________________________
def integration_results_for_distance(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2, ax3, ax4, ax5, ax16), (ax6, ax7, ax8, ax9, ax10, ax17), (ax11, ax12, ax13, ax14, ax15, ax18)) = plt.subplots(3,6, num='Résultats integration [m]', sharex=True, figsize=(maxW, maxH))
    #plt.title("Simu_rail_L__kZ %.0f_k %.0f__ksiZ %.3f_ksiY %.3f"%(DATA.kz, DATA.ky, DATA.ksiZ, DATA.ksiY))
    df.plot(x='xCg', y='t',        kind='line', ax=ax1,  grid = True, color= blue,    xlabel="[m]", ylabel="s")
    df.plot(x='xCg', y='yCg',      kind='line', ax=ax2,  grid = True, color= orange,  xlabel="[m]", ylabel="m")
    df.plot(x='xCg', y='zCg',      kind='line', ax=ax3,  grid = True, color= green,   xlabel="[m]", ylabel="m", ylim=[0,0.2])
    df.plot(x='xCg', y='tangage',  kind='line', ax=ax4,  grid = True, color= red,     xlabel="[m]", ylabel="°")
    df.plot(x='xCg', y='lacet',    kind='line', ax=ax5,  grid = True, color= ligthGreen,   xlabel="[m]", ylabel="°")
    df.plot(x='xCg', y='vXCg',     kind='line', ax=ax6,  grid = True, color= blue,    xlabel="[m]", ylabel="m/s")
    df.plot(x='xCg', y='vYCg',     kind='line', ax=ax7,  grid = True, color= orange,  xlabel="[m]", ylabel="m/s")
    df.plot(x='xCg', y='vZCg',     kind='line', ax=ax8,  grid = True, color= green,   xlabel="[m]", ylabel="m/s")
    df.plot(x='xCg', y='vTangage', kind='line', ax=ax9,  grid = True, color= red,     xlabel="[m]", ylabel="rad/s")
    df.plot(x='xCg', y='vLacet',   kind='line', ax=ax10, grid = True, color= ligthGreen,   xlabel="[m]", ylabel="rad/s")
    df.plot(x='xCg', y='aXCg',     kind='line', ax=ax11, grid = True, color= blue,    xlabel="[m]", ylabel="m/s2")
    df.plot(x='xCg', y='aYCg',     kind='line', ax=ax12, grid = True, color= orange,  xlabel="[m]", ylabel="m/s2")
    df.plot(x='xCg', y='aZCg',     kind='line', ax=ax13, grid = True, color= green,   xlabel="[m]", ylabel="m/s2")
    df.plot(x='xCg', y='aTangage', kind='line', ax=ax14, grid = True, color= red,     xlabel="[m]", ylabel="rad/s2")
    df.plot(x='xCg', y='aLacet',   kind='line', ax=ax15, grid = True, color= ligthGreen,   xlabel="[m]", ylabel="rad/s2")
    df.plot(x='xCg', y='roulis',   kind='line', ax=ax16, grid = True, color=violet ,     xlabel="[m]", ylabel="°")
    df.plot(x='xCg', y='vRoulis',  kind='line', ax=ax17, grid = True, color=violet ,   xlabel="[m]", ylabel="rad/s")
    df.plot(x='xCg', y='aRoulis',  kind='line', ax=ax18, grid = True, color=violet ,   xlabel="[m]", ylabel="rad/s2")
    #plt.get_current_fig_manager().window.showMaximized()
    plt.savefig(dt.img1_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Entrefers
def entrefers_Y_temps(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax2)) = plt.subplots(1,1, num='Entrefers Y selon le temps', sharex=True, sharey=True, figsize=(maxW, maxH*2/3)) #, figsize=(7.77, 3.24))
    df.plot(x='t', y='entreferAvGy', kind='line', ax=ax2, grid=True, color=green, xlabel="[s]", ylabel="[mm]")
    df.plot(x='t', y='entreferArGy', kind='line', ax=ax2, grid=True, color=red,   xlabel="[s]", ylabel="[mm]")
    df.plot(x='t', y='entreferArDy', kind='line', ax=ax2, grid=True, color=red,   xlabel="[s]", ylabel="[mm]", style='--')
    df.plot(x='t', y='entreferAvDy', kind='line', ax=ax2, grid=True, color=green, xlabel="[s]", ylabel="[mm]", style='--')
    ax2.legend(["Front left guide", "Rear left guide", "Rear right guide", "Front right guide"])
    #plt.ylim(0, 20)
    plt.xlim(0, max(df.t))
    plt.savefig(dt.img3_path)
    return fig


def entrefers_Z_temps(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax2)) = plt.subplots(1,1, num='Entrefers Z selon le temps', sharex=True, sharey=True, figsize=(maxW, maxH*2/3))
    df.plot(x='t', y='entreferAvGz', kind='line', ax=ax2, grid=True, color=blue,   xlabel="[s]", ylabel="[mm]")
    df.plot(x='t', y='entreferArGz', kind='line', ax=ax2, grid=True, color=orange, xlabel="[s]", ylabel="[mm]")
    df.plot(x='t', y='entreferArDz', kind='line', ax=ax2, grid=True, color=green,  xlabel="[s]", ylabel="[mm]", style='--')
    df.plot(x='t', y='entreferAvDz', kind='line', ax=ax2, grid=True, color=red,    xlabel="[s]", ylabel="[mm]", style='--')
    ax2.legend(["Front left lev", "Rear left lev", "Rear right lev", "Front right lev"])
    #plt.ylim(0, 20)
    plt.xlim(0, max(df.t))
    plt.savefig(dt.img2_path)
    return fig


def entrefers_Y_distance(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax2)) = plt.subplots(1,1, num='Entrefers Y selon la distance', sharex=True, sharey=True, figsize=(maxW, maxH*2/3)) #, figsize=(7.77, 3.24))
    df.plot(x="posLevAvGx", y='entreferAvGy', kind='line', ax=ax2, grid=True, color=green, xlabel="[m]", ylabel="[mm]")
    df.plot(x="posLevArGx", y='entreferArGy', kind='line', ax=ax2, grid=True, color=red,   xlabel="[m]", ylabel="[mm]")
    df.plot(x="posLevArDx", y='entreferArDy', kind='line', ax=ax2, grid=True, color=red,   xlabel="[m]", ylabel="[mm]", style='--')
    df.plot(x="posLevAvDx", y='entreferAvDy', kind='line', ax=ax2, grid=True, color=green, xlabel="[m]", ylabel="[mm]", style='--')
    ax2.legend(["Front left guide", "Rear left guide", "Rear right guide", "Front right guide"])
    #plt.ylim(0, 20)
    plt.xlim(0, max(df.posLevAvGx))
    plt.savefig(dt.img14_path)
    return fig


def entrefers_Z_distance(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax2)) = plt.subplots(1,1, num='Entrefers Z selon la distance', sharex=True, sharey=True, figsize=(maxW, maxH*2/3))
    df.plot(x="posLevAvGx", y='entreferAvGz', kind='line', ax=ax2, grid=True, color=blue,   xlabel="[m]", ylabel="[mm]")
    df.plot(x="posLevArGx", y='entreferArGz', kind='line', ax=ax2, grid=True, color=orange, xlabel="[m]", ylabel="[mm]")
    df.plot(x="posLevArDx", y='entreferArDz', kind='line', ax=ax2, grid=True, color=green,  xlabel="[m]", ylabel="[mm]", style='--')
    df.plot(x="posLevAvDx", y='entreferAvDz', kind='line', ax=ax2, grid=True, color=red,    xlabel="[m]", ylabel="[mm]", style='--')
    ax2.legend(["Front left lev", "Rear left lev", "Rear right lev", "Front right lev"])
    #plt.ylim(0, 20)
    plt.xlim(0, max(df.posLevAvGx))
    plt.savefig(dt.img13_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Ressorts
def lRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Longueur ressorts Y [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='lrAvGy', kind='line', ax=ax2, grid=True, color=blue,   xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrArGy', kind='line', ax=ax1, grid=True, color=orange, xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrArDy', kind='line', ax=ax3, grid=True, color=green,  xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrAvDy', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[m]")
    plt.savefig(dt.img10_path)
    return fig


def lRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Longueur ressorts Z [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='lrAvGz', kind='line', ax=ax2, grid=True, color=blue,   xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrArGz', kind='line', ax=ax1, grid=True, color=orange, xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrArDz', kind='line', ax=ax3, grid=True, color=green,  xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='lrAvDz', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[m]")
    plt.savefig(dt.img11_path)
    return fig


def vLRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Vitesse déformation ressorts Y [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='vLr_AvG_y', kind='line', ax=ax2, grid=True, color=blue,   xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_ArG_y', kind='line', ax=ax1, grid=True, color=orange, xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_ArD_y', kind='line', ax=ax3, grid=True, color=green,  xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_AvD_y', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[mm/min]")
    plt.savefig(dt.img15_path)
    return fig


def vLRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Vitesse déformation ressorts Z [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='vLr_AvG_z', kind='line', ax=ax2, grid=True, color=blue,        xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_ArG_z', kind='line', ax=ax1, grid=True, color=orange,      xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_ArD_z', kind='line', ax=ax3, grid=True, color=green,       xlabel="[s]", ylabel="[mm/min]")
    df.plot(x='t', y='vLr_AvD_z', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[mm/min]")
    plt.savefig(dt.img16_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Forces
def forces_module(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig1, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), (ax17, ax18, ax19, ax20), (ax13, ax14, ax15, ax16)) = plt.subplots(5,4, num='Forces Z modules [csv]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='t', y="fzAmortoAvG",  kind='line', ax=ax1, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzAmortoArG",  kind='line', ax=ax2, grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzAmortoArD",  kind='line', ax=ax3, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzAmortoAvD",  kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzContactAvG", kind='line', ax=ax5, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzContactArG", kind='line', ax=ax6, grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzContactArD", kind='line', ax=ax7, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzContactAvD", kind='line', ax=ax8, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzMagAvG",     kind='line', ax=ax9, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzMagArG",     kind='line', ax=ax10,grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzMagArD",     kind='line', ax=ax11,grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzMagAvD",     kind='line', ax=ax12,grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzFreinAvG",   kind='line', ax=ax17, grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzFreinArG",   kind='line', ax=ax18, grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzFreinArD",   kind='line', ax=ax19, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fzFreinAvD",   kind='line', ax=ax20, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="szModFAvG",    kind='line', ax=ax13,grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="szModFArG",    kind='line', ax=ax14,grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="szModFArD",    kind='line', ax=ax15,grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="szModFAvD",    kind='line', ax=ax16,grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    plt.xlim(0, max(df["t"]))
    plt.savefig(dt.img7_path)

    fig2, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), (ax17, ax18, ax19, ax20), (ax13, ax14, ax15, ax16)) = plt.subplots(5,4, num='Forces Y modules [csv]', sharex=True, figsize=(maxW, maxH)) #sharey=True,
    df.plot(x='t', y="fyAmortoAvG",  kind='line', ax=ax1, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyAmortoArG",  kind='line', ax=ax2, grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyAmortoArD",  kind='line', ax=ax3, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyAmortoAvD",  kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyContactAvG", kind='line', ax=ax5, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyContactArG", kind='line', ax=ax6, grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyContactArD", kind='line', ax=ax7, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyContactAvD", kind='line', ax=ax8, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyMagAvG",     kind='line', ax=ax9, grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyMagArG",     kind='line', ax=ax10,grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyMagArD",     kind='line', ax=ax11,grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyMagAvD",     kind='line', ax=ax12,grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyFreinAvG",   kind='line', ax=ax17, grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyFreinArG",   kind='line', ax=ax18, grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyFreinArD",   kind='line', ax=ax19, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fyFreinAvD",   kind='line', ax=ax20, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="syModFAvG",    kind='line', ax=ax13,grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="syModFArG",    kind='line', ax=ax14,grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="syModFArD",    kind='line', ax=ax15,grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="syModFAvD",    kind='line', ax=ax16,grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    plt.savefig(dt.img6_path)

    fig3, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12), (ax17, ax18, ax19, ax20), (ax13, ax14, ax15, ax16)) = plt.subplots(5,4, num='Forces X modules [csv]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='t', y="fxAmortoAvG",  kind='line', ax=ax1,  grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxAmortoArG",  kind='line', ax=ax2,  grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxAmortoArD",  kind='line', ax=ax3,  grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxAmortoAvD",  kind='line', ax=ax4,  grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxContactAvG", kind='line', ax=ax5,  grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxContactArG", kind='line', ax=ax6,  grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxContactArD", kind='line', ax=ax7,  grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxContactAvD", kind='line', ax=ax8,  grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxMagAvG",     kind='line', ax=ax9,  grid=True, color=blue,   xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxMagArG",     kind='line', ax=ax10, grid=True, color=orange, xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxMagArD",     kind='line', ax=ax11, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxMagAvD",     kind='line', ax=ax12, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxFreinAvG",   kind='line', ax=ax17, grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxFreinArG",   kind='line', ax=ax18, grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxFreinArD",   kind='line', ax=ax19, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="fxFreinAvD",   kind='line', ax=ax20, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="sxModFAvG",    kind='line', ax=ax13, grid=True, color=blue,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="sxModFArG",    kind='line', ax=ax14, grid=True, color=orange,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="sxModFArD",    kind='line', ax=ax15, grid=True, color=green,  xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y="sxModFAvD",    kind='line', ax=ax16, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    plt.savefig(dt.img5_path)
    return fig1, fig2, fig3
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Moments
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - 2D positions
def positions_2d_distance(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Positions 2D [m]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='posLevAvGx', y='posLevAvGy', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArGx', y='posLevArGy', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArDx', y='posLevArDy', kind='line', ax=ax1, grid=True, color=green,      xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevAvDx', y='posLevAvDy', kind='line', ax=ax2, grid=True, color=ligthGreen, xlabel="[m]", ylabel="[m]")

    df.plot(x='posLevAvGx', y='posLevAvGz', kind='line', ax=ax4, grid=True, color=blue,       xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArGx', y='posLevArGz', kind='line', ax=ax3, grid=True, color=orange,     xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArDx', y='posLevArDz', kind='line', ax=ax3, grid=True, color=green,      xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevAvDx', y='posLevAvDz', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[m]", ylabel="[m]")

    df.plot(x='posLevAvGx', y='railGLat', kind='line', ax=ax2, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArGx', y='railGLat', kind='line', ax=ax1, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArDx', y='railDLat', kind='line', ax=ax1, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevAvDx', y='railDLat', kind='line', ax=ax2, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevAvGx', y='railGLev', kind='line', ax=ax4, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArGx', y='railGLev', kind='line', ax=ax3, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevArDx', y='railGLev', kind='line', ax=ax3, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    df.plot(x='posLevAvDx', y='railGLev', kind='line', ax=ax4, grid=True, color=black, xlabel="[m]", ylabel="[m]")
    plt.savefig(str(dt.figuresPath + "Positions_2D_-_m" + ".png"))
    return fig


def positions_2d_temps(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Positions 2D [s]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='t', y='posLevAvGy',      kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevArGy',      kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevArDy',      kind='line', ax=ax1, grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevAvDy',      kind='line', ax=ax2, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posFixAvGy',      kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[m]", style="--")
    df.plot(x='t', y='posFixArGy',      kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[m]", style="--")
    df.plot(x='t', y='posFixArDy',      kind='line', ax=ax1, grid=True, color=green,      xlabel="[s]", ylabel="[m]", style="--")
    df.plot(x='t', y='posFixAvDy',      kind='line', ax=ax2, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]", style="--")
    df.plot(x='t', y='posForceYAvGy',   kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceYArGy',   kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceYArDy',   kind='line', ax=ax1, grid=True, color=green,      xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceYAvDy',   kind='line', ax=ax2, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='railGLat',        kind='line', ax=ax2, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGLat',        kind='line', ax=ax1, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railDLat',        kind='line', ax=ax1, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railDLat',        kind='line', ax=ax2, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    
    df.plot(x='t', y='posLevAvGz',      kind='line', ax=ax4, grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevArGz',      kind='line', ax=ax3, grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevArDz',      kind='line', ax=ax3, grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posLevAvDz',      kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posForceZAvGz',   kind='line', ax=ax4, grid=True, color=blue,       xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceZArGz',   kind='line', ax=ax3, grid=True, color=orange,     xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceZArDz',   kind='line', ax=ax3, grid=True, color=green,      xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='posForceZAvDz',   kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]", style="-.")
    df.plot(x='t', y='railGLev',        kind='line', ax=ax3, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGLev',        kind='line', ax=ax4, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGH',          kind='line', ax=ax3, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGH',          kind='line', ax=ax4, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGB',          kind='line', ax=ax3, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='railGB',          kind='line', ax=ax4, grid=True, color=black,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posAvGRoueAvHz',  kind='line', ax=ax3, grid=True, color=violet,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posArGRoueAvHz',  kind='line', ax=ax4, grid=True, color=violet,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='posAvGRoueAvBz',  kind='line', ax=ax3, grid=True, color=violet,      xlabel="[s]", ylabel="[m]", style="--")
    df.plot(x='t', y='posArGRoueAvBz',  kind='line', ax=ax4, grid=True, color=violet,      xlabel="[s]", ylabel="[m]", style="--")
    plt.xlim(0, max(df["t"]))
    plt.savefig(dt.img4_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Integration modules temps
def integration_Y_modules_temps(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12)) = plt.subplots(3,4, num='Integration modules Y [s]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='t', y='yModuleAvG', kind='line', ax=ax1,  grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='yModuleArG', kind='line', ax=ax2,  grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='yModuleArD', kind='line', ax=ax3,  grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='yModuleAvD', kind='line', ax=ax4,  grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")

    df.plot(x='t', y='vYmoduleAvG', kind='line', ax=ax5,  grid=True, color=blue,       xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vYmoduleArG', kind='line', ax=ax6,  grid=True, color=orange,     xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vYmoduleArD', kind='line', ax=ax7,  grid=True, color=green,      xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vYmoduleAvD', kind='line', ax=ax8,  grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m/s]")

    df.plot(x='t', y='aYmoduleAvG', kind='line', ax=ax9,  grid=True, color=blue,       xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aYmoduleArG', kind='line', ax=ax10, grid=True, color=orange,     xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aYmoduleArD', kind='line', ax=ax11, grid=True, color=green,      xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aYmoduleAvD', kind='line', ax=ax12, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m/s2]")
    plt.xlim(0, max(df["t"]))
    plt.savefig(dt.img8_path)
    return fig


def integration_Z_modules_temps(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8), (ax9, ax10, ax11, ax12)) = plt.subplots(3,4, num='Integration modules Z [s]', sharex=True, figsize=(maxW, maxH))
    df.plot(x='t', y='zModuleAvG', kind='line', ax=ax1,  grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='zModuleArG', kind='line', ax=ax2,  grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='zModuleArD', kind='line', ax=ax3,  grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='zModuleAvD', kind='line', ax=ax4,  grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")

    df.plot(x='t', y='vZmoduleAvG', kind='line', ax=ax5,  grid=True, color=blue,       xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vZmoduleArG', kind='line', ax=ax6,  grid=True, color=orange,     xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vZmoduleArD', kind='line', ax=ax7,  grid=True, color=green,      xlabel="[s]", ylabel="[m/s]")
    df.plot(x='t', y='vZmoduleAvD', kind='line', ax=ax8,  grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m/s]")

    df.plot(x='t', y='aZmoduleAvG', kind='line', ax=ax9,  grid=True, color=blue,       xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aZmoduleArG', kind='line', ax=ax10, grid=True, color=orange,     xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aZmoduleArD', kind='line', ax=ax11, grid=True, color=green,      xlabel="[s]", ylabel="[m/s2]")
    df.plot(x='t', y='aZmoduleAvD', kind='line', ax=ax12, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m/s2]")
    plt.xlim(0, max(df["t"]))
    plt.savefig(dt.img9_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Comportement amortisseurs
#F/dx
#dx/t
#N/v
def NFdlRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force fct. déformation ressorts Y [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='dlrAvGy', y='fyAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrArGy', y='fyAmortoArG', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrArDy', y='fyAmortoArD', kind='line', ax=ax3, grid=True, color=green,      xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrAvDy', y='fyAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[m]", ylabel="[N]")
    plt.savefig(dt.img17_path)
    return fig


def NFdlRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force fct. déformation ressorts Z [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='dlrAvGy', y='fzAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrArGy', y='fzAmortoArG', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrArDy', y='fzAmortoArD', kind='line', ax=ax3, grid=True, color=green,      xlabel="[m]", ylabel="[N]")
    df.plot(x='dlrAvDy', y='fzAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[m]", ylabel="[N]")
    plt.savefig(dt.img18_path)
    return fig


def dlRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Déformation ressorts Y [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='dlrAvGy', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrArGy', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrArDy', kind='line', ax=ax3, grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrAvDy', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")
    plt.savefig(dt.img19_path)
    return fig


def dlRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Déformation ressorts Z [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='dlrAvGz', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrArGz', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrArDz', kind='line', ax=ax3, grid=True, color=green,      xlabel="[s]", ylabel="[m]")
    df.plot(x='t', y='dlrAvDz', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[m]")
    plt.savefig(dt.img20_path)
    return fig


def NFVRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force fct. vitesse déformation ressorts Y [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='vLr_AvG_y', y='fyAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_ArG_y', y='fyAmortoArG', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_ArD_y', y='fyAmortoArD', kind='line', ax=ax3, grid=True, color=green,      xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_AvD_y', y='fyAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[mm/min]", ylabel="[N]")
    plt.savefig(dt.img21_path)
    return fig


def NFVRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force fct. vitesse déformation ressorts Z [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='vLr_AvG_z', y='fzAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,        xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_ArG_z', y='fzAmortoArG', kind='line', ax=ax1, grid=True, color=orange,      xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_ArD_z', y='fzAmortoArD', kind='line', ax=ax3, grid=True, color=green,       xlabel="[mm/min]", ylabel="[N]")
    df.plot(x='vLr_AvD_z', y='fzAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[mm/min]", ylabel="[N]")
    plt.savefig(dt.img22_path)
    return fig


def FRes_Y(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force ressorts Y fct. temps [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='fyAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,       xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fyAmortoArG', kind='line', ax=ax1, grid=True, color=orange,     xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fyAmortoArD', kind='line', ax=ax3, grid=True, color=green,      xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fyAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen, xlabel="[s]", ylabel="[N]")
    plt.savefig(dt.img23_path)
    return fig


def FRes_Z(df):
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, num='Force ressorts Z fct temps [csv]', sharex=True, sharey=True, figsize=(maxW, maxH))
    df.plot(x='t', y='fzAmortoAvG', kind='line', ax=ax2, grid=True, color=blue,        xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fzAmortoArG', kind='line', ax=ax1, grid=True, color=orange,      xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fzAmortoArD', kind='line', ax=ax3, grid=True, color=green,       xlabel="[s]", ylabel="[N]")
    df.plot(x='t', y='fzAmortoAvD', kind='line', ax=ax4, grid=True, color=ligthGreen,  xlabel="[s]", ylabel="[N]")
    plt.savefig(dt.img24_path)
    return fig
#!SECTION


#_____________________________________________________________________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________________________________________________________________
