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


#_____________________________________________________________________________________________________________________________________________________________________
def oscillation(x):
    return np.single(dt.railMisalignement/2)*(np.cos(x*np.pi/(dt.LRail/2)))


#_____________________________________________________________________________________________________________________________________________________________________
def matrice_rotation(angles):
    #roulis = np.single(0)
    [lacet, tangage, roulis] = angles
    Rz = np.array([
        [np.cos(lacet), -np.sin(lacet), 0],
        [np.sin(lacet),  np.cos(lacet), 0],
        [0, 0, 1]
    ])
    Ry = np.array([
        [np.cos(tangage), 0, -np.sin(tangage)],
        [0, 1, 0],
        [np.sin(tangage), 0, np.cos(tangage)]
    ])
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(roulis), -np.sin(roulis)],
        [0, np.sin(roulis),  np.cos(roulis)]
    ])
    matRot = np.dot(np.dot(Rz, Ry), Rx)
    #matRot = np.dot(Rz, Ry)
    return matRot


#_____________________________________________________________________________________________________________________________________________________________________
def pos_element_X_Y_Z_from_cg(angles, vector):
    #Convention rayon-longitude-latitude : https://fr.wikipedia.org/wiki/Coordonn%C3%A9es_sph%C3%A9riques
    #Ne fonctionne pas pour le Z des modules suspendus
    Axyz = np.array([[vector[dt.idx]],
                     [vector[dt.idy]],
                     [vector[dt.idz]]])
    matRot = matrice_rotation(angles)
    [xPrim, yPrim, zPrim] = np.dot(matRot, Axyz)
    return [xPrim[0], yPrim[0], zPrim[0]]


#_____________________________________________________________________________________________________________________________________________________________________
def geometrie_vehicule_selon_cg(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD):
    '''Rotation du Pod autour de son centre de gravité le repère est orienté comme le repère monde'''
    geomFromCgPod = []
    for id in range(len(dt.podGeom)):
        [x, y, z] = pos_element_X_Y_Z_from_cg(angles, dt.podGeom[id])
        if id == dt.idCgMobileModuleAvG:
            y = posCgModAvG[dt.idy] - posCg[dt.idy]
            z = posCgModAvG[dt.idz] - posCg[dt.idz]
        elif id == dt.idCgMobileModuleArG:
            y = posCgModArG[dt.idy] - posCg[dt.idy]
            z = posCgModArG[dt.idz] - posCg[dt.idz]
        elif id == dt.idCgMobileModuleArD:
            y = posCgModArD[dt.idy] - posCg[dt.idy]
            z = posCgModArD[dt.idz] - posCg[dt.idz]
        elif id == dt.idCgMobileModuleAvD:
            y = posCgModAvD[dt.idy] - posCg[dt.idy]
            z = posCgModAvD[dt.idz] - posCg[dt.idz]
        geomFromCgPod.append([x, y, z])
    return geomFromCgPod


#_____________________________________________________________________________________________________________________________________________________________________
def positions_repere_pod(geomFromCgPod, angles):
    '''Coordonées des éléments dans le repère pod'''
    geomRelativeToCg = []
    archMobileAvGRelativeToCg = []
    archMobileArGRelativeToCg = []
    archMobileArDRelativeToCg = []
    archMobileAvDRelativeToCg = []
    anglesInv = [-angles[dt.idLacet], -angles[dt.idTangage], -angles[dt.idRoulis]]
    for id in range(len(geomFromCgPod)):
        [x, y, z] = pos_element_X_Y_Z_from_cg(anglesInv, geomFromCgPod[id])
        geomRelativeToCg.append([x, y, z])
    
    for id in range(len(dt.pointsMobilesAvG)):
        [x, y, z] = geomRelativeToCg[dt.idCgMobileModuleAvG] + dt.pointsMobilesAvG[id]
        archMobileAvGRelativeToCg.append([x, y, z])
    for id in range(len(dt.pointsMobilesArG)):
        [x, y, z] = geomRelativeToCg[dt.idCgMobileModuleArG] + dt.pointsMobilesArG[id]
        archMobileArGRelativeToCg.append([x, y, z])
    for id in range(len(dt.pointsMobilesArD)):
        [x, y, z] = geomRelativeToCg[dt.idCgMobileModuleArD] + dt.pointsMobilesArD[id]
        archMobileArDRelativeToCg.append([x, y, z])
    for id in range(len(dt.pointsMobilesAvD)):
        [x, y, z] = geomRelativeToCg[dt.idCgMobileModuleAvD] + dt.pointsMobilesAvD[id]
        archMobileAvDRelativeToCg.append([x, y, z])
    return geomRelativeToCg, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg


