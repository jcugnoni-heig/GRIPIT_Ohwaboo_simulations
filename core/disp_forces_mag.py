# Copyright © 2025 Maxence Cailleteau - HEIG-VD - GRIPIT
# SPDX‑License‑Identifier: GPL‑3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License 
# and any later version.
#______________________________________________________________________


import numpy as np
import matplotlib.pyplot as plt
import core.forces as fo
import scenarios.datas as dt
import core.display as dsp

#Standard DPI = 100
DPI = 100
maxW = 19.20
maxH = 10.80

elev =  16
azim = -35
roll =  0

#_____________________________________________________________________________________________________________________________________________________________________
def view_3d_magn_forces():
    dy = dt.idealYairGag    #np.single(20)
    vitesse = np.linspace(0, 40, 40)
    airgap = np.linspace(0, 50, 50)
    X, Y = np.meshgrid(airgap, vitesse)

    Zlev = []
    Zdrag = []
    Zguid = []
    for x in vitesse :   #Axe Y
        rowLev = []
        rowDrag = []
        rowGuid = []
        for y in airgap : # Axe X
            if dt.magnetDim == "30mm_230828":
                force = fo.f_mag_30mm_230828(dy, y, x)
                forceGuid = fo.f_mag_30mm_230828(y, dy, x)
            elif dt.magnetDim == "40mm_230828":
                force = fo.f_mag_40mm_230828(dy, y, x)
                forceGuid = fo.f_mag_40mm_230828(y, dy, x)
            elif dt.magnetDim == "30mm_230922":
                force = fo.f_mag_30mm_230922(dy, y, x)
                forceGuid = fo.f_mag_30mm_230922(y, dy, x)
            elif dt.magnetDim == "30mm_230928":
                force = fo.f_mag_30mm_230928(dy, y, x)
                forceGuid = fo.f_mag_30mm_230928(y, dy, x)
            elif dt.magnetDim == "40mm_231201":
                force = fo.f_mag_40mm_231201(dy, y, x)
                forceGuid = fo.f_mag_40mm_231201(y, dy, x)
            rowDrag.append(-force[0])
            rowGuid.append(forceGuid[1])
            rowLev.append(force[2])
        Zdrag.append(rowDrag)
        Zguid.append(rowGuid)
        Zlev.append(rowLev)
    Zdrag = np.array(Zdrag)
    Zguid = np.array(Zguid)
    Zlev = np.array(Zlev)
    zMax = Zlev.max()
    #zMax = Zdrag.max()

    fig = plt.figure(num = 'Magnetic forces - magnets : %s'%(dt.magnetDim), figsize=(maxW, maxH/1.8))
    plt.rcParams.update(plt.rcParamsDefault)
    plt.rcParams["figure.autolayout"] = True
    fig.suptitle('Magnetic forces for ideal air gap = %.1fmm - magnets : %s'%(dt.idealYairGag*1000, dt.magnetDim), fontsize=16)
    
    axX = fig.add_subplot(1, 3, 1, projection='3d')
    axX.plot_surface(X, Y, Zdrag, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    axX.set_title('Drag (-X)')
    axX.set_xlabel('mm')
    axX.set_ylabel('m/s')
    axX.set_zlabel('N')
    axX.set_xlim3d(0, 50)
    axX.set_ylim3d(0, 40)
    axX.set_zlim3d(0, zMax)
    axX.view_init(elev=elev, azim=azim, vertical_axis='z')

    axY = fig.add_subplot(1, 3, 2, projection='3d')
    axY.plot_surface(X, Y, Zguid, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    axY.set_title('Guidance (Y)')
    axY.set_xlabel('mm')
    axY.set_ylabel('m/s')
    axY.set_zlabel('N')
    axY.set_xlim3d(0, 50)
    axY.set_ylim3d(0, 40)
    axY.set_zlim3d(0, zMax)
    #axY.view_init(elev, azim, roll)
    axX.view_init(elev=elev, azim=azim, vertical_axis='z')

    axZ = fig.add_subplot(1, 3, 3, projection='3d')
    axZ.plot_surface(X, Y, Zlev, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    axZ.set_title('Levitation (Z)')
    axZ.set_xlabel('mm')
    axZ.set_ylabel('m/s')
    axZ.set_zlabel('N')
    axZ.set_xlim3d(0, 50)
    axZ.set_ylim3d(0, 40)
    axZ.set_zlim3d(0, zMax)
    #axZ.view_init(elev, azim, roll)
    axX.view_init(elev=elev, azim=azim, vertical_axis='z')

    plt.savefig(dt.img12_path)
    return fig


def view_2d():
    speed = np.linspace(0, 30, 300)

    fig_drag, axs_drag = plt.subplots(3)
    fig_drag.suptitle("Drag - %s"%(dt.magnetDim))
    force_id = 0
    airgapY = np.single(5)
    force_func(airgapY, np.single(5),  speed, axs_drag[0], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_drag[0], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_drag[0], force_id).legend()
    airgapY = np.single(10)
    force_func(airgapY, np.single(5),  speed, axs_drag[1], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_drag[1], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_drag[1], force_id).legend()
    airgapY = np.single(20)
    force_func(airgapY, np.single(5),  speed, axs_drag[2], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_drag[2], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_drag[2], force_id).legend()

    fig_guid, axs_guid = plt.subplots(3)
    fig_guid.suptitle("Guidance - %s"%(dt.magnetDim))
    force_id = 1
    airgapY = np.single(5)
    force_func(airgapY, np.single(5),  speed, axs_guid[0], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_guid[0], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_guid[0], force_id).legend()
    airgapY = np.single(10)
    force_func(airgapY, np.single(5),  speed, axs_guid[1], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_guid[1], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_guid[1], force_id).legend()
    airgapY = np.single(20)
    force_func(airgapY, np.single(5),  speed, axs_guid[2], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_guid[2], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_guid[2], force_id).legend()

    fig_lift, axs_lift = plt.subplots(3)
    fig_lift.suptitle("Lift - %s"%(dt.magnetDim))
    force_id = 1
    airgapY = np.single(5)
    force_func(airgapY, np.single(5),  speed, axs_lift[0], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_lift[0], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_lift[0], force_id).legend()
    airgapY = np.single(10)
    force_func(airgapY, np.single(5),  speed, axs_lift[1], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_lift[1], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_lift[1], force_id).legend()
    airgapY = np.single(20)
    force_func(airgapY, np.single(5),  speed, axs_lift[2], force_id).legend()
    force_func(airgapY, np.single(10), speed, axs_lift[2], force_id).legend()
    force_func(airgapY, np.single(20), speed, axs_lift[2], force_id).legend()


def force_func(airgapY, airgapZ, speed, axe, index):
    force = []
    for vx in speed:
        f = fo.f_mag_30mm_230928(airgapY, airgapZ, vx)[index]
        if index == 0:
            f = -f
        force.append(f)
    line, = axe.plot(speed, force)
    axe.set_title("Air gap Y %d mm"%(airgapY))
    axe.set_xlabel("Speed m/s")
    axe.set_ylabel("Force N")
    axe.grid()
    line.set_label("Air gap Z %d mm"%(airgapZ))
    return axe
#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    view_2d()
    view_3d_magn_forces()
    dt.magnetDim = "30mm_230928"
    view_3d_magn_forces()
    plt.show()
    