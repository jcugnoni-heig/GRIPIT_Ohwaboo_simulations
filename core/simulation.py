import core.geometry as geom
import core.forces as fo
import scenarios.datas as data
import scenarios.initialisation as init
import core.sauvegarde as save
import core.geometry as geom
import core.auto_test as auto_test

import numpy as np
from scipy import interpolate, integrate
import time

#_____________________________________________________________________________________________________________________________________________________________________
###Monitoring
lastPercent = 0
monitorDec = 1
start_time = 0

###Fields
fieldNames = [
    "t", 
    "xCg", "vXCg", "aXCg", "yCg", "vYCg", "aYCg", "zCg", "vZCg", "aZCg", "tangage", "vTangage", "aTangage", "lacet", "vLacet", "aLacet", "roulis", "vRoulis", "aRoulis",
    "yModuleAvG", "yModuleArG", "yModuleArD", "yModuleAvD", "vYmoduleAvG", "vYmoduleArG", "vYmoduleArD", "vYmoduleAvD", "aYmoduleAvG", "aYmoduleArG", "aYmoduleArD", "aYmoduleAvD", 
    "zModuleAvG", "zModuleArG", "zModuleArD", "zModuleAvD", "vZmoduleAvG", "vZmoduleArG", "vZmoduleArD", "vZmoduleAvD", "aZmoduleAvG", "aZmoduleArG", "aZmoduleArD", "aZmoduleAvD",
    "fxMagAvG",     "fyMagAvG",      "fzMagAvG",
    "fxMagArG",     "fyMagArG",      "fzMagArG",
    "fxMagArD",     "fyMagArD",      "fzMagArD",
    "fxMagAvD",     "fyMagAvD",      "fzMagAvD",
    "fxContactAvG", "fyContactAvG",  "fzContactAvG",
    "fxContactArG", "fyContactArG",  "fzContactArG",
    "fxContactArD", "fyContactArD",  "fzContactArD",
    "fxContactAvD", "fyContactAvD",  "fzContactAvD",
    "fxFreinAvG",   "fyFreinAvG",    "fzFreinAvG",
    "fxFreinArG",   "fyFreinArG",    "fzFreinArG",
    "fxFreinArD",   "fyFreinArD",    "fzFreinArD",
    "fxFreinAvD",   "fyFreinAvD",    "fzFreinAvD",
    "fxAmortoAvG",  "fyAmortoAvG",   "fzAmortoAvG",
    "fxAmortoArG",  "fyAmortoArG",   "fzAmortoArG",
    "fxAmortoArD",  "fyAmortoArD",   "fzAmortoArD",
    "fxAmortoAvD",  "fyAmortoAvD",   "fzAmortoAvD",
    "sxModFAvG",    "syModFAvG",     "szModFAvG",
    "sxModFArG",    "syModFArG",     "szModFArG",
    "sxModFArD",    "syModFArD",     "szModFArD",
    "sxModFAvD",    "syModFAvD",     "szModFAvD",
    "entreferAvGy", "entreferAvGz",
    "entreferArGy", "entreferArGz",
    "entreferArDy", "entreferArDz",
    "entreferAvDy", "entreferAvDz",

    "lrAvGy", "lrAvGz",
    "lrArGy", "lrArGz",
    "lrArDy", "lrArDz",
    "lrAvDy", "lrAvDz",
    "dlrAvGy", "dlrAvGz",
    "dlrArGy", "dlrArGz",
    "dlrArDy", "dlrArDz",
    "dlrAvDy", "dlrAvDz",
    "vLrAvGy", "vLrAvGz",
    "vLrArGy", "vLrArGz",
    "vLrArDy", "vLrArDz",
    "vLrAvDy", "vLrAvDz",

    "posLevAvGx", "posLevAvGy", "posLevAvGz",
    "posLevArGx", "posLevArGy", "posLevArGz",
    "posLevArDx", "posLevArDy", "posLevArDz",
    "posLevAvDx", "posLevAvDy", "posLevAvDz",
    "posFixAvGx", "posFixAvGy", "posFixAvGz",
    "posFixArGx", "posFixArGy", "posFixArGz",
    "posFixArDx", "posFixArDy", "posFixArDz",
    "posFixAvDx", "posFixAvDy", "posFixAvDz",
    "posForceYAvGx", "posForceYAvGy", "posForceYAvGz",
    "posForceYArGx", "posForceYArGy", "posForceYArGz",
    "posForceYArDx", "posForceYArDy", "posForceYArDz",
    "posForceYAvDx", "posForceYAvDy", "posForceYAvDz",
    "posForceZAvGx", "posForceZAvGy", "posForceZAvGz",
    "posForceZArGx", "posForceZArGy", "posForceZArGz",
    "posForceZArDx", "posForceZArDy", "posForceZArDz",
    "posForceZAvDx", "posForceZAvDy", "posForceZAvDz",
    "posAvGRoueAvHx", "posAvGRoueAvHy", "posAvGRoueAvHz",
    "posArGRoueAvHx", "posArGRoueAvHy", "posArGRoueAvHz",
    "posArDRoueAvHx", "posArDRoueAvHy", "posArDRoueAvHz",
    "posAvDRoueAvHx", "posAvDRoueAvHy", "posAvDRoueAvHz",

    "posAvGRoueAvBx", "posAvGRoueAvBy", "posAvGRoueAvBz",
    "posArGRoueAvBx", "posArGRoueAvBy", "posArGRoueAvBz",
    "posArDRoueAvBx", "posArDRoueAvBy", "posArDRoueAvBz",
    "posAvDRoueAvBx", "posAvDRoueAvBy", "posAvDRoueAvBz",
    
    "posAvGRoueAvLx", "posAvGRoueAvLy", "posAvGRoueAvLz",
    "posArGRoueAvLx", "posArGRoueAvLy", "posArGRoueAvLz",
    "posArDRoueAvLx", "posArDRoueAvLy", "posArDRoueAvLz",
    "posAvDRoueAvLx", "posAvDRoueAvLy", "posAvDRoueAvLz",
    
    "posAvGRoueArHx", "posAvGRoueArHy", "posAvGRoueArHz",
    "posArGRoueArHx", "posArGRoueArHy", "posArGRoueArHz",
    "posArDRoueArHx", "posArDRoueArHy", "posArDRoueArHz",
    "posAvDRoueArHx", "posAvDRoueArHy", "posAvDRoueArHz",
    
    "posAvGRoueArBx", "posAvGRoueArBy", "posAvGRoueArBz",
    "posArGRoueArBx", "posArGRoueArBy", "posArGRoueArBz",
    "posArDRoueArBx", "posArDRoueArBy", "posArDRoueArBz",
    "posAvDRoueArBx", "posAvDRoueArBy", "posAvDRoueArBz",
    
    "posAvGRoueArLx", "posAvGRoueArLy", "posAvGRoueArLz",
    "posArGRoueArLx", "posArGRoueArLy", "posArGRoueArLz",
    "posArDRoueArLx", "posArDRoueArLy", "posArDRoueArLz",
    "posAvDRoueArLx", "posAvDRoueArLy", "posAvDRoueArLz",
    "railGH", "railGB","railGLat", "railGLev",
    "railDH", "railDB","railDLat", "railDLev"
    ]
