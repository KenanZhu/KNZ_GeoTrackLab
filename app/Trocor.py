##Tro correct-Hopfield
import math
def Hop_tro_cor(H, ma):
    global e
    P0 = 1013.25
    e0 = 11.69
    T0 = 288.15
    p = P0 * pow((1.0 - 0.0068 / T0 / H) , 5)
    T = 288.15 - 0.0068 * H
    if H > 11000:
        e = 0
    if H <= 11000:
        e = e0 * pow( (1.0 - 0.0068 * H / T0) , 4)
    deltaSd = 1.552e-5 * p * (40136 + 148.72 * (T - 273.16) - H) / T
    deltaSw = 1.552e-5 * 4810 * e * (11000 - H) / pow(T , 2)
    #Dry
    dtropd = deltaSd / math.sqrt( math.sin( math.radians( math.degrees( pow(math.radians(ma) , 2) ) + 6.25) ) )
    #Wet
    dtropw = deltaSw / math.sqrt( math.sin( math.radians( math.degrees( pow(math.radians(ma) , 2) ) + 6.25) ) )
    dtrop = dtropw + dtropd
    return dtrop

#Tro corrct-Saastamoinen
def Sas_tro_cor(B, H, ma):
    global e
    P0 = 1013.25 * pow( (1 - 2.2557 * 10e-5 * H), 5.2568)
    e0 = 11.69
    T0 = 15 - 6.5 * 10e-3 * H + 273.15
    deltaSd = 2.2768e-3 * P0 / (1 - 2.66e-3 * math.cos(2 * B) - 2.8e-4 * H * 1e3)
    deltaSw = 2.2768e-3 * (1255 / T0 + 0.05) * e0
    # Dry
    dtropd = deltaSd / math.sqrt( math.sin( math.radians( math.degrees( pow(math.radians(ma), 2) ) + 6.25) ) )
    # Wet
    dtropw = deltaSw / math.sqrt( math.sin( math.radians( math.degrees( pow(math.radians(ma), 2) ) + 6.25) ) )
    dtrop = dtropw + dtropd
    return dtrop