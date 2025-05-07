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
#_____________________________________________________________________________________________________________________________________________________________________
def force_propulsion(t):
    fx = 0
    if t <= dt.bstDureeDecharge:
        fx = dt.bstForce
        dt.podGeom[dt.idProp][dt.idKg] = decharge_booster(t)
    else:
        fx = 0
        dt.podGeom[dt.idProp][dt.idKg] = dt.bstMasseVide
    fy = 0
    fz = 0
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def decharge_booster(t):
    return dt.bstMasseFull - dt.bstMasseEau*(t/dt.bstDureeDecharge)
#_____________________________________________________________________________________________________________________________________________________________________
def force_EM_module_rail_L(entreferY, entreferZ, xSpeed, zSpeed, xCg, isLeft=True):
    Numb_array_lev = np.single(1)            # Number of array of levitator
    #factor_Lift3D = 0.45           # 3D model Lift factor
    #factor_Drag3D = (100/60)      # 3D model Drag factor   factor_drag3D = 1" et une fois "factor_drag3D = 0.60"
    facteur_Y_3D = dt.yFactor#np.single(0.1)

    #Convertion en mm
    airgapY = entreferY * np.single(1000)
    airgapZ = entreferZ * np.single(1000)

    if airgapY<0:
        print("Warning dy:", airgapY)
        dt.errorDescriptor = ValueError("Warning dy is negative : %dmm ; isLeft: %s"%(airgapY, isLeft))
        #raise ValueError("Warning dy is negative : %dmm ; isLeft: %s"%(airgapY, isLeft))
        #input("Press [enter] to continue.")
    if airgapZ<0:
        print("Warning dz:", airgapZ)
        dt.errorDescriptor = ValueError("Warning dz is negative : %dmm ; isLeft: %s"%(airgapZ, isLeft))
        #raise ValueError("Warning dz is negative : %dmm ; isLeft: %s"%(airgapZ, isLeft))
        #input("Press [enter] to continue.")

    if dt.magnetDim == "36":
        if xSpeed > np.single(34):
            xSpeed = np.single(34)
            #input("Warning xSpeed > 34m/s out of maximum real speed = %.1f \nPress [enter] to continue."%(xSpeed))
        factor_Lift3D = np.single(0.45)        # 3D model Lift factor
        factor_Drag3D = dt.coefDrag #np.single(60/100) #1    # 3D model Drag factor 
        if xSpeed <= np.single(1):
            return np.array([0, 0, 0])
        elif xSpeed > np.single(34):
            return ValueError
        elif xSpeed <= np.single(4):
            fx = -(((-37.41*np.exp(-0.1255*airgapZ)-50.62*np.exp(-0.06537*airgapZ))*np.power(xSpeed, 2) + (332.7*np.exp(-0.118*airgapZ) + 368.4*np.exp(-0.06486*airgapZ))*xSpeed+(2.169*np.exp(-0.08053*airgapZ)-0.5871*np.exp(-0.3893*airgapZ)))*Numb_array_lev*factor_Drag3D)
        else:
            fx = -(((231.3*np.exp(-0.2223*airgapZ)+505.9*np.exp(-0.0801*airgapZ))*np.exp((-0.004979*np.exp(-0.07838*airgapZ)-0.0000000000000002348*np.exp(0.8392*airgapZ))*xSpeed)+(994*np.exp(-0.07565*airgapZ)+0.009433*np.exp(0.1438*airgapZ))*np.exp(-0.0870611111111111*xSpeed))*Numb_array_lev*factor_Drag3D)
        fy = ((1166*np.exp(-0.1248*airgapY)+1692*np.exp(-0.06784*airgapY))*np.exp((-0.00003608*airgapY+0.001438)*xSpeed)+(-1262*np.exp(-0.1224*airgapY)-1686*np.exp(-0.06716*airgapY))*np.exp((-0.171*np.exp(0.0003046*airgapY)+0.005959*np.exp(-0.03584*airgapY))*xSpeed))*Numb_array_lev*factor_Lift3D * facteur_Y_3D
        fz = ((1166*np.exp(-0.1248*airgapZ)+1692*np.exp(-0.06784*airgapZ))*np.exp((-0.00003608*airgapZ+0.001438)*xSpeed)+(-1262*np.exp(-0.1224*airgapZ)-1686*np.exp(-0.06716*airgapZ))*np.exp((-0.171*np.exp(0.0003046*airgapZ)+0.005959*np.exp(-0.03584*airgapZ))*xSpeed))*Numb_array_lev*factor_Lift3D
    
    elif dt.magnetDim == "40":
        if xSpeed > np.single(34):
            xSpeed = np.single(34)
            #input("Warning xSpeed > 34m/s out of maximum real speed = %.1f \nPress [enter] to continue."%(xSpeed))
        factor_Lift3D = np.single(0.45)           # 3D model Lift factor
        factor_Drag3D = dt.coefDrag #np.single(0.6)      # 3D model Drag factor --> essai à 0.6 et 1
        if xSpeed <= np.single(1):
            return np.array([0, 0, 0])
        elif xSpeed > np.single(34):
            return ValueError
        elif xSpeed <= np.single(4):
            fx = -((((6.117*np.exp(-0.1071*airgapZ)+6.276*np.exp(-0.05537*airgapZ))*np.power(xSpeed,3) + (-97.36*np.exp(-0.1078*airgapZ)-109.2*np.exp(-0.057*airgapZ))*np.power(xSpeed,2) +(432.1*np.exp(-0.1133*airgapZ)+630.9*np.exp(-0.06022*airgapZ))*xSpeed+(-1.093*np.exp(-0.1875*airgapZ)-1.581*np.exp(-0.05462*airgapZ))))*Numb_array_lev*factor_Drag3D)
        else:
            fx = -(((748.3*np.exp(-0.1017*airgapZ)+65.05*np.exp(-0.02038*airgapZ))*np.exp((-0.0000000006585*np.exp(0.405*airgapZ)-0.004471*np.exp(-0.1021*airgapZ))*xSpeed) + (1392*np.exp(-0.0697*airgapZ)-0.000000000000008039*np.exp(0.8489*airgapZ))*np.exp(-0.0912555555555556*xSpeed))*Numb_array_lev*factor_Drag3D)
        fy = ((1075*np.exp(-0.1282*airgapY)+2581*np.exp(-0.06456*airgapY))*np.exp((0.0000003799*np.power(airgapY, 2)-0.00004419*airgapY+0.001075)*xSpeed)+(-1120*np.exp(-0.1271*airgapY)-2653*np.exp(-0.06445*airgapY))*np.exp((0.0000006413*np.power(airgapY, 2)-0.000176*airgapY-0.1684)*xSpeed))*Numb_array_lev*factor_Lift3D * facteur_Y_3D
        fz = ((1075*np.exp(-0.1282*airgapZ)+2581*np.exp(-0.06456*airgapZ))*np.exp((0.0000003799*np.power(airgapZ, 2)-0.00004419*airgapZ+0.001075)*xSpeed)+(-1120*np.exp(-0.1271*airgapZ)-2653*np.exp(-0.06445*airgapZ))*np.exp((0.0000006413*np.power(airgapZ, 2)-0.000176*airgapZ-0.1684)*xSpeed))*Numb_array_lev*factor_Lift3D

    elif dt.magnetDim == "36old":
        if xSpeed > np.single(34):
            xSpeed = np.single(34)
            #input("Warning xSpeed > 34m/s out of maximum real speed = %.1f \nPress [enter] to continue."%(xSpeed))
        factor_Lift3D = np.single(0.7)           # 3D model Lift factor
        factor_Drag3D = np.single(100/95)      # 3D model Drag factor
        if xSpeed <= np.single(1):
            return np.array([0, 0, 0])
        elif xSpeed > np.single(34):
            return ValueError
        elif xSpeed <= np.single(4):
            fx =  -((-2.48*airgapZ +130.6)*xSpeed + (3002/np.power(airgapZ,1.468)+3.608))*factor_Drag3D*Numb_array_lev #OLD
        else:
            fx =  -((1.784*np.power(airgapZ,-0.256)-0.6167)*np.power(xSpeed,2) + (-121.9/np.power(airgapZ,0.3068)+34.14)*xSpeed + (2930/np.power(airgapZ,0.2841)-912.1))*factor_Drag3D*Numb_array_lev   #OLD
        fy = (((5277/np.power(airgapY,0.2267)-2114)+ (-6214/np.power(airgapY,0.2269)+2489)*np.exp(-0.19*xSpeed)))*factor_Lift3D*Numb_array_lev * facteur_Y_3D #OLD
        fz = (((5277/np.power(airgapZ,0.2267)-2114)+ (-6214/np.power(airgapZ,0.2269)+2489)*np.exp(-0.19*xSpeed)))*factor_Lift3D*Numb_array_lev  #OLD
    
    elif dt.magnetDim == "30mm_230828":
        [fx, fy, fz] = f_mag_30mm_230828(airgapY, airgapZ, xSpeed)
    elif dt.magnetDim == "40mm_230828":
        [fx, fy, fz] = f_mag_40mm_230828(airgapY, airgapZ, xSpeed)
    elif dt.magnetDim == "30mm_230922":
        [fx, fy, fz] = f_mag_30mm_230922(airgapY, airgapZ, xSpeed)
    elif dt.magnetDim == "30mm_230928":
        [fx, fy, fz] = f_mag_30mm_230928(airgapY, airgapZ, xSpeed)
    elif dt.magnetDim == "40mm_231201":
        [fx, fy, fz] = f_mag_40mm_231201(airgapY, airgapZ, xSpeed)

    if airgapZ < 0 :
        print(fx, fy, fz)
    if fz < 0:
        fz = 0
    if fx > 0 :
        fx = 0
    if fy < 0:
        fy = 0
    if isLeft :
        fy = -fy
    #Amortissement Z
    fz = fz - dt.cZlev*zSpeed
    if xCg < dt.cancelFMagnMeters:
        return np.array([0, 0, 0])
    else:
        fx = fx * dt.multMagX
        fy = fy * dt.multMagY
        fz = fz * dt.multMagZ
        return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def f_mag_30mm_230828(dy, dz, vx):
    vMax = np.single(34)
    if vx > vMax:
        vx = vMax
    #Drag
    if vx <= np.single(5):
        fx = -(((-51.31*np.exp(-0.096*dz))*np.power(vx,2)+(421.7*np.exp(-0.09688*dz))*vx+(-0.0000000000001903*np.exp(-0.11*dz)-0.00000000000002225*np.exp(-0.04239*dz)))*0.6)
    elif vx > np.single(5) and vx <= vMax:
        fx = -(((170.5*np.exp(-0.3847*dz)+441.3*np.exp(-0.1022*dz))*np.exp((0.0001069*np.exp(0.07026*dz)-0.006785*np.exp(-0.05505*dz))*vx)+(515.9*np.exp(-0.08508*dz)+0.0003042*np.exp(0.2113*dz))*np.exp((-0.0799066666666667)*vx))*0.6)
    #Lift & guidance
    if vx <= np.single(8):
        fy = (((103.3*np.exp(-0.1381*dy)+108.1*np.exp( -0.07726*dy))*vx+(0.1757*np.exp(-0.02688*dy)-0.2934*np.exp(-0.1835*dy)))*0.4) * dt.yFactor
        fz = (((103.3*np.exp(-0.1381*dz)+108.1*np.exp( -0.07726*dz))*vx+(0.1757*np.exp(-0.02688*dz)-0.2934*np.exp(-0.1835*dz)))*0.4)
    elif vx > np.single(8) and vx <= vMax:
        fy = (((-2353*np.exp(-0.1283*dy)-1324*np.exp(-0.06837*dy))*np.power(vx,(-0.6108*np.exp(0.008692*dy)+0.1129*np.exp(-0.8983*dy)))+(901.2*np.exp(-0.1689*dy)+1577*np.exp(-0.08661*dy)))*0.5)*dt.yFactor
        fz = (((-2353*np.exp(-0.1283*dz)-1324*np.exp(-0.06837*dz))*np.power(vx,(-0.6108*np.exp(0.008692*dz)+0.1129*np.exp(-0.8983*dz)))+(901.2*np.exp(-0.1689*dz)+1577*np.exp(-0.08661*dz)))*0.5)
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def f_mag_40mm_230828(dy, dz, vx):
    vMax = np.single(34)
    if vx > vMax:
        vx = vMax
    #Drag, Lift & guidance
    if vx <= np.single(5):
        fx = -(((6.117*np.exp(-0.1071*dz)+6.276*np.exp(-0.05537*dz))*np.power(vx,3)+(-97.36*np.exp(-0.1078*dz)-109.2*np.exp(-0.057*dz))*np.power(vx,2)+(432.1*np.exp(-0.1133*dz)+630.9*np.exp(-0.06022*dz))*vx+(-1.093*np.exp(-0.1875*dz)-1.581*np.exp(-0.05462*dz)))*0.7) 
        fy = (((124.3*np.exp(-0.2247*dy)+343.4*np.exp(-0.06505*dy))*vx+(-7.707*np.exp(-0.2085*dy)-24.57*np.exp(-0.05951*dy)))*0.55)*dt.yFactor
        fz = (((124.3*np.exp(-0.2247*dz)+343.4*np.exp(-0.06505*dz))*vx+(-7.707*np.exp(-0.2085*dz)-24.57*np.exp(-0.05951*dz)))*0.55) 
    elif vx > np.single(5) and vx <= vMax:
        fx = -(((748.3*np.exp(-0.1017*dz)+65.05*np.exp(-0.02038*dz))*np.exp((-0.0000000006585*np.exp(0.405*dz)-0.004471*np.exp(-0.1021*dz))*vx)+(1392*np.exp(-0.0697*dz)-0.000000000000008039*np.exp(0.8489*dz))*np.exp((-0.0912555555555556)*vx))*0.7)
        fy = (((-5325*np.exp(-0.08857* dy)-2124*np.exp(-0.04879* dy))*np.power(vx,(-0.8099*np.exp(0.004094* dy)+0.07554 *np.exp(-0.3414* dy)))+(974.9*np.exp(-0.1668* dy)+3363*np.exp(-0.06879*dy)))*0.55)*dt.yFactor
        fz = (((-5325*np.exp(-0.08857* dz)-2124*np.exp(-0.04879* dz))*np.power(vx,(-0.8099*np.exp(0.004094* dz)+0.07554 *np.exp(-0.3414* dz)))+(974.9*np.exp(-0.1668* dz)+3363*np.exp(-0.06879*dz)))*0.55)
    if fx > np.single(0):
        fx = np.single(0)
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def f_mag_40mm_231201(dy, dz, vx):
    vMax = np.single(34)
    yFactor = np.single(0.5)
    if vx > vMax:
        vx = vMax
    #Drag, Lift & guidance
    if vx <= np.single(5):
        fx = -(((6.117*np.exp(-0.1071*dz)+6.276*np.exp(-0.05537*dz))*np.power(vx,3)+(-97.36*np.exp(-0.1078*dz)-109.2*np.exp(-0.057*dz))*np.power(vx,2)+(432.1*np.exp(-0.1133*dz)+630.9*np.exp(-0.06022*dz))*vx+(-1.093*np.exp(-0.1875*dz)-1.581*np.exp(-0.05462*dz)))*0.7) 
        fy = (((124.3*np.exp(-0.2247*dy)+343.4*np.exp(-0.06505*dy))*vx+(-7.707*np.exp(-0.2085*dy)-24.57*np.exp(-0.05951*dy)))*0.55)*yFactor
        fz = (((124.3*np.exp(-0.2247*dz)+343.4*np.exp(-0.06505*dz))*vx+(-7.707*np.exp(-0.2085*dz)-24.57*np.exp(-0.05951*dz)))*0.55) 
    elif vx > np.single(5) and vx <= vMax:
        fx = -(((748.3*np.exp(-0.1017*dz)+65.05*np.exp(-0.02038*dz))*np.exp((-0.0000000006585*np.exp(0.405*dz)-0.004471*np.exp(-0.1021*dz))*vx)+(1392*np.exp(-0.0697*dz)-0.000000000000008039*np.exp(0.8489*dz))*np.exp((-0.0912555555555556)*vx))*0.7)
        fy = (((-5325*np.exp(-0.08857* dy)-2124*np.exp(-0.04879* dy))*np.power(vx,(-0.8099*np.exp(0.004094* dy)+0.07554 *np.exp(-0.3414* dy)))+(974.9*np.exp(-0.1668* dy)+3363*np.exp(-0.06879*dy)))*0.55)*yFactor
        fz = (((-5325*np.exp(-0.08857* dz)-2124*np.exp(-0.04879* dz))*np.power(vx,(-0.8099*np.exp(0.004094* dz)+0.07554 *np.exp(-0.3414* dz)))+(974.9*np.exp(-0.1668* dz)+3363*np.exp(-0.06879*dz)))*0.55)
    if fx > np.single(0):
        fx = np.single(0)
    #tir sans aimants
    fx = np.single(0)
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def f_mag_30mm_230922(dy, dz, vx):
    vMax = np.single(30)
    fxStep = np.single(5)
    fyStep = np.single(4)
    fzStep = np.single(8)
    if vx > vMax:
        vx = vMax

    #Drag
    if vx <= fxStep:
        fx = -(((-51.31*np.exp(-0.096*dz))*np.power(vx,2) + (421.7*np.exp(-0.09688*dz))*vx + (-0.0000000000001903*np.exp(-0.11*dz) - 0.00000000000002225*np.exp(-0.04239*dz)))*(2.007*np.power(dy,-0.4016)))
    elif vx > fxStep and vx <= vMax:
        fx = -(((170.5*np.exp(-0.3847*dz)+441.3*np.exp(-0.1022*dz))*np.exp((0.0001069*np.exp( 0.07026*dz)-0.006785*np.exp(-0.05505*dz))*vx)+(515.9*np.exp(-0.08508*dz)+0.0003042*np.exp(0.2113*dz))*np.exp((-0.0799066666666667)*vx))*(2.007*np.power(dy,-0.4016)))	

    #Guidance
    if vx <= fyStep:
        fy = (((-0.08001* np.power(dz,0.9999)+4.6)*vx)*( 10.59*np.exp(-0.1211*dy)))
    elif vx > fyStep and vx <= vMax:
        fy = (((4.37* dz -234.7)* np.power(vx,(-0.9363* np.power(dz,-0.0435)))+(80.49*np.exp(-0.01767* dz)))*(10.59*np.exp(-0.1211*dy)))

    #Lift
    if vx <= fzStep:
        fz = (((103.3*np.exp(-0.1381*dz)+108.1*np.exp( -0.07726*dz))*vx+(0.1757*np.exp( -0.02688*dz) -0.2934*np.exp(-0.1835*dz)))*0.4)
    elif vx > fzStep and vx <= vMax:
        fz = (((-2353*np.exp(-0.1283*dz)-1324*np.exp(-0.06837*dz))*np.power(vx,(-0.6108*np.exp(0.008692*dz)+0.1129*np.exp(-0.8983*dz)))+(901.2*np.exp(-0.1689*dz)+1577*np.exp(-0.08661*dz)))*0.56)
    
    #Verifications
    if fx > np.single(0):
        fx = np.single(0)
        print("Warning : fx was > 0")
    if fy < np.single(0):
        fy = np.single(0)
        print("Warning : fy was < 0")
    if fz < np.single(0):
        fz = np.single(0)
        print("Warning : fz was < 0")
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def f_mag_30mm_230928(dy, dz, vx):
    vMax = np.single(40)
    if vx > np.single(30):
        pass
        #print("Note that the speed is greater than the range of validity of the levitation equations: [5 ; 30] m/s.\tThe speed is %d m/s, tolerated up to %d m/s."%(vx, vMax))
    fxStep = np.single(5)
    fyStep = np.single(4)
    fzStep = np.single(8)
    dyLim = np.array([5, 20]) #mm
    dzLim = np.array([5, 15]) #mm
    if vx > vMax:
        vx = vMax
    
    if dy < dyLim[0]:
        #if dy < dyLim[0]-0.1:
        #    print("Note that the lateral Y air gap is below the range of validity of the guidance equations: [%d ; %d] mm. The air gap Y is %.4f mm."%(dyLim[0], dyLim[1], dy))
        dy = dyLim[0]
    elif dy > dyLim[1]:
        #print("Note that the lateral air gap is greater than the range of validity of the guidance equations: [%d ; %d] mm. The air gap Y is %.4f mm."%(dyLim[0], dyLim[1], dy))
        dy = dyLim[1]

    if dz < dzLim[0]:
        #if dz < dzLim[0]-0.1:
        #    print("Note that the lateral air gap is below the range of validity of the levitation equations: [%d ; %d] mm. The air gap Z is %.4f mm."%(dzLim[0], dzLim[1], dz))
        dz = dzLim[0]
    elif dz > dzLim[1]:
        #print("Note that the lateral air gap is greater than the range of validity of the levitation equations: [%d ; %d] mm. The air gap Z is %.4f mm."%(dzLim[0], dzLim[1], dz))
        dz = dzLim[1]

    #Drag
    if vx <= fxStep:
        fx = -(((-51.31*np.exp(-0.096*dz))*np.power(vx, 2)+(421.7*np.exp(-0.09688*dz))*vx+(-0.0000000000001903*np.exp(-0.11*dz)-0.00000000000002225*np.exp(-0.04239*dz)))*(2.007*np.power(dy, -0.4016)))
    elif vx > fxStep and vx <= vMax:
        fx = -(((170.5*np.exp(-0.3847*dz)+441.3*np.exp(-0.1022*dz))*np.exp((0.0001069*np.exp( 0.07026*dz)-0.006785*np.exp(-0.05505*dz))*vx)+(515.9*np.exp(-0.08508*dz)+0.0003042*np.exp(0.2113*dz))*np.exp((-0.0799066666666667)*vx))*(2.007*np.power(dy, -0.4016)))

    #Guidance
    if vx <= fyStep:
        fy = (((-0.08001* np.power(dz, 0.9999)+4.6)* vx)*( 10.59*np.exp(-0.1211*dy)))
    elif vx > fyStep and vx <= vMax:
        fy = (((4.37* dz -234.7)* np.power(vx, (-0.9363* np.power(dz, -0.0435)))+(80.49*np.exp(-0.01767* dz)))*(10.59*np.exp(-0.1211*dy)))

    #Lift
    if vx <= fzStep:
        fz = (((103.3*np.exp(-0.1381*dz)+108.1*np.exp(-0.07726*dz))*vx+(0.1757*np.exp(-0.02688*dz)-0.2934*np.exp(-0.1835*dz)))*0.4)
    elif vx > fzStep and vx <= vMax:
        fz = (((-2353*np.exp(-0.1283*dz)-1324*np.exp(-0.06837*dz))*np.power(vx, (-0.6108*np.exp(0.008692*dz)+0.1129*np.exp(-0.8983*dz)))+(901.2*np.exp(-0.1689*dz)+1577*np.exp(-0.08661*dz)))*0.56)
    
    #Verifications
    if fx > np.single(0):
        fx = np.single(0)
        #print("Warning : fx was > 0")
    if fy < np.single(0):
        fy = np.single(0)
        #print("Warning : fy was < 0")
    if fz < np.single(0):
        fz = np.single(0)
        #print("Warning : fz was < 0")
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def force_freinage(t, pXCg, vXCg, fResistX, masseTotale):
    sFx = -dt.coefFriction * dt.fBrake * dt.perfFrein * dt.nbBrakes + fResistX
    #sFx = (masseTotale * dt.maxDeceleration + fResistX)
    dax = sFx/masseTotale
    maxTime = -vXCg/dax
    breakingDistance = 0.5*dax*maxTime*maxTime+vXCg*maxTime
    if dt.flagFreinage == False:
        if (pXCg+breakingDistance >= dt.posXCgStop and vXCg >=1) or (pXCg > 10 and vXCg < 1 and vXCg > 0):
            dt.flagFreinage = True
            dt.tBraking = t
        else:
            fx=0
    if dt.flagFreinage == True:
        if vXCg > 0:
            fx = -dt.coefFriction * dt.fBrake * dt.perfFrein
            #fx = masseTotale * (dt.maxDeceleration)/dt.nbBrakes
        else:
            fx=0
    if pXCg > 0 and vXCg <= 0: #equivaut 0
        fx = 0
    fy = 0
    fz = 0
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def force_wheel_reaction(distFromRailToMod, vDistFromRailToMod, masseOnMod, isLeft=True):
    deltaAvL = distFromRailToMod[dt.idForceRoueAvL]
    deltaAvH = distFromRailToMod[dt.idForceRoueAvH]
    deltaAvB = distFromRailToMod[dt.idForceRoueAvB]
    deltaArL = distFromRailToMod[dt.idForceRoueArL]
    deltaArH = distFromRailToMod[dt.idForceRoueArH]
    deltaArB = distFromRailToMod[dt.idForceRoueArB]
    m = dt.masseModule + masseOnMod
    cy = dt.wheelKsi * 2*np.sqrt(dt.wheelKy*m)
    cz = dt.wheelKsi * 2*np.sqrt(dt.wheelKz*m)
    deltamin = dt.firstContactDist
    #fxAvL = 0
    #fxArL = 0
    #fxAvH = 0
    #fxArH = 0
    #fxAvB = 0
    #fxArB = 0
    #fyAvL = 0
    #fyArL = 0
    #fzAvH = 0
    #fzArH = 0
    #fzAvB = 0
    #fzArB = 0
    fAvL = np.array([0, 0, 0])
    fArL = np.array([0, 0, 0])
    fAvH = np.array([0, 0, 0])
    fArH = np.array([0, 0, 0])
    fAvB = np.array([0, 0, 0])
    fArB = np.array([0, 0, 0])
    #Roues contact latéral
    if deltaAvL <= deltamin:
        fAvL[dt.idy] = -dt.wheelKy * (deltaAvL-deltamin) + cy * -vDistFromRailToMod[dt.idForceRoueAvL]
        if fAvL[dt.idy] < 0:
            #fAvL[dt.idy] = 0
            fAvL[dt.idy] = -fAvL[dt.idy]
        fAvL[dt.idx] = -dt.coefFrotDyn*fAvL[dt.idy]
    if deltaArL <= deltamin:
        fArL[dt.idy] = -dt.wheelKy * (deltaArL-deltamin) + cy * -vDistFromRailToMod[dt.idForceRoueArL]
        if fArL[dt.idy] < 0:
            #fArL[dt.idy] = 0
            fArL[dt.idy] = -fArL[dt.idy]
        fArL[dt.idx] = -dt.coefFrotDyn*fArL[dt.idy]
    #Roues contact vertical haut
    if deltaAvH <= deltamin:
        fAvH[dt.idz] = -dt.wheelKz * (deltaAvH-deltamin) + cz * -vDistFromRailToMod[dt.idForceRoueAvH]
        if fAvH[dt.idz] < 0:
            #fAvH[dt.idz] = 0
            fAvH[dt.idz] = -fAvH[dt.idz]
        fAvH[dt.idx] = -dt.coefFrotDyn*fAvH[dt.idz]
    if deltaArH <= deltamin:
        fArH[dt.idz] = -dt.wheelKz * (deltaArH-deltamin) + cz * -vDistFromRailToMod[dt.idForceRoueArH]
        if fArH[dt.idz] < 0:
            #fArH[dt.idz] = 0
            fArH[dt.idz] = -fArH[dt.idz]
        fArH[dt.idx] = -dt.coefFrotDyn*fArH[dt.idz]
    #Roues contact vertical bas
    if deltaAvB <= deltamin:
        fAvB[dt.idz] = -dt.wheelKz * (deltaAvB-deltamin) + cz * -vDistFromRailToMod[dt.idForceRoueAvB]
        if fAvB[dt.idz] < 0:
            #fAvB[dt.idz] = 0
            fAvB[dt.idz] = -fAvB[dt.idz]
        fAvB[dt.idx] = -dt.coefFrotDyn*fAvB[dt.idz]
    if deltaArB <= deltamin:
        fArB[dt.idz] = -dt.wheelKz * (deltaArB-deltamin) + cz * -vDistFromRailToMod[dt.idForceRoueArB]
        if fArB[dt.idz] < 0:
            #fArB[dt.idz] = 0
            fArB[dt.idz] = -fArB[dt.idz]
        fArB[dt.idx] = -dt.coefFrotDyn*fArB[dt.idz]
    #fx = fAvL[dt.idx] + fArL[dt.idx] + fAvH[dt.idx] + fArH[dt.idx] + fAvB[dt.idx] + fArB[dt.idx]
    #fy = fAvL[dt.idy] + fArL[dt.idy]
    #fz = fAvH[dt.idz] + fArH[dt.idz] - fAvB[dt.idz] - fArB[dt.idz]
    fContact = fAvL + fArL + fAvH + fArH + fAvB + fArB
    #Invert y if left
    if isLeft:
        fContact = fContact * np.array([1, -1, 1])
        #fy = -fy
    return fContact, [fAvH, fAvB, fAvL, fArH, fArB, fArL]
    #return np.array([fx, fy, fz]) 
