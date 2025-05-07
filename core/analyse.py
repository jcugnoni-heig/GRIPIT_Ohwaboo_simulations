import numpy as np
import scipy
from scipy.signal import find_peaks
import scenarios.datas as data
import matplotlib.pyplot as plt
import pandas as pd
#_____________________________________________________________________________________________________________________________________________________________________
def analyse(df):
    #dfDatas = df.values
    for i in range(len(df["t"])):
        continue
    dMax = max(df.xCg)-data.podLength/2
    tMax = max(df.t)
    vMax = max(df.vXCg)
    tVol = 0
    tDec = 0
    vDec = 0

    airgag = df.entreferAvGz
    pd.concat([airgag, df.entreferArGz])
    pd.concat([airgag, df.entreferArDz])
    pd.concat([airgag, df.entreferAvDz])
    AGzMoy = np.mean(airgag)
    AGzMin = min(airgag)
    AGzMax = max(airgag)
    tAGzMax = 0
    ampAGz = 0
    fAGz = 0
    tDecY = 0
    vDecY = 0
    AGyMoy = 0
    AGyMin = 0
    AGyMax = 0
    tAGyMax = 0
    ampAGy = 0
    fAGy = 0
    tFrein = 0
    vFrein = 0
    fBreak = df.fxFreinAvG
    pd.concat([airgag, df.fxFreinArG])
    pd.concat([airgag, df.fxFreinArD])
    pd.concat([airgag, df.fxFreinAvD])
    fBreakMax = min(fBreak)
    if data.tBraking > 0:
        dtBraking = max(df.t)-data.tBraking
    else:
        dtBraking = np.single(0)

    print("\n--------------------- Statistiques ---------------------")
    print("Masse totale : %d kg"%(data.masseTotale))
    print("Masse module : %d kg"%(data.masseModule))
    print("---------------------")
    print("Distance totale : %.1fm / %.1fm"%(dMax, data.posXCgStop-data.podLength/2))
    print("Durée totale : %.3f s"%(tMax))
    print("Vitesse max  : %.3f m/s"%(vMax))
    print("Durée de vol : %.3f s"%(tVol))
    print("---------------------")
    print("Durée décollage   : %.3f s"%(tDec))
    print("Vitesse décollage : %.1f m/s"%(vDec))
    print("Durée contact guidage      : %.3f s"%(tDecY))
    print("Vitesse guidage magnétique : %.1f m/s"%(vDecY))
    print("Durée freinage         : %.3f s"%(tFrein))
    print("Vitesse début freinage : %.1f m/s"%(vFrein))
    print("---------------------")
    print("Début freinage   : %.1f s"%(data.tBraking))
    print("Durée de freinage   : %.1f s"%(dtBraking))
    print("Force max de freinage   : %d N"%(fBreakMax))
    print("---------------------")
    print("Or accélération et freinage")
    print("Entrefer lévitation moyen : %.1f mm"%(AGzMoy))
    print("Entrefer lévitation min   : %.0f mm"%(AGzMin))
    print("Entrefer lévitation max   : %.0f mm"%(AGzMax))
    print("Durée pour atteindre l'entrefer de lévitation max : %.3f s"%(tAGzMax))
    print("Amplitude oscillation lev : %.1f mm"%(ampAGz))
    print("Fréquence oscillation lev : %.1f Hz"%(fAGz))
    print("---------------------")
    print("Or accélération et freinage")
    print("Entrefer guidage moyen : %.1f mm"%(AGyMoy))
    print("Entrefer guidage min   : %.0f mm"%(AGyMin))
    print("Entrefer guidage max   : %.0f mm"%(AGyMax))
    print("Durée pour atteidre entrefer guidage max : %.3f s"%(tAGyMax))
    print("Amplitude oscillation lev : %.1f mm"%(ampAGy))
    print("Fréquence oscillation lev : %.1f Hz"%(fAGy))
    print("---------------------")
#_____________________________________________________________________________________________________________________________________________________________________
def lissage_signal(t, y):
    return scipy.interpolate.interp1d(t, y)
