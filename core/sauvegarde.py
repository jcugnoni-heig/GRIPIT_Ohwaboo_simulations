# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import csv
import os
import pandas as pd
import numpy as np

import core.user_inputs as user
import scenarios.datas as dt
import core.simulation as sim
import scenarios.scenarios_masses as scma

#_____________________________________________________________________________________________________________________________________________________________________
def in_tmp(tmpfile, dataline):
    write = csv.writer(tmpfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    write.writerow(dataline)
#_____________________________________________________________________________________________________________________________________________________________________
def in_csv(solution, fieldNames=sim.fieldNames):
    df = pd.read_csv(dt.outputTmpFileName, delimiter=';')
    j = 0
    with open(dt.outputFileName, 'w', encoding='UTF8', newline='') as csvfile :
        write = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        write.writerow(fieldNames)
        print("len df :", len(df.t))
        for i in range(len(df.t)):
            if j == len(solution.t):
                csvfile.close()
                break
            if (np.isclose(df.at[i, 't'], solution.t[j])):
                if (np.single(df.at[i, 'xCg']) == np.single(solution.y[0][j]) and np.single(df.at[i, 'zCg']) == np.single(solution.y[2][j])):
                    write.writerow(df.iloc[i])
                    j += 1
        csvfile.close()
#_____________________________________________________________________________________________________________________________________________________________________
#def solution_in_csv(solution, ODEfieldnames):
#    with open(dt.outputSolutionFileName, 'w', encoding='UTF8', newline='') as csvfile :
#        write = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
#        write.writerow(ODEfieldnames)
#        for i in range(len(solution.t)):
#                write.writerow([solution.t[i], 
#                    solution.y[0][i], solution.y[1][i], solution.y[2][i], solution.y[3][i], solution.y[4][i], solution.y[5][i], solution.y[6][i], solution.y[7][i], solution.y[8][i], solution.y[9][i],
#                    solution.y[10][i], solution.y[11][i], solution.y[12][i], solution.y[13][i], solution.y[14][i], solution.y[15][i], solution.y[16][i], solution.y[17][i], solution.y[18][i], solution.y[19][i],
#                    solution.y[20][i], solution.y[21][i], solution.y[22][i], solution.y[23][i], solution.y[24][i], solution.y[25][i]
#                    ])
#        csvfile.close()
#_____________________________________________________________________________________________________________________________________________________________________
def create_dir():
    #dt.folderPath = str(dt.originPath + "/Z init %dmm - kZ %.1E kY %.1E ksiZ %.3f ksiY %.3f"%(dt.upLev*1000, dt.kZ, dt.kY, dt.ksiZ, dt.ksiY))
    dt.folderPath = str(dt.originPath + "/mult_mag_%.2f-Fprop_%dN-zMin_%dmm-kZ_%.1E-kY_%.1E-ksiZ_%.3f-ksiY_%.3f"%(dt.multMagZ, dt.bstForce, dt.upLev*1000, dt.kZ, dt.kY, dt.ksiZ, dt.ksiY))
    #dt.figuresPath = str(dt.folderPath + "/figures/")
    #dt.tmpPath = str(dt.folderPath + "/tmp/")
    #dt.airgapsPath = str(dt.originPath + "/comparaison")
    os.makedirs(dt.folderPath, exist_ok=True)
    os.makedirs(dt.defaultDir, exist_ok=True)
    os.makedirs(dt.outFile, exist_ok=True)
    #os.makedirs(dt.figuresPath, exist_ok=True)
    #os.makedirs(dt.airgapsPath, exist_ok=True)
    dt.outputTmpFileName = str(dt.folderPath + "/RecODE.tmp")
    dt.outputFileName = str(dt.folderPath + "/Output.csv")
    dt.outputSolutionFileName = str(dt.folderPath + "/SolutionODE.csv")
    #dt.figuresPath = str(dt.figuresPath+'/')
    #dt.outputFileName = dt.outputFileName
    #dt.airgapsPath = dt.airgapsPath
    img_dir()
    if user.demander_confirmation("Souhaitez-vous saisir le nom du pdf ?"):
        dt.pdfName = str(dt.pdfName + " - " + user.demander_texte() + ".pdf")
    else:
        dt.pdfName = str(dt.pdfName + "_Compte_rendu_simu-scenar_%s-mult_mag_%.2f-Fprop_%dN-zMin_%dmm-kZ_%.1E-kY_%.1E-ksiZ_%.3f-ksiY_%.3f.pdf"%(scma.masse_version, dt.multMagZ, dt.bstForce, dt.upLev*1000, dt.kZ, dt.kY, dt.ksiZ, dt.ksiY))

#_____________________________________________________________________________________________________________________________________________________________________
def img_dir():
    dt.img0_path = str(dt.tmpDir + "/" + "Resultats_integration_dans_le_temps" + ".png")
    dt.img1_path = str(dt.tmpDir + "/" + "Resultats_integration_selon_la_distance" + ".png")
    dt.img2_path = str(dt.tmpDir + "/" + "Entrefers_Z_selon_le_temps" + ".png")
    dt.img3_path = str(dt.tmpDir + "/" + "Entrefers_Y_selon_le_temps" + ".png")
    dt.img4_path = str(dt.tmpDir + "/" + "Positions_2D_-_s" + ".png")
    dt.img5_path = str(dt.tmpDir + "/" + "Forces_X_selon_le_temps_[N]" + ".png")
    dt.img6_path = str(dt.tmpDir + "/" + "Forces_Y_selon_le_temps_[N]" + ".png")
    dt.img7_path = str(dt.tmpDir + "/" + "Forces_Z_selon_le_temps_[N]" + ".png")
    dt.img8_path = str(dt.tmpDir + "/" + "Integration_modules_Y_-_s" + ".png")
    dt.img9_path = str(dt.tmpDir + "/" + "Integration_modules_Z_-_s" + ".png")
    dt.img10_path = str(dt.tmpDir + "/" + "Deformation_ressort_Y" + ".png")
    dt.img11_path = str(dt.tmpDir + "/" + "Deformation_ressort_Z" + ".png")
    dt.img12_path = str(dt.tmpDir + "/" + 'Magnetic_forces_for_ideal_air_gap_%dmm_magnets_%s.png'%(dt.idealYairGag*1000, dt.magnetDim))#Graph 3D forces EM
    dt.img13_path = str(dt.tmpDir + "/" + "Entrefers_Z_selon_la_distance" + ".png")
    dt.img14_path = str(dt.tmpDir + "/" + "Entrefers_Y_selon_la_distance" + ".png")

    dt.img15_path = str(dt.tmpDir + "/" + "Vitesse_deformation_ressort_Y" + ".png")
    dt.img16_path = str(dt.tmpDir + "/" + "Vitesse_deformation_ressort_Z" + ".png")
    dt.img17_path = str(dt.tmpDir + "/" + "Force_fct_deformation_ressorts_Y_[csv]" + ".png")
    dt.img18_path = str(dt.tmpDir + "/" + "Force_fct_deformation_ressorts_Z_[csv]" + ".png")
    dt.img19_path = str(dt.tmpDir + "/" + "Deformation_ressorts_Y_[csv]" + ".png")
    dt.img20_path = str(dt.tmpDir + "/" + "Deformation_ressorts_Z_[csv]" + ".png")
    dt.img21_path = str(dt.tmpDir + "/" + "Force_fct_vitesse_deformation_ressorts_Y_[csv]" + ".png")
    dt.img22_path = str(dt.tmpDir + "/" + "Force_fct_vitesse_deformation_ressorts_Z_[csv]" + ".png")
    dt.img23_path = str(dt.tmpDir + "/" + "Force_ressorts_Y_fct_temps_[csv]" + ".png")
    dt.img24_path = str(dt.tmpDir + "/" + "Force_ressorts_Z_fct_temps_[csv]" + ".png")

#_____________________________________________________________________________________________________________________________________________________________________
def specs_txt():
    with open(str(dt.originPath + "settings.txt"), 'a') as file:
        file.write("Simulation settings:\n")
        file.writelines(["--------------------\n",
                         "Magnets:\n",
                         f"\tdim magnets: {dt.magnetDim}\n",
                         f"\talu box: {dt.aluBox}\n",
                         f"\tc lev: {dt.cZlev}\n"])
        file.writelines(["--------------------\n",
                         "Dampers Y:\n",
                         f"\tksi y: {dt.ksiY}\n",
                         f"\tk y:   {dt.kY}\n"])
        file.writelines(["--------------------\n",
                         "Dampers Z:\n",
                         f"\tksi z: {dt.ksiZ}\n",
                         f"\tk z:   {dt.kZ}\n"])
    file.close()
#_____________________________________________________________________________________________________________________________________________________________________
def run_and_save():
    create_dir()
    tmpfile = None
    with open(dt.outputTmpFileName, 'w', encoding='UTF8', newline='') as tmpfile :
        write = csv.writer(tmpfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        write.writerow(sim.fieldNames)
        solution = sim.simulation(tmpfile)
        tmpfile.close()

        if type(dt.errorDescriptor) == type(ValueError):
            dt.stepPerSecond = dt.stepPerSecond * 1E1  #[Hz]  Default : 1E3 Hz
            print("Restart for file %s at %dHz"%(dt.fileInfo, dt.stepPerSecond))
            with open(dt.outputTmpFileName, 'w', encoding='UTF8', newline='') as tmpfile :
                write = csv.writer(tmpfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                write.writerow(sim.fieldNames)
                solution = sim.simulation(tmpfile)
                tmpfile.close()
    in_csv(solution)
    if user.demander_confirmation("Supprimer le fichier temporaire contenant les données ?"):
        os.remove(dt.outputTmpFileName)
#_____________________________________________________________________________________________________________________________________________________________________

#_____________________________________________________________________________________________________________________________________________________________________