#_____________________________________________________________________________________________________________________________________________________________________
def force_amortisseur(lRes, vLRes, masseOnLev, isLeft=True):
    fx = np.single(0)
    #cY = dt.ksiY * 2 * np.sqrt(dt.kY * masseOnLev/4)
    cY = dt.cY
    fYRessort = -dt.kY*(lRes[dt.idy] - dt.l0Y)
    fYVisc = -cY * vLRes[dt.idy]
    fy = fYRessort + fYVisc

    #cZ = dt.ksiZ * 2 * np.sqrt(dt.kZ * masseOnLev/4)
    cZ = dt.cZ
    fZRessort = -dt.kZ*(lRes[dt.idz] - dt.l0Z)
    fZVisc = -cZ * vLRes[dt.idz]
    fz = fZRessort + fZVisc

    if isLeft == False:
        fy = -fy
    return np.array([fx, fy, fz])#, np.array([fYRessort, fYVisc])

#_____________________________________________________________________________________________________________________________________________________________________
def force_amortisseur_v2(lRes, vLRes, masseOnLev, isLeft=True):
    fx = np.single(0)
    cY = dt.ksiY * 2 * np.sqrt(dt.kY * masseOnLev/4)
    fYRessort = -dt.kY*(lRes[dt.idy] - dt.l0Y)
    fYVisc = -cY * vLRes[dt.idy]
    fy = fYRessort + fYVisc

    cZ = dt.ksiZ * 2 * np.sqrt(dt.kZ * masseOnLev/4)
    fZRessort = -dt.kZ*(lRes[dt.idz] - dt.l0Z)
    fZVisc = -cZ * vLRes[dt.idz]
    fz = fZRessort + fZVisc

    if isLeft == False:
        fy = -fy
    return np.array([fx, fy, fz])
