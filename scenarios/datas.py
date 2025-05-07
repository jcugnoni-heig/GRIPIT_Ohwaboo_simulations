# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import numpy as np
import os
from datetime import datetime
from main import yFactor, mainDir
import core.user_inputs as user
import scenarios.scenarios_masses as scma
#print("Max int 64", np.iinfo(np.int64).max)
#print("Max int 32", np.iinfo(np.int32).max)

upLev = 0.009#8   #entre 5 & 8mm
runTimeLimit = np.single(2 * 60 * 60) #s -->2h 0min

versionAmorto = "V1"

g = np.single(-9.81)
#_____________________________________________________________________________________________________________________________________________________________________
mTot = scma.vehiculeTot
masseModule = scma.mModule
masseTotale = np.single(0)
masseOnMod = np.single(0)
masseOnLev = np.single(0)

#_____________________________________________________________________________________________________________________________________________________________________
runSimu = True
debug = False
dispVal = False
cancelFMagnMeters = np.single(0)
lastPercent = 0
stepPerSecond = 1E3  #[Hz]
manualTravelDuration = np.single(10) #[s]
dateTime = datetime.now().strftime("%m-%d")
dir_path = str(mainDir + "/sim_results")
defaultDir = str(dir_path + "/ODE")
originPath = str(defaultDir + "/%s"%(dateTime))
outFile = str(dir_path + "/reports/")
folderPath = None
#figuresPath = None
tmpPath = None
airgapsPath = None
outputTmpFileName = None
outputFileName = None
outputSolutionFileName = None
tmpDir = "C:/tmp"
htmlName = str(datetime.now().strftime("%m-%d_%H-%M") + "_Compte_rendu_simu.html")
pdfName = datetime.now().strftime("%m-%d_%H-%M")
fileInfo = ""

#_____________________________________________________________________________________________________________________________________________________________________
#Files path
img0_path = None
img1_path = None
img2_path = None
img3_path = None
img4_path = None
img5_path = None
img6_path = None
img7_path = None
img8_path = None
img9_path = None
img10_path = None
img11_path = None
img12_path = None    #Graph 3D forces EM
img13_path = None
img14_path = None
img15_path = None
img16_path = None
img17_path = None
img18_path = None
img19_path = None
img20_path = None
img21_path = None
img22_path = None
img23_path = None
img24_path = None

#_____________________________________________________________________________________________________________________________________________________________________
errorDescriptor = False
finishFlag = False

#_____________________________________________________________________________________________________________________________________________________________________
def y_factor(yFactor):
    if yFactor == np.single(0.05):
        fYmagGoal = np.single(7)
    elif yFactor == np.single(0.1):
        fYmagGoal = np.single(14)
    elif yFactor == np.single(0.25):
        fYmagGoal = np.single(34)
    else :
        fYmagGoal = np.single(35)
    return fYmagGoal

#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Levitation
## Magnets
#magnetDim = "40"
#magnetDim = "30mm_230828"
#magnetDim = "40mm_230828"
#magnetDim = "30mm_230922"
magnetDim = "30mm_230928"
## Amortissement
cZlev = 89 #[Ns/m] Alu box 5mm
aluBox = "5"
## Factor drag
coefDrag = np.single(0.6)
#coefDrag = np.single(1)
#yFactor = np.single(0.1)    #5, 10, 25%
fYmagGoal = y_factor(yFactor)
multMagX = np.single(1)
multMagY = np.single(1)
multMagZ = np.single(1)
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Amortisseur V1
if versionAmorto == "V1":
    idealYairGag = np.single(0.010) #m #20mm
    idealYwheelGap = idealYairGag - np.single(0.010)

    if magnetDim == "30mm_230928":
        kyFactor = np.single(1)
        kzFactor = np.single(1)
        #fYmagGoal = np.single(145)/4 #bstForce = 2700N
        #fYmagGoal = np.single(158) #bstForce = 3200N
        #fYmagGoal = np.single(180) #bstForce = 5400N
        fYmagGoal = np.single(190)/4 #bstForce = 6000N
    else:
        kyFactor = np.single(1)
        kzFactor = np.single(1)

    largeurAmortisseurY = np.single(0.175)  #m
    l0Y = np.single(0.030)  #m
    l0Z = np.single(0.060)  #m
    lYpreCharge = np.single(0.015)  #m
    lZpreCharge = np.single(0.030)  #m

    fYprecharge = (1-kyFactor) * fYmagGoal*kyFactor
    fZprecharge = (1-kzFactor) * (mTot-4*masseModule)/4*9.81*kzFactor

    ##kY = np.single(2000) #N/m
    ##kY = np.single(-35/(lYpreCharge-idealYwheelGap-l0Y))#2000) #N/m
    kY = np.single(-fYmagGoal/(lYpreCharge-idealYwheelGap-l0Y)) * kyFactor  #N/m
    kZ = np.single(-(mTot-4*masseModule)/4*9.81/(lZpreCharge-l0Z)) * kzFactor #N/m
    ksiY = np.single(0.707)#707) #- 1
    ksiZ = np.single(0.707)#707) #- 1
    cY = ksiY * 2 * np.sqrt(kY * scma.mOnLev/4) #N.s/m
    cZ = ksiZ * 2 * np.sqrt(kZ * scma.mOnLev/4) #N.s/m
    print("\nAmortisseurs")
    print("\tkY : %.3E N/mm, précharge : %d N, course : %d mm"%(kY/1000, fYmagGoal*kyFactor, -(lYpreCharge-idealYwheelGap-l0Y)*1000))
    print("\tkZ : %.3E N/mm, précharge : %d N, course : %d mm"%(kZ/1000, (mTot-4*masseModule)/4*9.81*kzFactor, -(lZpreCharge-l0Z)*1000))
    print("\tksiY : %.3f"%(ksiY))
    print("\tksiZ : %.3f"%(ksiZ))
    print("\tcY : %.3f N.s/m"%(cY))
    print("\tcZ : %.3f N.s/m"%(cZ))