#_____________________________________________________________________________________________________________________________________________________________________
def eq_system(t, stateVectorY, ft, tmpfile, dt):
    '''
    Hypothèse : Le centre de gravité du véhicule ne se déplace pas.
    '''
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

    posCgN1 = np.array([xCg+vXCg*dt, yCg+vYCg*dt, zCg+vZCg*dt])
    anglesN1 = np.array([lacet+vLacet*dt, tangage+vTangage*dt, roulis+vRoulis*dt])
    posCgModAvGn1 = np.array([0, yCgModAvG+vYCgModAvG*dt, zCgModAvG+vZCgModAvG*dt])
    posCgModArGn1 = np.array([0, yCgModArG+vYCgModArG*dt, zCgModArG+vZCgModArG*dt])
    posCgModArDn1 = np.array([0, yCgModArD+vYCgModArD*dt, zCgModArD+vZCgModArD*dt])
    posCgModAvDn1 = np.array([0, yCgModAvD+vYCgModAvD*dt, zCgModAvD+vZCgModAvD*dt])
    

    #SECTION - Geométrie générale
    geomFromCgPod, geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD = geom.general_geometry(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD)
    geomFromCgPodN1, geomWorldPodN1, geomWorldAvGN1, geomWorldArGN1, geomWorldArDN1, geomWorldAvDN1, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1 = geom.general_geometry(posCgN1, anglesN1, posCgModAvGn1, posCgModArGn1, posCgModArDn1, posCgModAvDn1)
    vLrAvG, vLrArG, vLrArD, vLrAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD = geom.vitesse_variation_distances(dt, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1)
    #!SECTION

    #SECTION - Forces
    fAero, fProp, fGraviteOnMod, fGravs, fMags, fConts, fWheels, fBrakes, fAmorts, fReacts = fo.all_forces(t, xCg, vXCg, angles, distToAvG, distToArG, distToArD, distToAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD, lrAvG, lrArG, lrArD, lrAvD, vLrAvG, vLrArG, vLrArD, vLrAvD)
    #!SECTION

    #SECTION - Somme des forces
    sCgF, sModFAvG, sModFArG, sModFArD, sModFAvD = fo.somme_forces(fProp, fGraviteOnMod, fGravs, fAmorts, fAero, fBrakes, fConts, fMags, fReacts)
    #!SECTION

    #SECTION - Tenseur d'inertie
    tenseurInertie = geom.inertia_tensor_3D(geomFromCgPod)
    #!SECTION

    #SECTION - Somme des moments
    sCgT = fo.somme_moments(fReacts[0], fReacts[1], fReacts[2], fReacts[3], fProp, geomFromCgPod)
    #!SECTION

    #SECTION - Accelérations
    #Pod
    aXCg = sCgF[data.idx] / data.masseTotale
    aYCg = sCgF[data.idy] / data.masseOnMod
    aZCg = sCgF[data.idz] / data.masseOnMod
    aLacet =   sCgT[data.idz] / tenseurInertie[2][2] #for Ioz
    aTangage = sCgT[data.idy] / tenseurInertie[1][1] #for Ioy
    aRoulis =  sCgT[data.idx] / tenseurInertie[0][0] #for Iox
    #Modules
    aYCgModAvG = sModFAvG[data.idy] / data.podGeom[data.idCgMobileModuleAvG][data.idKg]
    aYCgModArG = sModFArG[data.idy] / data.podGeom[data.idCgMobileModuleArG][data.idKg]
    aYCgModArD = sModFArD[data.idy] / data.podGeom[data.idCgMobileModuleArD][data.idKg]
    aYCgModAvD = sModFAvD[data.idy] / data.podGeom[data.idCgMobileModuleAvD][data.idKg]

    aZCgModAvG = sModFAvG[data.idz] / data.podGeom[data.idCgMobileModuleAvG][data.idKg]
    aZCgModArG = sModFArG[data.idz] / data.podGeom[data.idCgMobileModuleArG][data.idKg]
    aZCgModArD = sModFArD[data.idz] / data.podGeom[data.idCgMobileModuleArD][data.idKg]
    aZCgModAvD = sModFAvD[data.idz] / data.podGeom[data.idCgMobileModuleAvD][data.idKg]
    #!SECTION
    
    #SECTION - Sauvegarde & monitoring
    railL = geom.rail(xCg, True)
    railR = geom.rail(xCg, False)
    dataline = [
        t, 
        xCg, vXCg, aXCg, yCg, vYCg, aYCg, zCg, vZCg, aZCg, np.rad2deg(tangage), vTangage, aTangage, np.rad2deg(lacet), vLacet, aLacet, np.rad2deg(roulis), vRoulis, aRoulis, 
        yCgModAvG, yCgModArG, yCgModArD, yCgModAvD, vYCgModAvG, vYCgModArG, vYCgModArD, vYCgModAvD, aYCgModAvG, aYCgModArG, aYCgModArD, aYCgModAvD, 
        zCgModAvG, zCgModArG, zCgModArD, zCgModAvD, vZCgModAvG, vZCgModArG, vZCgModArD, vZCgModAvD, aZCgModAvG, aZCgModArG, aZCgModArD, aZCgModAvD,
        fMags[0][data.idx], fMags[0][data.idy], fMags[0][data.idz],
        fMags[1][data.idx], fMags[1][data.idy], fMags[1][data.idz],
        fMags[2][data.idx], fMags[2][data.idy], fMags[2][data.idz],
        fMags[3][data.idx], fMags[3][data.idy], fMags[3][data.idz],
        fConts[0][data.idx], fConts[0][data.idy], fConts[0][data.idz],
        fConts[1][data.idx], fConts[1][data.idy], fConts[1][data.idz],
        fConts[2][data.idx], fConts[2][data.idy], fConts[2][data.idz],
        fConts[3][data.idx], fConts[3][data.idy], fConts[3][data.idz],
        fBrakes[0][data.idx], fBrakes[0][data.idy], fBrakes[0][data.idz],
        fBrakes[1][data.idx], fBrakes[1][data.idy], fBrakes[1][data.idz],
        fBrakes[2][data.idx], fBrakes[2][data.idy], fBrakes[2][data.idz],
        fBrakes[3][data.idx], fBrakes[3][data.idy], fBrakes[3][data.idz],
        fAmorts[0][data.idx], fAmorts[0][data.idy], fAmorts[0][data.idz],
        fAmorts[1][data.idx], fAmorts[1][data.idy], fAmorts[1][data.idz],
        fAmorts[2][data.idx], fAmorts[2][data.idy], fAmorts[2][data.idz],
        fAmorts[3][data.idx], fAmorts[3][data.idy], fAmorts[3][data.idz],
        sModFAvG[data.idx], sModFAvG[data.idy], sModFAvG[data.idz],
        sModFArG[data.idx], sModFArG[data.idy], sModFArG[data.idz],
        sModFArD[data.idx], sModFArD[data.idy], sModFArD[data.idz],
        sModFAvD[data.idx], sModFAvD[data.idy], sModFAvD[data.idz],
        distToAvG[data.idForceLevY]*1000, distToAvG[data.idForceLevZ]*1000,
        distToArG[data.idForceLevY]*1000, distToArG[data.idForceLevZ]*1000,
        distToArD[data.idForceLevY]*1000, distToArD[data.idForceLevZ]*1000,
        distToAvD[data.idForceLevY]*1000, distToAvD[data.idForceLevZ]*1000,
        lrAvG[data.idy], lrAvG[data.idz],
        lrArG[data.idy], lrArG[data.idz],
        lrArD[data.idy], lrArD[data.idz],
        lrAvD[data.idy], lrAvD[data.idz],
        lrAvG[data.idy]-data.l0Y, lrAvG[data.idz]-data.l0Z,
        lrArG[data.idy]-data.l0Y, lrArG[data.idz]-data.l0Z,
        lrArD[data.idy]-data.l0Y, lrArD[data.idz]-data.l0Z,
        lrAvD[data.idy]-data.l0Y, lrAvD[data.idz]-data.l0Z,
        vLrAvG[data.idy]*np.single(60000), vLrAvG[data.idz]*np.single(60000),
        vLrArG[data.idy]*np.single(60000), vLrArG[data.idz]*np.single(60000),
        vLrArD[data.idy]*np.single(60000), vLrArD[data.idz]*np.single(60000),
        vLrAvD[data.idy]*np.single(60000), vLrAvD[data.idz]*np.single(60000),

        geomWorldPod[data.idCgMobileModuleAvG][data.idx], geomWorldPod[data.idCgMobileModuleAvG][data.idy], geomWorldPod[data.idCgMobileModuleAvG][data.idz],
        geomWorldPod[data.idCgMobileModuleArG][data.idx], geomWorldPod[data.idCgMobileModuleArG][data.idy], geomWorldPod[data.idCgMobileModuleArG][data.idz],
        geomWorldPod[data.idCgMobileModuleArD][data.idx], geomWorldPod[data.idCgMobileModuleArD][data.idy], geomWorldPod[data.idCgMobileModuleArD][data.idz],
        geomWorldPod[data.idCgMobileModuleAvD][data.idx], geomWorldPod[data.idCgMobileModuleAvD][data.idy], geomWorldPod[data.idCgMobileModuleAvD][data.idz],
        geomWorldAvG[data.idFixDumper][data.idx], geomWorldAvG[data.idFixDumper][data.idy], geomWorldAvG[data.idFixDumper][data.idz],
        geomWorldArG[data.idFixDumper][data.idx], geomWorldArG[data.idFixDumper][data.idy], geomWorldArG[data.idFixDumper][data.idz],
        geomWorldArD[data.idFixDumper][data.idx], geomWorldArD[data.idFixDumper][data.idy], geomWorldArD[data.idFixDumper][data.idz],
        geomWorldAvD[data.idFixDumper][data.idx], geomWorldAvD[data.idFixDumper][data.idy], geomWorldAvD[data.idFixDumper][data.idz],
        geomWorldAvG[data.idForceLevY][data.idx], geomWorldAvG[data.idForceLevY][data.idy], geomWorldAvG[data.idForceLevY][data.idz],
        geomWorldArG[data.idForceLevY][data.idx], geomWorldArG[data.idForceLevY][data.idy], geomWorldArG[data.idForceLevY][data.idz],
        geomWorldArD[data.idForceLevY][data.idx], geomWorldArD[data.idForceLevY][data.idy], geomWorldArD[data.idForceLevY][data.idz],
        geomWorldAvD[data.idForceLevY][data.idx], geomWorldAvD[data.idForceLevY][data.idy], geomWorldAvD[data.idForceLevY][data.idz],
        geomWorldAvG[data.idForceLevZ][data.idx], geomWorldAvG[data.idForceLevZ][data.idy], geomWorldAvG[data.idForceLevZ][data.idz],
        geomWorldArG[data.idForceLevZ][data.idx], geomWorldArG[data.idForceLevZ][data.idy], geomWorldArG[data.idForceLevZ][data.idz],
        geomWorldArD[data.idForceLevZ][data.idx], geomWorldArD[data.idForceLevZ][data.idy], geomWorldArD[data.idForceLevZ][data.idz],
        geomWorldAvD[data.idForceLevZ][data.idx], geomWorldAvD[data.idForceLevZ][data.idy], geomWorldAvD[data.idForceLevZ][data.idz],
        
        geomWorldAvG[data.idForceRoueAvH][data.idx], geomWorldAvG[data.idForceRoueAvH][data.idy], geomWorldAvG[data.idForceRoueAvH][data.idz],
        geomWorldArG[data.idForceRoueAvH][data.idx], geomWorldArG[data.idForceRoueAvH][data.idy], geomWorldArG[data.idForceRoueAvH][data.idz],
        geomWorldArD[data.idForceRoueAvH][data.idx], geomWorldArD[data.idForceRoueAvH][data.idy], geomWorldArD[data.idForceRoueAvH][data.idz],
        geomWorldAvD[data.idForceRoueAvH][data.idx], geomWorldAvD[data.idForceRoueAvH][data.idy], geomWorldAvD[data.idForceRoueAvH][data.idz],
        
        geomWorldAvG[data.idForceRoueAvB][data.idx], geomWorldAvG[data.idForceRoueAvB][data.idy], geomWorldAvG[data.idForceRoueAvB][data.idz],
        geomWorldArG[data.idForceRoueAvB][data.idx], geomWorldArG[data.idForceRoueAvB][data.idy], geomWorldArG[data.idForceRoueAvB][data.idz],
        geomWorldArD[data.idForceRoueAvB][data.idx], geomWorldArD[data.idForceRoueAvB][data.idy], geomWorldArD[data.idForceRoueAvB][data.idz],
        geomWorldAvD[data.idForceRoueAvB][data.idx], geomWorldAvD[data.idForceRoueAvB][data.idy], geomWorldAvD[data.idForceRoueAvB][data.idz],
        
        geomWorldAvG[data.idForceRoueAvL][data.idx], geomWorldAvG[data.idForceRoueAvL][data.idy], geomWorldAvG[data.idForceRoueAvL][data.idz],
        geomWorldArG[data.idForceRoueAvL][data.idx], geomWorldArG[data.idForceRoueAvL][data.idy], geomWorldArG[data.idForceRoueAvL][data.idz],
        geomWorldArD[data.idForceRoueAvL][data.idx], geomWorldArD[data.idForceRoueAvL][data.idy], geomWorldArD[data.idForceRoueAvL][data.idz],
        geomWorldAvD[data.idForceRoueAvL][data.idx], geomWorldAvD[data.idForceRoueAvL][data.idy], geomWorldAvD[data.idForceRoueAvL][data.idz],
        
        geomWorldAvG[data.idForceRoueArH][data.idx], geomWorldAvG[data.idForceRoueArH][data.idy], geomWorldAvG[data.idForceRoueArH][data.idz],
        geomWorldArG[data.idForceRoueArH][data.idx], geomWorldArG[data.idForceRoueArH][data.idy], geomWorldArG[data.idForceRoueArH][data.idz],
        geomWorldArD[data.idForceRoueArH][data.idx], geomWorldArD[data.idForceRoueArH][data.idy], geomWorldArD[data.idForceRoueArH][data.idz],
        geomWorldAvD[data.idForceRoueArH][data.idx], geomWorldAvD[data.idForceRoueArH][data.idy], geomWorldAvD[data.idForceRoueArH][data.idz],
        
        geomWorldAvG[data.idForceRoueArB][data.idx], geomWorldAvG[data.idForceRoueArB][data.idy], geomWorldAvG[data.idForceRoueArB][data.idz],
        geomWorldArG[data.idForceRoueArB][data.idx], geomWorldArG[data.idForceRoueArB][data.idy], geomWorldArG[data.idForceRoueArB][data.idz],
        geomWorldArD[data.idForceRoueArB][data.idx], geomWorldArD[data.idForceRoueArB][data.idy], geomWorldArD[data.idForceRoueArB][data.idz],
        geomWorldAvD[data.idForceRoueArB][data.idx], geomWorldAvD[data.idForceRoueArB][data.idy], geomWorldAvD[data.idForceRoueArB][data.idz],
        
        geomWorldAvG[data.idForceRoueArL][data.idx], geomWorldAvG[data.idForceRoueArL][data.idy], geomWorldAvG[data.idForceRoueArL][data.idz],
        geomWorldArG[data.idForceRoueArL][data.idx], geomWorldArG[data.idForceRoueArL][data.idy], geomWorldArG[data.idForceRoueArL][data.idz],
        geomWorldArD[data.idForceRoueArL][data.idx], geomWorldArD[data.idForceRoueArL][data.idy], geomWorldArD[data.idForceRoueArL][data.idz],
        geomWorldAvD[data.idForceRoueArL][data.idx], geomWorldAvD[data.idForceRoueArL][data.idy], geomWorldAvD[data.idForceRoueArL][data.idz],
        railL[0], railL[1], railL[2], railL[3],
        railR[0], railR[1], railR[2], railR[3]
        ]
    save.in_tmp(tmpfile, dataline)
    monitor_eq(t, vXCg, tangage, lacet, roulis, xCg, yCg, zCg, distToAvG[data.idForceLevY]*1000, distToAvG[data.idForceLevZ]*1000,
        distToArG[data.idForceLevY]*1000, distToArG[data.idForceLevZ]*1000,
        distToArD[data.idForceLevY]*1000, distToArD[data.idForceLevZ]*1000,
        distToAvD[data.idForceLevY]*1000, distToAvD[data.idForceLevZ]*1000,
        fProp[0], sCgF[data.idx]-fProp[0], aXCg)
    
    if t>np.single(0) and t <= data.bstDureeDecharge and aXCg <= np.single(1):
        data.finishFlag = True  #Flag for event

    #!SECTION
    if data.debug:
        auto_test.debug(t, geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD)
    return np.array([vXCg, vYCg, vZCg, vLacet, vTangage, vRoulis, 
                     aXCg, aYCg, aZCg, aLacet, aTangage, aRoulis, 
                     vYCgModAvG, vZCgModAvG, vYCgModArG, vZCgModArG, vYCgModArD, vZCgModArD, vYCgModAvD, vZCgModAvD, 
                     aYCgModAvG, aZCgModAvG, aYCgModArG, aZCgModArG, aYCgModArD, aZCgModArD, aYCgModAvD, aZCgModAvD])