#_____________________________________________________________________________________________________________________________________________________________________
def somme_moments(fReactionAvG, fReactionArG, fReactionArD, fReactionAvD, fProp, cartesianCoordinates):
    tGravity = gravitational_torque(cartesianCoordinates)
    tReactionAvG = moment(cartesianCoordinates[dt.idFixAvG], fReactionAvG)
    tReactionArG = moment(cartesianCoordinates[dt.idFixArG], fReactionArG)
    tReactionArD = moment(cartesianCoordinates[dt.idFixArD], fReactionArD)
    tReactionAvD = moment(cartesianCoordinates[dt.idFixAvD], fReactionAvD)
    tProp = moment(cartesianCoordinates[dt.idForceProp], fProp)
    tSum = tGravity + tReactionAvG + tReactionArG + tReactionArD + tReactionAvD + tProp
    dspT = [tGravity, tReactionAvG, tReactionArG, tReactionArD, tReactionAvD, tProp]
    return tSum#, dspT, tReactionAvG, tReactionArG, tReactionArD, tReactionAvD, tProp
#_____________________________________________________________________________________________________________________________________________________________________
def moment(positionFromCg, force):
    mX = positionFromCg[dt.idy]*force[dt.idz] - positionFromCg[dt.idz]*force[dt.idy]
    mY = positionFromCg[dt.idx]*force[dt.idz] - positionFromCg[dt.idz]*force[dt.idx]
    mZ = positionFromCg[dt.idx]*force[dt.idy] - positionFromCg[dt.idy]*force[dt.idx]
    return np.array([mX, mY, mZ])
