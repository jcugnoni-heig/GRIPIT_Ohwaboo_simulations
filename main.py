# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import os
import numpy as np

yFactor = np.single(0.25)    #5, 10, 25%
mainDir = os.path.dirname(os.path.realpath(__file__))

import core.sauvegarde as save
import scenarios.datas as dt
import core.display as dsp
import core.analyse as anal
import core.disp_forces_mag as fm
import scenarios.script_rapport as srap
import scenarios.scenarios_masses as scma

from matplotlib import pyplot as plt
from tkinter import filedialog


#dt.runSimu = False

dt.cancelFMagnMeters = np.single(0) #Rail element : 6m  Default:0m
#dt.bstForce = np.single(6000)  #N 2700, 3200, 6000, 6700 Default:5400 N
dt.multMagX = np.single(0.89)#0.53)
dt.multMagY = np.single(0.79)#0.39)
dt.multMagZ = np.single(0.67)#0.37)

#dt.debug = True
#dt.dispVal = True

#dt.stepPerSecond = 1E2  #[Hz]  Default : 1E3 Hz
#dt.manualTravelDuration = np.single(0.005) #[s]    Deffault : 10s

# Magnets
#dt.magnetDim = "30mm_230828"    #Default.
#dt.magnetDim = "40"
#dt.magnetDim = "40mm_230828"
dt.magnetDim = "40mm_231201"
#dt.magnetDim = "30mm_230928"

dt.note_pdf = "\nMultiplicateurs tirés de la comparaison entre les valeurs de simulation magnétiques pour rail et alliage Constelium et <br> les valeurs des équations magnétiques du modèle.\nFacteurs pour passer de fsim_mag_30mm --> fnew_35mm."


#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    
    if dt.runSimu:
        #yn = input("\n\nAdd informations to folder name ? (a goes for all) s/e/a/y/n\n\t-->  ")
        yn = "s"
        if yn == "y" or yn == "Y":
            fileInfo = input("Type informations :\n\t-->  ")
            dt.originPath = dt.originPath + " - " + fileInfo
        elif yn == "a" or yn == "A":
            dt.originPath = dt.originPath + " - %dkg - mag %s - Fprop %dN - Fbrake %dN"%(dt.masseTot, dt.magnetDim, dt.bstForce, dt.fBrake)
        elif yn == "e" or yn == "E":
            dt.originPath = dt.originPath + " - mag_%s - Fprop %dN - zMin %dmm - yFactor %.2f - No magn rail %dm - Amorto_%s - kZ %.2fN_mm"%(dt.magnetDim, dt.bstForce, dt.upLev*1000, yFactor, dt.cancelFMagnMeters, dt.versionAmorto, dt.kZ/1000)
        elif yn == "s" or yn == "S":
            dt.originPath = dt.originPath + "scenar_%s"%(scma.masse_version)
        #Run simulation
        save.run_and_save()
        #Interprete
        df = dsp.read_file(fileName=dt.outputFileName)
        print("\nAdresse : %s" %(dt.outputFileName))
        #anal.analyse(df)
        #anal.analyse_fft(df)
        #print("\nAffichage des données...")
        #dsp.all_graphs(df)
    else:
        if dt.debug:
            plt.ion()
            plt.show()
            input("Press [enter] to continue.")
        else:
            filepath = filedialog.askopenfilename(title="Open a CSV File", filetypes=(("tab files","*.csv"), ("all files","*.*")), initialdir=dt.defaultDir)
            dt.outputFileName = filepath
            print("\nAdresse : %s" %(filepath))
            df = dsp.read_file(fileName=filepath)
            #anal.analyse(df)
            #anal.analyse_fft(df)
            #print("\nAffichage des données...")
            #dsp.all_graphs(df)
    print("\nAffichage des données...")
    fm.view_3d_magn_forces()
    #♣plt.show()

    dsp.all_graphs(df)
    #plt.show()
    #plt.close()
    srap.gen_html(srap.content(df))
    input_html_file = str(dt.outFile + dt.htmlName)
    output_pdf_file = str(dt.outFile + dt.pdfName)
    srap.html_to_pdf(input_html_file, output_pdf_file)
    anal.analyse(df)
    anal.analyse_fft(df)
    print("runned succesfully")