#_____________________________________________________________________________________________________________________________________________________________________
def monitor_eq(t, vX, tangage, lacet, roulis, xCg, yCg, zCg, deltaYAvG, deltaZAvG, deltaYArG, deltaZArG, deltaYArD, deltaZArD, deltaYAvD, deltaZAvD, fProp, fDrag, aXCg):
    #eval = round(t/data.manualTravelDuration*100, 0)
    eval = round(xCg/data.posXCgStop*100, monitorDec)
    if data.lastPercent < eval:
        print("\nProgress : %.3f,\ttime : %.3f, vitesse : %.3f,\n\ttangage : %.3f, lacet : %.3f, roulis : %.3f, \n\txCg : %.3f, yCg : %.3f, zCg : %.3f, \n\tentrefers: AvG Y %.1f Z %.1f \tArG Y %.1f Z %.1f \tArD Y %.1f Z %.1f \tAvD Y %.1f Z %.1f, \n\tFprop %dN \tFdrag %dN \tAXCg %.3fm_s2" %(eval, t, vX, np.rad2deg(tangage), np.rad2deg(lacet), np.rad2deg(roulis), xCg, yCg, zCg, deltaYAvG, deltaZAvG, deltaYArG, deltaZArG, deltaYArD, deltaZArD, deltaYAvD, deltaZAvD, fProp, fDrag, aXCg))
        data.lastPercent = eval
        return True