#_____________________________________________________________________________________________________________________________________________________________________
def gravitational_torque(cartesianCoordinates):
    tX = 0
    tY = 0
    tZ = 0
    for i in range(len(dt.podGeom)):
        force = np.array([0, 0, dt.podGeom[i][dt.idKg]*dt.g])
        gravTorque = moment(cartesianCoordinates[i], force)
        tX += gravTorque[dt.idx]
        tY += gravTorque[dt.idy]
        tZ += gravTorque[dt.idz]
    return np.array([tX, tY, tZ])
#_____________________________________________________________________________________________________________________________________________________________________
def masses_actualisation():
    dt.masseTotale = np.single(0)
    for elem in dt.podGeom:
        dt.masseTotale += elem[dt.idKg]
    dt.masseOnMod = dt.masseTotale - 4*dt.masseModule
    dt.masseOnLev = dt.masseOnMod/4
    return dt.masseTotale, dt.masseOnMod, dt.masseOnLev
#_____________________________________________________________________________________________________________________________________________________________________
def all_forces(t, xCg, vXCg, angles, distToAvG, distToArG, distToArD, distToAvD, vDistToAvG, vDistToArG, vDistToArD, vDistToAvD, lrAvG, lrArG, lrArD, lrAvD, vLrAvG, vLrArG, vLrArD, vLrAvD):
    matRot = geom.matrice_rotation(angles)
    #Aero, propulsion, magnétique, contact au rail, freinage, amortisseur, gravité
    fAero = np.array([0, 0, 0])
    fProp = force_propulsion(t)

    #SECTION - Masses
    masses_actualisation()
    #!SECTION

    fGraviteOnMod = np.array([0, 0, dt.masseOnMod*dt.g])
    fGraviteModAvG = np.array([0, 0, dt.podGeom[dt.idCgMobileModuleAvG][dt.idKg]*dt.g])
    fGraviteModArG = np.array([0, 0, dt.podGeom[dt.idCgMobileModuleArG][dt.idKg]*dt.g])
    fGraviteModArD = np.array([0, 0, dt.podGeom[dt.idCgMobileModuleArD][dt.idKg]*dt.g])
    fGraviteModAvD = np.array([0, 0, dt.podGeom[dt.idCgMobileModuleAvD][dt.idKg]*dt.g])

    fMagAvG = force_EM_module_rail_L(distToAvG[dt.idForceLevY], distToAvG[dt.idForceLevZ], vXCg, vDistToAvG[dt.idForceLevZ], xCg, True)
    fMagArG = force_EM_module_rail_L(distToArG[dt.idForceLevY], distToArG[dt.idForceLevZ], vXCg, vDistToArG[dt.idForceLevZ], xCg, True)
    fMagArD = force_EM_module_rail_L(distToArD[dt.idForceLevY], distToArD[dt.idForceLevZ], vXCg, vDistToArD[dt.idForceLevZ], xCg, False)
    fMagAvD = force_EM_module_rail_L(distToAvD[dt.idForceLevY], distToAvD[dt.idForceLevZ], vXCg, vDistToAvD[dt.idForceLevZ], xCg, False)
    
    fContactAvG, fWheelsAvG = force_wheel_reaction(distToAvG, vDistToAvG, dt.masseOnMod, True)
    fContactArG, fWheelsArG = force_wheel_reaction(distToArG, vDistToArG, dt.masseOnMod, True)
    fContactArD, fWheelsArD = force_wheel_reaction(distToArD, vDistToArD, dt.masseOnMod, False)
    fContactAvD, fWheelsAvD = force_wheel_reaction(distToAvD, vDistToAvD, dt.masseOnMod, False)

    fResistX = fContactAvG[dt.idx] + fContactArG[dt.idx] + fContactArD[dt.idx] + fContactAvD[dt.idx] + fMagAvG[dt.idx] + fMagArG[dt.idx] + fMagArD[dt.idx] + fMagAvD[dt.idx]
    fFreinAvG = force_freinage(t, xCg, vXCg, fResistX, dt.masseTotale)
    fFreinArG = fFreinAvG
    fFreinArD = fFreinAvG
    fFreinAvD = fFreinAvG

    fAmortoAvG = force_amortisseur(lrAvG, vLrAvG, dt.masseOnLev, True)
    fAmortoArG = force_amortisseur(lrArG, vLrArG, dt.masseOnLev, True)
    fAmortoArD = force_amortisseur(lrArD, vLrArD, dt.masseOnLev, False)
    fAmortoAvD = force_amortisseur(lrAvD, vLrAvD, dt.masseOnLev, False)
    
    #SECTION - passage des forces dans le repère monde
    fAero = rotation_force(fAero, matRot)
    fProp = rotation_force(fProp, matRot)
    #fGrav --> pas de rotation
    #fMag --> pas de rotation (normales au rail)
    #fContact --> pas de rotation (normales au rail)
    #fFrein --> idem
    fAmortoAvG = rotation_force(fAmortoAvG, matRot)
    fAmortoArG = rotation_force(fAmortoArG, matRot)
    fAmortoArD = rotation_force(fAmortoArD, matRot)
    fAmortoAvD = rotation_force(fAmortoAvD, matRot)
    #!SECTION

    fReactionAvGOnPod = fAmortoAvG*np.array([1,-1,1]) + fFreinAvG*np.array([1,0,0]) + fMagAvG*np.array([1,0,0])
    fReactionArGOnPod = fAmortoArG*np.array([1,-1,1]) + fFreinArG*np.array([1,0,0]) + fMagArG*np.array([1,0,0])
    fReactionArDOnPod = fAmortoArD*np.array([1,-1,1]) + fFreinArD*np.array([1,0,0]) + fMagArD*np.array([1,0,0])
    fReactionAvDOnPod = fAmortoAvD*np.array([1,-1,1]) + fFreinAvD*np.array([1,0,0]) + fMagAvD*np.array([1,0,0])

    fGravs = [fGraviteModAvG, fGraviteModArG, fGraviteModArD, fGraviteModAvD]
    fMags = [fMagAvG, fMagArG, fMagArD, fMagAvD]
    fConts = [fContactAvG, fContactArG, fContactArD, fContactAvD]
    fWheels = [fWheelsAvG, fWheelsArG, fWheelsArD, fWheelsAvD]
    fBrakes = [fFreinAvG, fFreinArG, fFreinArD, fFreinAvD]
    fAmorts = [fAmortoAvG, fAmortoArG, fAmortoArD, fAmortoAvD]
    fReacts = [fReactionAvGOnPod, fReactionArGOnPod, fReactionArDOnPod, fReactionAvDOnPod]
    return fAero, fProp, fGraviteOnMod, fGravs, fMags, fConts, fWheels, fBrakes, fAmorts, fReacts

