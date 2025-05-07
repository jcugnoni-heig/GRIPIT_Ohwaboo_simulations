# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import numpy as np

#masse_version = "first-126kg"
#masse_version = "06_10_2023-165.4kg"
#masse_version = "17_10_2023-141.4kg"
#masse_version = "21_11_2023-171.4kg"
#masse_version = "05_12_2023-158.4kg"
masse_version = "01_11_2024-150.5kg-sans_coque"

if masse_version == "first-126kg":
    mModule = np.single(15)
    cuveBooster = np.single(20)
    eauBooster = np.single(12)
    mChassis = np.single(16)
    mCoque = np.single(10)
    mChargement = np.single(20)

elif masse_version == "06_10_2023-165.4kg":
    mModule = np.single(26.1)
    cuveBooster = np.single(20)
    eauBooster = np.single(25)
    mChassis = np.single(7)
    mCoque = np.single(14)
    mChargement = np.single(20)

elif masse_version == "17_10_2023-141.4kg":
    mModule = np.single(19.1)
    cuveBooster = np.single(20)
    eauBooster = np.single(25)
    mChassis = np.single(11)
    mCoque = np.single(14)
    mChargement = np.single(20)

elif masse_version == "21_11_2023-171.4kg":
    mModule = np.single(19.1)
    cuveBooster = np.single(50)
    eauBooster = np.single(25)
    mChassis = np.single(11)
    mCoque = np.single(14)
    mChargement = np.single(20)

elif masse_version == "05_12_2023-158.4kg":
    mModule = np.single(19.1)
    cuveBooster = np.single(37)
    eauBooster = np.single(25)
    mChassis = np.single(11)
    mCoque = np.single(14)
    mChargement = np.single(20)

elif masse_version == "01_11_2024-150.5kg-sans_coque":
    mModule = np.single(20.5)   #22kg sdw - réel: aimants 2,075kg/pièce; pince 5.2kg/pièce
    cuveBooster = np.single(37)
    eauBooster = np.single(20)  #20L max. Remplissage max pour chaque condition de pression.
    mChassis = np.single(11)
    mCoque = np.single(0)
    mChargement = np.single(20.5)

totBooster = cuveBooster + eauBooster
vehiculeAvide = 4*mModule + cuveBooster + mChassis + mCoque + mChargement
vehiculeTot =   4*mModule + totBooster  + mChassis + mCoque + mChargement
mOnLev = (vehiculeTot - 4*mModule)/4
print("Masses : véhicule à vide %.1f kg ; véhicule plein %.1f kg"%(vehiculeAvide, vehiculeTot))