#_____________________________________________________________________________________________________________________________________________________________________
def simulation(tmpFile):
    global start_time
    start_time = time.time()
    t = np.linspace(0, data.manualTravelDuration, round(data.manualTravelDuration * data.stepPerSecond))
    npts = len(t)
    dt = np.single(data.manualTravelDuration / npts)
    temp = 200.0 * np.ones(npts)
    tempf = interpolate.interp1d(t, temp,fill_value="extrapolate")
    
    ###Solver###
    #event.direction = -1
    event.terminal = True # Try false, this gives the result but integrates beyond the event I need.

    Y0 = init.conditions_initiales()
    solution = integrate.solve_ivp(eq_system, [0,max(t)], Y0, method='RK45',
                                    first_step=dt, max_step=dt, 
                                    events = event,
                                    #atol=1e-6, rtol= 1e-3,
                                    atol=1e-7, rtol= 1e-4,
                                    #atol=1e-9, rtol= 1e-6,
                                    args=(tempf, tmpFile, dt))
    print("nb echantillons = ", len(solution.t))
    print("LA SOLUTION :\n", solution)
    return solution
#_____________________________________________________________________________________________________________________________________________________________________
def event(t,x,a,b,c):
    run_time = time.time() - start_time
    #print(t, "\t", x, "\t", a,b,c)
    if (x[0] > data.podLength/2 and x[6] <= np.single(1E-5) and t > np.single(1)) or (x[0] >= data.posXCgStop) or (run_time > data.runTimeLimit) or (data.finishFlag) or (type(data.errorDescriptor)==type(ValueError)): # or (t>np.single(0) and t <= data.bstDureeDecharge and aXCg == 0):
        print("\nEvent found")
        print("Position : %.1f/%.1f m"%(x[0], data.posXCgStop))
        print("Speed    : %.1f/%.1f m/s"%(x[6], 0))
        print("Duration : %.1f/%.1f(max) s"%(t, data.manualTravelDuration))
        print("Run time : %.3f/%.3f s"%(run_time, data.runTimeLimit))
        print("Error descriptor", data.errorDescriptor)
        return False
    else:
        #print("False...")
        return True
#_____________________________________________________________________________________________________________________________________________________________________