#_____________________________________________________________________________________________________________________________________________________________________
def somme_forces(fProp, fGraviteOnMod, fGravs, fAmorts, fAero, fBrakes, fConts, fMags, fReacts):
    #Pod
    sCgF = fGraviteOnMod + fAero + fProp + fReacts[0] + fReacts[1] + fReacts[2] + fReacts[3]
    #Modules
    sModFAvG = fGravs[0] + fAmorts[0]*np.array([1,1,-1]) + fBrakes[0] + fConts[0] + fMags[0]
    sModFArG = fGravs[1] + fAmorts[1]*np.array([1,1,-1]) + fBrakes[1] + fConts[1] + fMags[1]
    sModFArD = fGravs[2] + fAmorts[2]*np.array([1,1,-1]) + fBrakes[2] + fConts[2] + fMags[2]
    sModFAvD = fGravs[3] + fAmorts[3]*np.array([1,1,-1]) + fBrakes[3] + fConts[3] + fMags[3]
    return sCgF, sModFAvG, sModFArG, sModFArD, sModFAvD

#_____________________________________________________________________________________________________________________________________________________________________
def rotation_force(force, matRot):
    Axyz = np.array([[force[dt.idx]],
                     [force[dt.idy]],
                     [force[dt.idz]]])
    [xPrim, yPrim, zPrim] = np.dot(matRot, Axyz)
    return [xPrim[0], yPrim[0], zPrim[0]]
#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    dt.yFactor = np.single(5/100)    #5, 10, 25%
    #entreferY = dt.idealYairGag
    #entreferZ = np.single(0.005)
    entreferY = dt.idealYairGag
    entreferZ = np.single(0.008)
    xSpeed = np.single(28)
    zSpeed = np.single(0)
    xCg = np.single(10)
    #dt.magnetDim = "40mm_230828"

    print("Force mag:", force_EM_module_rail_L(entreferY, entreferZ, xSpeed, zSpeed, xCg, False))