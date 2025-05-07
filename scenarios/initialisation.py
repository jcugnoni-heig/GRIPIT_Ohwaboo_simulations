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
import core.forces as fo

rehausse = np.single(1E-6)

def conditions_initiales():
    dt.lastPercent = 0
    dt.flagFreinage = False
    xCg = dt.podLength/2
    yCg = np.single(0.00)
    zCg = np.single(0.095)# + dt.tRail + np.single(0.005)

    vXCg = np.single(0)
    vYCg = np.single(0)
    vZCg = np.single(0)

    tangage =  np.single(0) #np.deg2rad(1) #
    vTangage = np.single(0)

    lacet =  np.deg2rad(0) #np.single(0)   #np.deg2rad(1) #
    vLacet = np.single(0)

    roulis = np.single(0)
    vRoulis = np.single(0)

    yCgModAvG = np.single(0.324)  - rehausse#np.single(0.005)
    yCgModArG = np.single(0.324)  - rehausse#np.single(0.005)
    yCgModArD = np.single(-0.324) + rehausse#np.single(0.005)
    yCgModAvD = np.single(-0.324) + rehausse#np.single(0.005)

    vYCgModAvG = np.single(0)
    vYCgModArG = np.single(0)
    vYCgModArD = np.single(0)
    vYCgModAvD = np.single(0)

    zCgModAvG = np.single(0.095) + rehausse #np.single(0.001)# + dt.tRail + np.single(0.005)
    zCgModArG = np.single(0.095) + rehausse #np.single(0.001)# + dt.tRail + np.single(0.005)
    zCgModArD = np.single(0.095) + rehausse #np.single(0.001)# + dt.tRail + np.single(0.005)
    zCgModAvD = np.single(0.095) + rehausse #np.single(0.001)# + dt.tRail + np.single(0.005)

    vZCgModAvG = np.single(0)
    vZCgModArG = np.single(0)
    vZCgModArD = np.single(0)
    vZCgModAvD = np.single(0)

    return np.array([xCg, yCg, zCg, 
                     lacet, tangage, roulis, 
                     vXCg, vYCg, vZCg, 
                     vLacet, vTangage, vRoulis, 
                     yCgModAvG, zCgModAvG, 
                     yCgModArG, zCgModArG, 
                     yCgModArD, zCgModArD, 
                     yCgModAvD, zCgModAvD, 
                     vYCgModAvG, vZCgModAvG, 
                     vYCgModArG, vZCgModArG, 
                     vYCgModArD, vZCgModArD, 
                     vYCgModAvD, vZCgModAvD])