#!SECTION

#SECTION - Amortisseur V1   29/11/2023
if versionAmorto == "V1.1":
    idealYairGag = np.single(0.010) #m #20mm
    idealYwheelGap = idealYairGag - np.single(0.010)

    if magnetDim == "30mm_230928":
        kyFactor = np.single(1)
        kzFactor = np.single(1)
        #fYmagGoal = np.single(145)/4 #bstForce = 2700N
        #fYmagGoal = np.single(158) #bstForce = 3200N
        #fYmagGoal = np.single(180) #bstForce = 5400N
        fYmagGoal = np.single(190)/4 #bstForce = 6000N
    else:
        kyFactor = np.single(1)
        kzFactor = np.single(1)

    largeurAmortisseurY = np.single(0.175)  #m
    l0Y = np.single(0.030)  #m
    l0Z = np.single(0.060)  #m
    lYpreCharge = np.single(0.015)  #m
    lZpreCharge = np.single(0.030)  #m

    fYprecharge = (1-kyFactor) * fYmagGoal*kyFactor
    fZprecharge = (1-kzFactor) * (mTot-4*masseModule)/4*9.81*kzFactor

    kY = np.single(-fYmagGoal/(lYpreCharge-idealYwheelGap-l0Y)) * kyFactor  #N/m    #@171.4kg : 3166N/m
    kZ = np.single(-(mTot-4*masseModule)/4*9.81/(lZpreCharge-l0Z)) * kzFactor #N/m   #@171.4kg : 9810N/m
    cY = np.single(1000)   #N.s/m    #@171.4kg : 30.82 N.s/m
    cZ = np.single(1000)   #N.s/m    #@171.4kg : 54.25 N.s/m
    ksiY = cY / (2 * np.sqrt(kY * scma.mOnLev/4)) #N.s/m    #@171.4kg : 0.1 -
    ksiZ = cZ / (2 * np.sqrt(kZ * scma.mOnLev/4)) #N.s/m    #@171.4kg : 0.1 -

    print("\nAmortisseurs")
    print("\tkY : %.3E N/mm, précharge : %d N, course : %d mm"%(kY/1000, fYmagGoal*kyFactor, -(lYpreCharge-idealYwheelGap-l0Y)*1000))
    print("\tkZ : %.3E N/mm, précharge : %d N, course : %d mm"%(kZ/1000, (mTot-4*masseModule)/4*9.81*kzFactor, -(lZpreCharge-l0Z)*1000))
    print("\tksiY : %.3f"%(ksiY))
    print("\tksiZ : %.3f"%(ksiZ))
    print("\tcY : %.3f N.s/m"%(cY))
    print("\tcZ : %.3f N.s/m"%(cZ))
#!SECTION

