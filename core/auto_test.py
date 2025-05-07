# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import numpy as np
import scenarios.datas as dt
import core.geometry as geom
from matplotlib import pyplot as plt
maxW = 19.20
maxH = 10.80

def debug(t, geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD):
    fig, ((ay1, az1), (ay2, az2), (ay3, az3), (ay4, az4), (ay5, az5), (ay6, az6), (ay7, az7), (ay8, az8), (ay9, az9))  = plt.subplots(9,2, num='Suivi des positions', sharex=True, figsize=(maxW, maxH))
    fig.suptitle('Suivi des positions')
    add_point_to_graph(geomWorldPod[dt.idChassis][dt.idx], geomWorldPod[dt.idChassis][dt.idy], "yCg", ay1)
    add_point_to_graph(geomWorldPod[dt.idChassis][dt.idx], geomWorldPod[dt.idChassis][dt.idz], "zCg", az1)

    add_point_to_graph(geomWorldPod[dt.idFixAvG][dt.idx], geomWorldPod[dt.idFixAvG][dt.idy], "y fixe AvG", ay2)
    add_point_to_graph(geomWorldPod[dt.idFixAvG][dt.idx], geomWorldPod[dt.idFixAvG][dt.idz], "z fixe AvG", az2)
    add_point_to_graph(geomWorldPod[dt.idFixArG][dt.idx], geomWorldPod[dt.idFixArG][dt.idy], "y fixe ArG", ay3)
    add_point_to_graph(geomWorldPod[dt.idFixArG][dt.idx], geomWorldPod[dt.idFixArG][dt.idz], "z fixe ArG", az3)
    add_point_to_graph(geomWorldPod[dt.idFixArD][dt.idx], geomWorldPod[dt.idFixArD][dt.idy], "y fixe ArD", ay4)
    add_point_to_graph(geomWorldPod[dt.idFixArD][dt.idx], geomWorldPod[dt.idFixArD][dt.idz], "z fixe ArD", az4)
    add_point_to_graph(geomWorldPod[dt.idFixAvD][dt.idx], geomWorldPod[dt.idFixAvD][dt.idy], "y fixe AvD", ay5)
    add_point_to_graph(geomWorldPod[dt.idFixAvD][dt.idx], geomWorldPod[dt.idFixAvD][dt.idz], "z fixe AvD", az5)

    add_point_to_graph(geomWorldAvG[dt.idFixDumper][dt.idx], geomWorldAvG[dt.idFixDumper][dt.idy], "y mobile AvG", ay6)
    add_point_to_graph(geomWorldAvG[dt.idFixDumper][dt.idx], geomWorldAvG[dt.idFixDumper][dt.idz], "z mobile AvG", az6)
    add_point_to_graph(geomWorldArG[dt.idFixDumper][dt.idx], geomWorldArG[dt.idFixDumper][dt.idy], "y mobile ArG", ay7)
    add_point_to_graph(geomWorldArG[dt.idFixDumper][dt.idx], geomWorldArG[dt.idFixDumper][dt.idz], "z mobile ArG", az7)
    add_point_to_graph(geomWorldArD[dt.idFixDumper][dt.idx], geomWorldArD[dt.idFixDumper][dt.idy], "y mobile ArD", ay8)
    add_point_to_graph(geomWorldArD[dt.idFixDumper][dt.idx], geomWorldArD[dt.idFixDumper][dt.idz], "z mobile ArD", az8)
    add_point_to_graph(geomWorldAvD[dt.idFixDumper][dt.idx], geomWorldAvD[dt.idFixDumper][dt.idy], "y mobile AvD", ay9)
    add_point_to_graph(geomWorldAvD[dt.idFixDumper][dt.idx], geomWorldAvD[dt.idFixDumper][dt.idz], "z mobile AvD", az9)

    plt.draw()
    plt.pause(0.001)
    if t == dt.manualTravelDuration:
        input("Press [enter] to continue.")

def add_point_to_graph(x, y, title, axs):
    axs.plot(x, y)
    axs.set_title(title)
    axs.set_xlabel('s')
    axs.set_ylabel('m')
    axs.grid(True)

def auto_test():
    dt = np.single(0)

    xCg = np.single(0)
    yCg = np.single(0)
    zCg = np.single(0.095)

    lacet = np.single(0)
    tangage = np.single(0)
    roulis = np.single(0)

    vXCg = np.single(0)
    vYCg = np.single(0)
    vZCg = np.single(0)

    vLacet = np.single(0)
    vTangage = np.single(0)
    vRoulis = np.single(0)

    yCgModAvG = np.single(0.324)
    yCgModArG = np.single(0.324)
    yCgModArD = np.single(-0.324)
    yCgModAvD = np.single(-0.324)
    
    zCgModAvG = np.single(0.095)
    zCgModArG = np.single(0.095)
    zCgModArD = np.single(0.095)
    zCgModAvD = np.single(0.095)


    vYCgModAvG = np.single(0)
    vYCgModArG = np.single(0)
    vYCgModArD = np.single(0)
    vYCgModAvD = np.single(0)
    
    vZCgModAvG = np.single(0)
    vZCgModArG = np.single(0)
    vZCgModArD = np.single(0)
    vZCgModAvD = np.single(0)

    posCg = np.array([0, 0, 0.095])
    angles = np.array([0,0,0])
    posCgModAvG = np.array([ 0.407,  0.324, 0.098])
    posCgModArG = np.array([-0.407,  0.324, 0.098])
    posCgModArD = np.array([-0.407, -0.324, 0.098])
    posCgModAvD = np.array([ 0.407, -0.324, 0.098])
    posCgN1 = np.array([xCg+vXCg*dt, yCg+vYCg*dt, zCg+vZCg*dt])
    anglesN1 = np.array([lacet+vLacet*dt, tangage+vTangage*dt, roulis+vRoulis*dt])
    posCgModAvGn1 = np.array([0, yCgModAvG+vYCgModAvG*dt, zCgModAvG+vZCgModAvG*dt])
    posCgModArGn1 = np.array([0, yCgModArG+vYCgModArG*dt, zCgModArG+vZCgModArG*dt])
    posCgModArDn1 = np.array([0, yCgModArD+vYCgModArD*dt, zCgModArD+vZCgModArD*dt])
    posCgModAvDn1 = np.array([0, yCgModAvD+vYCgModAvD*dt, zCgModAvD+vZCgModAvD*dt])

    geomFromCgPod, geomWorldPod, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD = geom.general_geometry(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD)
    geomFromCgPodN1, geomWorldPodN1, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1 = geom.general_geometry(posCgN1, anglesN1, posCgModAvGn1, posCgModArGn1, posCgModArDn1, posCgModAvDn1)
    vLrAvG, vLrArG, vLrArD, vLrAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD = geom.vitesse_variation_distances(dt, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1)