#_____________________________________________________________________________________________________________________________________________________________________
def longueurs_ressorts(geomRelativeToCg, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg):
    lrAvG = np.array([0,#archMobileAvGRelativeToCg[dt.idFixDumper][dt.idx] - geomRelativeToCg[dt.idFixAvG][dt.idx],
             archMobileAvGRelativeToCg[dt.idFixDumper][dt.idy] - geomRelativeToCg[dt.idFixAvG][dt.idy],
             -(archMobileAvGRelativeToCg[dt.idFixDumper][dt.idz] - geomRelativeToCg[dt.idFixAvG][dt.idz])+dt.lZpreCharge])
    
    lrArG = np.array([0,#archMobileArGRelativeToCg[dt.idFixDumper][dt.idx] - geomRelativeToCg[dt.idFixArG][dt.idx],
             archMobileArGRelativeToCg[dt.idFixDumper][dt.idy] - geomRelativeToCg[dt.idFixArG][dt.idy],
             -(archMobileArGRelativeToCg[dt.idFixDumper][dt.idz] - geomRelativeToCg[dt.idFixArG][dt.idz])+dt.lZpreCharge])
    
    lrArD = np.array([0,#-(archMobileArDRelativeToCg[dt.idFixDumper][dt.idx] - geomRelativeToCg[dt.idFixArD][dt.idx]),
             -(archMobileArDRelativeToCg[dt.idFixDumper][dt.idy] - geomRelativeToCg[dt.idFixArD][dt.idy]),
             -(archMobileArDRelativeToCg[dt.idFixDumper][dt.idz] - geomRelativeToCg[dt.idFixArD][dt.idz])+dt.lZpreCharge])
    
    lrAvD = np.array([0,#-(archMobileAvDRelativeToCg[dt.idFixDumper][dt.idx] - geomRelativeToCg[dt.idFixAvD][dt.idx]),
             -(archMobileAvDRelativeToCg[dt.idFixDumper][dt.idy] - geomRelativeToCg[dt.idFixAvD][dt.idy]),
             -(archMobileAvDRelativeToCg[dt.idFixDumper][dt.idz] - geomRelativeToCg[dt.idFixAvD][dt.idz])+dt.lZpreCharge])
    #lrAvG = lrAvG*np.array([1,-1,1])
    #lrArG = lrArG*np.array([1,-1,1])
    #lrArD = lrArD*np.array([1,-1,1])
    #lrAvD = lrAvD*np.array([1,-1,1])
    return lrAvG, lrArG, lrArD, lrAvD


#_____________________________________________________________________________________________________________________________________________________________________
def geom_world(posCg, angles, geomFromCgPod, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg):
    '''Coordonnées des éléments dans le repère monde'''
    geomWorldPod = []
    geomWorldAvG = []
    geomWorldArG = []
    geomWorldArD = []
    geomWorldAvD = []
    for id in range(len(geomFromCgPod)):
        x = geomFromCgPod[id][dt.idx] + posCg[dt.idx]
        y = geomFromCgPod[id][dt.idy] + posCg[dt.idy]
        z = geomFromCgPod[id][dt.idz] + posCg[dt.idz]
        m = dt.podGeom[id][dt.idKg]
        geomWorldPod.append([x, y, z, m])

    for coord in archMobileAvGRelativeToCg:
        [x, y, z] = posCg + pos_element_X_Y_Z_from_cg(angles, coord)
        geomWorldAvG.append([x, y, z])
    for coord in archMobileArGRelativeToCg:
        [x, y, z] = posCg + pos_element_X_Y_Z_from_cg(angles, coord)
        geomWorldArG.append([x, y, z])
    for coord in archMobileArDRelativeToCg:
        [x, y, z] = posCg + pos_element_X_Y_Z_from_cg(angles, coord)
        geomWorldArD.append([x, y, z])
    for coord in archMobileAvDRelativeToCg:
        [x, y, z] = posCg + pos_element_X_Y_Z_from_cg(angles, coord)
        geomWorldAvD.append([x, y, z])
    return geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD


#_____________________________________________________________________________________________________________________________________________________________________
def rail(x, isLeft = True):
    shift = oscillation(x)
    if isLeft:
        faceRoueHaut = dt.hRail
        faceRoueBas = faceRoueHaut - dt.tRail
        faceLat = dt.demiEspacementRails - dt.tRail/2
        faceLevZ = dt.tRail
    else:
        faceRoueHaut = dt.hRail
        faceRoueBas = faceRoueHaut - dt.tRail
        faceLat = -dt.demiEspacementRails + dt.tRail/2
        faceLevZ = dt.tRail
    return [faceRoueHaut+shift, faceRoueBas+shift, faceLat+shift, faceLevZ+shift]


#_____________________________________________________________________________________________________________________________________________________________________
def ecarts_aux_rails(point, itemId, isLeft=True):
    [faceRoueHaut, faceRoueBas, faceLat, faceLevZ] = rail(point[dt.idx], isLeft)
    espFaceRoueH = point[dt.idz] - faceRoueHaut
    espFaceRoueB = faceRoueBas - point[dt.idz]
    espFaceLevZ = point[dt.idz] - faceLevZ
    if isLeft:
        espFaceLat = faceLat - point[dt.idy]
    else:
        espFaceLat = -(faceLat - point[dt.idy])
    if itemId == dt.idFRH:
        return espFaceRoueH
    elif itemId == dt.idFRB:
        return espFaceRoueB
    elif itemId == dt.idFRLat or itemId == dt.idFLevY:
        return espFaceLat
    elif itemId == dt.idFLevZ:
        return espFaceLevZ
    