#_____________________________________________________________________________________________________________________________________________________________________
def analyse_fft(df):
    # Découpe du signal : Vol 
    peaks = maximums(df.t, df.entreferAvGz, "Do not print it")
    #print("peaks", peaks)
    limMin = peaks[0] #np.single(1)    #1.43)
    limMax = peaks[-1] #np.single(3)    #1.85)
    #print("limites", limMin, limMax)
    t = []
    y = []
    for i in range(len(df.t)):
        if df.t[i] >= limMin and df.t[i]<=limMax:
            t.append(df.t[i])
            #y.append(df.zCg[i])
            y.append(df.entreferAvGz[i])
    t = np.array(t)
    y = np.array(y)
    #print("t:",t)
    #print("y:",y)
    print("yMean (hauteur de vol) : %.1fmm"%(np.mean(y)))
    print("Amplitude oscillation : %.1fmm"%(max(y)-min(y)))
    print("---------------------")
    print("---------------------\n\n")
    # 
    tf, xf, abs = filtered_signal(df.t, df.entreferAvGz, 1E-3)
    peaks = maximums(df.t, df.entreferAvGz, "Peaks")
    peaksFilt = maximums(tf, xf, "Peaks on filtered signal")
    plt.show()
    tf, xf, abs = filtered_signal(t, y, 1E-3)
    peaks = maximums(t, y, "Peaks")
    peaksFilt = maximums(tf, xf, "Peaks on filtered signal")
    plt.show()

#_____________________________________________________________________________________________________________________________________________________________________
def interp_sig(t, y):
    tMax = t[len(t)-1]
    tMin = t[0]
    Te = data.stepPerSecond*1E2  # Période d'échantillonnage en seconde
    N = round((tMax-tMin) * data.stepPerSecond)#int(Duree/Te) + 1  # Nombre de points du signal échantillonné

    te = np.linspace(tMin, tMax, N)  # Temps des échantillons
    fx = lissage_signal(t, y)
    x_e = fx(te)  # Calcul de l'échantillonnage
    return te, x_e, Te, N
#_____________________________________________________________________________________________________________________________________________________________________
def filtered_signal(te, xe, cut_off):
    #https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html
    t, x, Te, N = interp_sig(te, xe)
    
    # Analyse
    plt.figure(num='Original signal', figsize = (8, 6))
    plt.plot(te, xe, 'r')
    plt.ylabel('Amplitude')
    plt.title('Original signal')
    plt.grid()
    # FFT the signal
    sig_fft = np.fft.fft(x)
    # copy the FFT results
    sig_fft_filtered = sig_fft.copy()

    # obtain the frequencies using scipy function
    freq = np.fft.fftfreq(len(x), d=1./2000)

    # define the cut-off frequency
    #cut_off = 6

    # high-pass filter by assign zeros to the 
    # FFT amplitudes where the absolute 
    # frequencies smaller than the cut-off 
    sig_fft_filtered[np.abs(freq) < cut_off] = 0

    # get the filtered signal in time domain
    filtered = np.fft.ifft(sig_fft_filtered)

    # plot the filtered signal
    plt.figure(num='Amplitude', figsize = (12, 6))
    plt.plot(te, xe, 'r', label='Original')
    plt.plot(t, filtered, label='Filtered')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.legend()
    #plt.show()

    # plot the FFT amplitude before and after
    plt.figure(num='FFT Amplitude', figsize = (12, 6))

    plt.subplot(121)
    plt.stem(freq, np.abs(sig_fft), 'b', \
            markerfmt=" ", basefmt="-b")
    plt.title('Before filtering')
    plt.xlim(0, 30)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Amplitude')
    plt.grid()

    plt.subplot(122)
    plt.stem(freq, np.abs(sig_fft_filtered), 'b', \
            markerfmt=" ", basefmt="-b")
    plt.title('After filtering')
    plt.xlim(0, 30)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Amplitude')
    plt.tight_layout()
    plt.grid()

    #plt.show()
    return t, filtered, np.abs(sig_fft_filtered)

#_____________________________________________________________________________________________________________________________________________________________________
def maximums(t, x, title):
    te = np.single(0)
    lstt = np.single(0)
    #print("len :",len(t))
    for i in range(len(t)):
        if i < (len(t)-1):
            te += t[i+1]-t[i]
        #lstt = t[i]
    te = te/(len(t)-1)
    #print("te : ", te)
    peaks, properties = find_peaks(x, prominence=1, width=10)
    peaksTe = peaks*te
    #print("Peaks", peaks)
    #print("prominences", properties["prominences"], "\twidths", properties["widths"])

    plt.figure(num=title)
    plt.plot(t, x)
    #plt.plot(peaksTe, x[peaks], "x")
    plt.plot(t[peaks], x[peaks], "x")

    #print("PeaksTe : ", type(peaksTe), peaksTe)
    #print("x[peaks] : ", type(x[peaks]), x[peaks])
    #print("peaks : ", type(peaks), peaks)
    #print("x : ", type(x), x)
    try:
        return np.array(peaksTe, x[peaks])
    except:
        return np.array(peaksTe, pd.Series(x)[peaks])
#_____________________________________________________________________________________________________________________________________________________________________
def x(t):
    # Calcul du signal x(t) = sin(2*pi*t)
    return np.sin(2*np.pi*t)
#_____________________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    pass