#SECTION - Amortisseur V2
elif versionAmorto == "V2":
    idealYairGag = np.single(0.020) #m
    idealYwheelGap = idealYairGag - np.single(0.010)

    largeurAmortisseurY = np.single(0.175)  #m
    lYpreCharge = np.single(0.015)  #m
    lZpreCharge = np.single(0.030)  #m
    lY = lYpreCharge-idealYwheelGap
    lZ = lZpreCharge
    fZmagGoal = (mTot-4*masseModule)/4*9.81

    if magnetDim == "30mm_230828" or magnetDim == "40mm_230828":
        kY = np.single(1  *1000)    #N/m note: 0.28 N/mm
        kZ = np.single(3 *1000)    #N/m note: 6.38 N/mm   VTT : 85N/mm (Samson)
    elif magnetDim == "30mm_230928":
        kY = np.single(1  *1000)    #N/m 
        kZ = np.single(0.1 *1000)    #N/m 

    l0Y = np.single(y_factor(yFactor)/kY+lY)  #m
    l0Z = np.single(fZmagGoal/kZ+lZ)  #m

    print("\nAmortisseurs")
    print("\tkY : %.1E N/mm, \tprécharge : %d N,    \tcourse : %d mm, \tl0 : %.3f mm"%(kY/1000, fYmagGoal, -(lY-l0Y)*1000, l0Y*1000))
    print("\tkZ : %.1E N/mm, \tprécharge : %d N, \tcourse : %d mm, \tl0 : %.3f mm"%(kZ/1000, (mTot-4*masseModule)/4*9.81, -(lZ-l0Z)*1000, l0Z*1000))

    ksiY = np.single(1)#707) #-
    ksiZ = np.single(1)#707) #-
    print("\tksiY : %.3f"%(ksiY))
    print("\tksiZ : %.3f"%(ksiZ))
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Coordonnées 
podGeom = np.array([    #x, y, z, kg    ref : 3D origine
    [ 0,      0,     0, scma.mChassis],  #CG châssis
    [ 0,      0,     0, scma.mCoque],  #CG coque
    [ 0,      0,     0, scma.mChargement],  #CG chargement
    [ 0,      0,     0, scma.totBooster],  #CG propulseur
    [-0.610,  0,     -0., 0],   #Pts F propulsion
    [ 0.495,  0.170 + largeurAmortisseurY, 0, 0],   #Pts fixation amortisseur avant gauche
    [-0.495,  0.170 + largeurAmortisseurY, 0, 0],   #Pts fixation amortisseur arrière gauche
    [-0.495, -0.170 - largeurAmortisseurY, 0, 0],   #Pts fixation amortisseur arrière droit
    [ 0.495, -0.170 - largeurAmortisseurY, 0, 0],   #Pts fixation amortisseur avant droit
    [ 0.406,  0.324 + l0Y, -lZpreCharge, masseModule], #CG Mobile module AvG
    [-0.406,  0.324 + l0Y, -lZpreCharge, masseModule], #CG Mobile module ArG
    [-0.406, -0.324 - l0Y, -lZpreCharge, masseModule], #CG Mobile module ArD
    [ 0.406, -0.324 - l0Y, -lZpreCharge, masseModule]  #CG Mobile module AvD
])
masseTot = 0
for item in podGeom:
    masseTot += item[3]
mTot = masseTot
print("Masses")
print("\tTotal masse: %dkg"%(masseTot))
print("\tMasse module : %dkg"%(masseModule))

idx = 0
idy = 1
idz = 2
idKg = 3

idLacet = 0
idTangage = 1
idRoulis = 2

idChassis = 0
idCoque = 1
idLoad = 2
idProp = 3
idForceProp = 4
idFixAvG = 5
idFixArG = 6
idFixArD = 7
idFixAvD = 8
idCgMobileModuleAvG = 9
idCgMobileModuleArG = 10
idCgMobileModuleArD = 11
idCgMobileModuleAvD = 12

idModule = 0
idFixDumper = 1
idForceRoueAvH = 2
idForceRoueAvB = 3
idForceRoueAvL = 4
idForceRoueArH = 5
idForceRoueArB = 6
idForceRoueArL = 7
idForceFrein = 8
idForceLevY = 9
idForceLevZ = 10