def test(stateVectorY, t, deltaT):
    xCg = stateVectorY[0]
    yCg = stateVectorY[1]
    zCg = stateVectorY[2]
    lacet = stateVectorY[3]
    tangage = stateVectorY[4]
    roulis = stateVectorY[5]
    vXCg = stateVectorY[6]
    vYCg = stateVectorY[7]
    vZCg = stateVectorY[8]
    vLacet = stateVectorY[9]
    vTangage = stateVectorY[10]
    vRoulis = stateVectorY[11]
    yCgModAvG = stateVectorY[12]
    zCgModAvG = stateVectorY[13]
    yCgModArG = stateVectorY[14]
    zCgModArG = stateVectorY[15]
    yCgModArD = stateVectorY[16]
    zCgModArD = stateVectorY[17]
    yCgModAvD = stateVectorY[18]
    zCgModAvD = stateVectorY[19]
    
    vYCgModAvG = stateVectorY[20]
    vZCgModAvG = stateVectorY[21]
    vYCgModArG = stateVectorY[22]
    vZCgModArG = stateVectorY[23]
    vYCgModArD = stateVectorY[24]
    vZCgModArD = stateVectorY[25]
    vYCgModAvD = stateVectorY[26]
    vZCgModAvD = stateVectorY[27]

    posCg = np.array([xCg, yCg, zCg])
    angles = np.array([lacet, tangage, roulis])
    posCgModAvG = np.array([0, yCgModAvG, zCgModAvG])
    posCgModArG = np.array([0, yCgModArG, zCgModArG])
    posCgModArD = np.array([0, yCgModArD, zCgModArD])
    posCgModAvD = np.array([0, yCgModAvD, zCgModAvD])
    
    posCgN1 = np.array([xCg+vXCg*deltaT, yCg+vYCg*deltaT, zCg+vZCg*deltaT])
    anglesN1 = np.array([lacet+vLacet*deltaT, tangage+vTangage*deltaT, roulis+vRoulis*deltaT])
    posCgModAvGn1 = np.array([0, yCgModAvG+vYCgModAvG*deltaT, zCgModAvG+vZCgModAvG*deltaT])
    posCgModArGn1 = np.array([0, yCgModArG+vYCgModArG*deltaT, zCgModArG+vZCgModArG*deltaT])
    posCgModArDn1 = np.array([0, yCgModArD+vYCgModArD*deltaT, zCgModArD+vZCgModArD*deltaT])
    posCgModAvDn1 = np.array([0, yCgModAvD+vYCgModAvD*deltaT, zCgModAvD+vZCgModAvD*deltaT])

    geomFromCgPod, geomWorldPod, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD = geom.general_geometry(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD)
    geomFromCgPodN1, geomWorldPodN1, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1 = geom.general_geometry(posCgN1, anglesN1, posCgModAvGn1, posCgModArGn1, posCgModArDn1, posCgModAvDn1)
    vLrAvG, vLrArG, vLrArD, vLrAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD = geom.vitesse_variation_distances(deltaT, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1)
    
    print()
    print("AvG entrefer Y: %.3f \tZ: %.3f \tL ressorts Y: %.3f \tZ: %.3f \tRoue vH: %.3f vB: %.3f vLat: %.3f  \tRoue rH: %.3f rB: %.3f rLat: %.3f"%(distToAvG[dt.idForceLevY], distToAvG[dt.idForceLevZ], lrAvG[dt.idy], lrAvG[dt.idz], distToAvG[dt.idForceRoueAvH], distToAvG[dt.idForceRoueAvB], distToAvG[dt.idForceRoueAvL], distToAvG[dt.idForceRoueArH], distToAvG[dt.idForceRoueArB], distToAvG[dt.idForceRoueArL]))
    print("ArG entrefer Y: %.3f \tZ: %.3f \tL ressorts Y: %.3f \tZ: %.3f \tRoue vH: %.3f vB: %.3f vLat: %.3f  \tRoue rH: %.3f rB: %.3f rLat: %.3f"%(distToArG[dt.idForceLevY], distToArG[dt.idForceLevZ], lrArG[dt.idy], lrArG[dt.idz], distToArG[dt.idForceRoueAvH], distToArG[dt.idForceRoueAvB], distToArG[dt.idForceRoueAvL], distToArG[dt.idForceRoueArH], distToArG[dt.idForceRoueArB], distToArG[dt.idForceRoueArL]))
    print("ArD entrefer Y: %.3f \tZ: %.3f \tL ressorts Y: %.3f \tZ: %.3f \tRoue vH: %.3f vB: %.3f vLat: %.3f  \tRoue rH: %.3f rB: %.3f rLat: %.3f"%(distToArD[dt.idForceLevY], distToArD[dt.idForceLevZ], lrArD[dt.idy], lrArD[dt.idz], distToArD[dt.idForceRoueAvH], distToArD[dt.idForceRoueAvB], distToArD[dt.idForceRoueAvL], distToArD[dt.idForceRoueArH], distToArD[dt.idForceRoueArB], distToArD[dt.idForceRoueArL]))
    print("AvD entrefer Y: %.3f \tZ: %.3f \tL ressorts Y: %.3f \tZ: %.3f \tRoue vH: %.3f vB: %.3f vLat: %.3f  \tRoue rH: %.3f rB: %.3f rLat: %.3f"%(distToAvD[dt.idForceLevY], distToAvD[dt.idForceLevZ], lrAvD[dt.idy], lrAvD[dt.idz], distToAvD[dt.idForceRoueAvH], distToAvD[dt.idForceRoueAvB], distToAvD[dt.idForceRoueAvL], distToAvD[dt.idForceRoueArH], distToAvD[dt.idForceRoueArB], distToAvD[dt.idForceRoueArL]))

    fAero, fProp, fGraviteOnMod, fGravs, fMags, fConts, fWheels, fBrakes, fAmorts, fReacts = fo.all_forces(t, xCg, vXCg, distToAvG, distToArG, distToArD, distToAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD, lrAvG, lrArG, lrArD, lrAvD, vLrAvG, vLrArG, vLrArD, vLrAvD)
    sCgF, sModFAvG, sModFArG, sModFArD, sModFAvD = fo.somme_forces(fProp, fGraviteOnMod, fGravs, fAmorts, fAero, fBrakes, fConts, fMags, fReacts)
    print()
    print("___________Forces sur le chassis")
    print()
    print("fAero", fAero)
    print()
    print("fProp", fProp)
    print()
    print("fGraviteOnMod", fGraviteOnMod)
    print()
    for i in fReacts:
        print("fReacts", i)
    print()
    print("fSum on chassis", sCgF)
    print()
    print("___________Forces sur les modules")
    print()

    for i in fGravs:
        print("fGravs", i)
    print()
    for i in fMags:
        print("fMags", i)
    print()
    for i in fConts:
        print("fConts", i)
    print()
    for i in fWheels:
        print("fWheels", i)
    print()
    for i in fBrakes:
        print("fBrakes", i)
    print()
    for i in fAmorts:
        print("fAmorts", i)
    print()
    print("sModFAvG", sModFAvG)
    print("sModFArG", sModFArG)
    print("sModFArD", sModFArD)
    print("sModFAvD", sModFAvD)
    
    print()
    print("masseTotale %.3f, masseOnMod %.3f, masseOnLev %.3f"%(dt.masseTotale, dt.masseOnMod, dt.masseOnLev))

#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    Y = conditions_initiales()
    test(Y, 0, 0.1)