#_____________________________________________________________________________________________________________________________________________________________________
def general_geometry(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD):
    geomFromCgPod = geometrie_vehicule_selon_cg(posCg, angles, posCgModAvG, posCgModArG, posCgModArD, posCgModAvD)
    geomRelativeToCg, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg = positions_repere_pod(geomFromCgPod, angles)
    lrAvG, lrArG, lrArD, lrAvD = longueurs_ressorts(geomRelativeToCg, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg)
    geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD = geom_world(posCg, angles, geomFromCgPod, archMobileAvGRelativeToCg, archMobileArGRelativeToCg, archMobileArDRelativeToCg, archMobileAvDRelativeToCg)
    #Ecarts aux rails
    #Roues avant du haut Z
    espRoueAvHAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueAvH], dt.idFRH, True)
    espRoueAvHArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueAvH], dt.idFRH, True)
    espRoueAvHArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueAvH], dt.idFRH, False)
    espRoueAvHAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueAvH], dt.idFRH, False)
    #Roues avant du bas Z
    espRoueAvBAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueAvB], dt.idFRB, True)
    espRoueAvBArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueAvB], dt.idFRB, True)
    espRoueAvBArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueAvB], dt.idFRB, False)
    espRoueAvBAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueAvB], dt.idFRB, False)
    #Roues avant latérales Y
    espRoueAvLAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueAvL], dt.idFRLat, True)
    espRoueAvLArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueAvL], dt.idFRLat, True)
    espRoueAvLArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueAvL], dt.idFRLat, False)
    espRoueAvLAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueAvL], dt.idFRLat, False)
    #Roues arrière du haut Z
    espRoueArHAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueArH], dt.idFRH, True)
    espRoueArHArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueArH], dt.idFRH, True)
    espRoueArHArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueArH], dt.idFRH, False)
    espRoueArHAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueArH], dt.idFRH, False)
    #Roues arrière du bas Z
    espRoueArBAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueArB], dt.idFRB, True)
    espRoueArBArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueArB], dt.idFRB, True)
    espRoueArBArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueArB], dt.idFRB, False)
    espRoueArBAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueArB], dt.idFRB, False)
    #Roues arrière latérales Y
    espRoueArLAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceRoueArL], dt.idFRLat, True)
    espRoueArLArG = ecarts_aux_rails(geomWorldArG[dt.idForceRoueArL], dt.idFRLat, True)
    espRoueArLArD = ecarts_aux_rails(geomWorldArD[dt.idForceRoueArL], dt.idFRLat, False)
    espRoueArLAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceRoueArL], dt.idFRLat, False)
    #entrefer lev Y
    entreferYAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceLevY], dt.idFLevY, True)
    entreferYArG = ecarts_aux_rails(geomWorldArG[dt.idForceLevY], dt.idFLevY, True)
    entreferYArD = ecarts_aux_rails(geomWorldArD[dt.idForceLevY], dt.idFLevY, False)
    entreferYAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceLevY], dt.idFLevY, False)
    #Entrefer lev Z
    entreferZAvG = ecarts_aux_rails(geomWorldAvG[dt.idForceLevZ], dt.idFLevZ, True)
    entreferZArG = ecarts_aux_rails(geomWorldArG[dt.idForceLevZ], dt.idFLevZ, True)
    entreferZArD = ecarts_aux_rails(geomWorldArD[dt.idForceLevZ], dt.idFLevZ, False)
    entreferZAvD = ecarts_aux_rails(geomWorldAvD[dt.idForceLevZ], dt.idFLevZ, False)
    
    distToAvG = np.array([0,0, espRoueAvHAvG, espRoueAvBAvG, espRoueAvLAvG, espRoueArHAvG, espRoueArBAvG, espRoueArLAvG, 0, entreferYAvG, entreferZAvG])
    distToArG = np.array([0,0, espRoueAvHArG, espRoueAvBArG, espRoueAvLArG, espRoueArHArG, espRoueArBArG, espRoueArLArG, 0, entreferYArG, entreferZArG])
    distToArD = np.array([0,0, espRoueAvHArD, espRoueAvBArD, espRoueAvLArD, espRoueArHArD, espRoueArBArD, espRoueArLArD, 0, entreferYArD, entreferZArD])
    distToAvD = np.array([0,0, espRoueAvHAvD, espRoueAvBAvD, espRoueAvLAvD, espRoueArHAvD, espRoueArBAvD, espRoueArLAvD, 0, entreferYAvD, entreferZAvD])
    if dt.dispVal:
        print()
        print("Dist AvG: rAvH %.3f   rAvB %.3f   rAvL %.3f   \trArH %.3f   rArB %.3f   rArL %.3f   \tagY %.3f   agZ %.3f"%(distToAvG[2], distToAvG[3], distToAvG[4], distToAvG[5], distToAvG[6], distToAvG[7], distToAvG[9], distToAvG[10]))
        print("Dist ArG: rAvH %.3f   rAvB %.3f   rAvL %.3f   \trArH %.3f   rArB %.3f   rArL %.3f   \tagY %.3f   agZ %.3f"%(distToArG[2], distToArG[3], distToArG[4], distToArG[5], distToArG[6], distToArG[7], distToArG[9], distToArG[10]))
        print("Dist ArD: rAvH %.3f   rAvB %.3f   rAvL %.3f   \trArH %.3f   rArB %.3f   rArL %.3f   \tagY %.3f   agZ %.3f"%(distToArD[2], distToArD[3], distToArD[4], distToArD[5], distToArD[6], distToArD[7], distToArD[9], distToArD[10]))
        print("Dist AvD: rAvH %.3f   rAvB %.3f   rAvL %.3f   \trArH %.3f   rArB %.3f   rArL %.3f   \tagY %.3f   agZ %.3f"%(distToAvD[2], distToAvD[3], distToAvD[4], distToAvD[5], distToAvD[6], distToAvD[7], distToAvD[9], distToAvD[10]))
    return geomFromCgPod, geomWorldPod, geomWorldAvG, geomWorldArG, geomWorldArD, geomWorldAvD, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD


#_____________________________________________________________________________________________________________________________________________________________________
def vitesse_variation_distances(deltaT, lrAvG, lrArG, lrArD, lrAvD, distToAvG, distToArG, distToArD, distToAvD, lrAvGn1, lrArGn1, lrArDn1, lrAvDn1, distToAvGn1, distToArGn1, distToArDn1, distToAvDn1):
    vLrAvG = (lrAvGn1-lrAvG)*deltaT  #[(lrAvGn1[dt.idx]-lrAvG[dt.idx])*deltaT, (lrAvGn1[dt.idy]-lrAvG[dt.idy])*deltaT, (lrAvGn1[dt.idz]-lrAvG[dt.idz])*deltaT]
    vLrArG = (lrArGn1-lrArG)*deltaT  #[(lrArGn1[dt.idx]-lrArG[dt.idx])*deltaT, (lrArGn1[dt.idy]-lrArG[dt.idy])*deltaT, (lrArGn1[dt.idz]-lrArG[dt.idz])*deltaT]
    vLrArD = (lrArDn1-lrArD)*deltaT  #[(lrArDn1[dt.idx]-lrArD[dt.idx])*deltaT, (lrArDn1[dt.idy]-lrArD[dt.idy])*deltaT, (lrArDn1[dt.idz]-lrArD[dt.idz])*deltaT]
    vLrAvD = (lrAvDn1-lrAvD)*deltaT  #[(lrAvDn1[dt.idx]-lrAvD[dt.idx])*deltaT, (lrAvDn1[dt.idy]-lrAvD[dt.idy])*deltaT, (lrAvDn1[dt.idz]-lrAvD[dt.idz])*deltaT]
    vDistToAvG = (distToAvGn1-distToAvG)*deltaT #[(distToAvGn1[dt.idFRH]-distToAvG[dt.idFRH])*deltaT, (distToAvGn1[dt.idFRB]-distToAvG[dt.idFRB])*deltaT, (distToAvGn1[dt.idFRLat]-distToAvG[dt.idFRLat])*deltaT, (distToAvGn1[dt.idFLevY]-distToAvG[dt.idFLevY])*deltaT, (distToAvGn1[dt.idFLevZ]-distToAvG[dt.idFLevZ])*deltaT]
    vDistToArG = (distToArGn1-distToArG)*deltaT #[(distToArGn1[dt.idFRH]-distToArG[dt.idFRH])*deltaT, (distToArGn1[dt.idFRB]-distToArG[dt.idFRB])*deltaT, (distToArGn1[dt.idFRLat]-distToArG[dt.idFRLat])*deltaT, (distToArGn1[dt.idFLevY]-distToArG[dt.idFLevY])*deltaT, (distToArGn1[dt.idFLevZ]-distToArG[dt.idFLevZ])*deltaT]
    vDistToArD = (distToArDn1-distToArD)*deltaT #[(distToArDn1[dt.idFRH]-distToArD[dt.idFRH])*deltaT, (distToArDn1[dt.idFRB]-distToArD[dt.idFRB])*deltaT, (distToArDn1[dt.idFRLat]-distToArD[dt.idFRLat])*deltaT, (distToArDn1[dt.idFLevY]-distToArD[dt.idFLevY])*deltaT, (distToArDn1[dt.idFLevZ]-distToArD[dt.idFLevZ])*deltaT]
    vDistToAvD = (distToAvDn1-distToAvD)*deltaT #[(distToAvDn1[dt.idFRH]-distToAvD[dt.idFRH])*deltaT, (distToAvDn1[dt.idFRB]-distToAvD[dt.idFRB])*deltaT, (distToAvDn1[dt.idFRLat]-distToAvD[dt.idFRLat])*deltaT, (distToAvDn1[dt.idFLevY]-distToAvD[dt.idFLevY])*deltaT, (distToAvDn1[dt.idFLevZ]-distToAvD[dt.idFLevZ])*deltaT]
    
    return vLrAvG, vLrArG, vLrArD, vLrAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD


#_____________________________________________________________________________________________________________________________________________________________________
def inertia_tensor_3D(geomFromCgPod):
    Iox = 0
    Ioy = 0
    Ioz = 0
    Ixy = 0
    Ixz = 0
    Iyz = 0
    for i in range(len(geomFromCgPod)):
        Iox += dt.podGeom[i][dt.idKg] * (pow(geomFromCgPod[i][dt.idy], 2) + pow(geomFromCgPod[i][dt.idz], 2))
        Ioy += dt.podGeom[i][dt.idKg] * (pow(geomFromCgPod[i][dt.idx], 2) + pow(geomFromCgPod[i][dt.idz], 2))
        Ioz += dt.podGeom[i][dt.idKg] * (pow(geomFromCgPod[i][dt.idx], 2) + pow(geomFromCgPod[i][dt.idy], 2))

        Ixy += dt.podGeom[i][dt.idKg] * geomFromCgPod[i][dt.idx] * geomFromCgPod[i][dt.idy]
        Ixz += dt.podGeom[i][dt.idKg] * geomFromCgPod[i][dt.idx] * geomFromCgPod[i][dt.idz]
        Iyz += dt.podGeom[i][dt.idKg] * geomFromCgPod[i][dt.idz] * geomFromCgPod[i][dt.idz]
    tensorIcg = np.array([[Iox, -Ixy, -Ixz], [-Ixy, Ioy, -Iyz], [-Ixz, -Iyz, Ioz]])
    return tensorIcg


#_____________________________________________________________________________________________________________________________________________________________________