pointsMobilesAvG = np.array([   #x, y, z    ref : CG module
    [ 0,     0,      0,   ],  #CG module
    [ 0.089, 0.021,  0    ],   #Pts fixation amortisseur
    [ 0.239, 0.048,  0.055],   #Pts F roue AvH
    [ 0.239, 0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue AvB
    [ 0.239, 0.085, -0.053],   #Pts F roue AvL
    [-0.209, 0.048,  0.055],   #Pts F roue ArH
    [-0.209, 0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue ArB
    [-0.209, 0.085, -0.053],   #Pts F roue ArL
    [-0.110, 0.048,  0.045],   #Pts F frein
    [ 0.089, 0.075, -0.053 -0.005 + upLev],   #Pts F lévitation Y
    [ 0.089, 0.050, -0.078 -0.005 + upLev]    #Pts F lévitation Z
])

pointsMobilesArG = np.array([   #x, y, z, kg    ref : CG module
    [ 0,     0,      0,   ],  #CG module
    [-0.089, 0.021,  0    ],   #Pts fixation amortisseur
    [-0.239, 0.048,  0.055],   #Pts F roue AvH
    [-0.239, 0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue AvB
    [-0.239, 0.085, -0.053],   #Pts F roue AvL
    [ 0.209, 0.048,  0.055],   #Pts F roue ArH
    [ 0.209, 0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue ArB
    [ 0.209, 0.085, -0.053],   #Pts F roue ArL
    [ 0.110, 0.048,  0.045],   #Pts F frein
    [-0.089, 0.075, -0.053 -0.005 + upLev],   #Pts F lévitation Y
    [-0.089, 0.050, -0.078 -0.005 + upLev]    #Pts F lévitation Z
])

pointsMobilesArD = np.array([   #x, y, z, kg    ref : CG module
    [ 0,      0,      0,   ],  #CG module
    [-0.089, -0.021,  0    ],   #Pts fixation amortisseur
    [-0.239, -0.048,  0.055],   #Pts F roue AvH
    [-0.239, -0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue AvB
    [-0.239, -0.085, -0.053],   #Pts F roue AvL
    [ 0.209, -0.048,  0.055],   #Pts F roue ArH
    [ 0.209, -0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue ArB
    [ 0.209, -0.085, -0.053],   #Pts F roue ArL
    [ 0.110, -0.048,  0.045],   #Pts F frein
    [-0.089, -0.075, -0.053 -0.005 + upLev],   #Pts F lévitation Y
    [-0.089, -0.050, -0.078 -0.005 + upLev]    #Pts F lévitation Z
])

pointsMobilesAvD = np.array([   #x, y, z, kg    ref : CG module
    [ 0,      0,      0    ],  #CG module
    [ 0.089, -0.021,  0    ],   #Pts fixation amortisseur
    [ 0.239, -0.048,  0.055],   #Pts F roue AvH
    [ 0.239, -0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue AvB
    [ 0.239, -0.085, -0.053],   #Pts F roue AvL
    [-0.209, -0.048,  0.055],   #Pts F roue ArH
    [-0.209, -0.048,  0.034-0.06 -0.005 + upLev],   #Pts F roue ArB
    [-0.209, -0.085, -0.053],   #Pts F roue ArL
    [-0.110, -0.048,  0.045],   #Pts F frein
    [ 0.089, -0.075, -0.053 -0.005 + upLev],   #Pts F lévitation Y
    [ 0.089, -0.050, -0.078 -0.005 + upLev]    #Pts F lévitation Z
])
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Piste
pisteLongueur = np.single(90)  #m (100)
securityDistance = np.single(10.0) #m
podLength = np.single(1.5) #[m]
posXCgStop = pisteLongueur - (podLength/2 + securityDistance)
#!SECTION
# #_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Rail Allega 3169111 
#LINK - https://www.allega.ch/fr/I-profile-presse-EN-755-2-EN-755-9/3169111
railMisalignement = np.single(0)    #[m]
demiEspacementRails = np.single(0.415)  #m
LRail = np.single(6)  #[m]
bRail = np.single(0.150)    #m
hRail = np.single(0.150)    #m
tRail = np.single(0.012)    #m
idFRH = 0
idFRB = 1
idFRLat = 2
idFLevY = 3
idFLevZ = 4
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Booster
bstDureeDecharge = np.single(1.346)#1.346)    #s
#pression = np.single(29.3)
pression = np.single(user.demander_valeur("Veuillez entrer la pression du réservoir (float) :"))
bstForce = np.single(pression/40*6000)  #N 2700, 3200, 4700, 5400, 6000 N
#bstForce = np.single(3800)  #N 2700, 3200, 4700, 5400, 6000 N
bstMasseFull = scma.totBooster # Kg
bstMasseEau  = scma.eauBooster #Kg
bstMasseVide = scma.cuveBooster #Kg
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Frein
flagFreinage = False
perfFrein = np.single(0.5)
maxDeceleration = np.single(-6 *(9.81)*(1400/2200*perfFrein)) #[m/s2]
fBrake = np.single(3500)    #DH 020 FPM 040
coefFriction = np.single(0.4)
nbBrakes = 4
tBraking = np.single(0)
#!SECTION
#_____________________________________________________________________________________________________________________________________________________________________
#SECTION - Roue
firstContactDist = np.single(1E-6) #m
if versionAmorto == "V1" or versionAmorto == "V1.2":
    wheelKy = np.single(1E8)#kY*(lYpreCharge-l0Y)/(-firstContactDist))#1E6)
    wheelKz = np.single(1E8)#-mTot/(4*2)*9.81/(-firstContactDist))#1E6) 343
else:
    wheelKy = np.single(1E10) #5E6 #N/m
    wheelKz = np.single(1E10) #2E8 #N/m
print("Wheel")
print("\tkY : %.1E N/mm"%(wheelKy/1000))
print("\tkZ : %.1E N/mm"%(wheelKz/1000))
wheelKsi = np.single(0.01)
coefFrotDyn = np.single(0.05)
#!SECTION

#_____________________________________________________________________________________________________________________________________________________________________

note_pdf = ""