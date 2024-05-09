from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import time

signal = signalMeu()

filename = 'output.wav'

# Carregar o arquivo de áudio
data, samplerate = sf.read(filename)

sd.default.samplerate = 44100
sd.default.channels = 1 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
#Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.
duration = 4 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic   
#calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
numAmostras = duration*sd.default.samplerate

print("Gravação iniciada")
audio = sd.rec(int(numAmostras), 44100, channels=1)
sd.wait()

print("Gravação finalizada")

U = []
for l in audio:
    # print("l")
    U.append(l[0])

print("teste1")

a = 6.379e-05
b = 6.331e-05
c = 1
d = -1.977
e = 0.9776

Y = [U[0],U[1]]

for i in range(2,len(U)):
    # print("i")
    equacao = -d*Y[i-1]-e*Y[i-2]+a*U[i-1]+b*U[i-2]
    Y.append(equacao)

print("teste2")
# # print(len(U))
# print(len(Y))
xu,yu = signal.calcFFT(U, 44100)
xy,yy = signal.calcFFT(Y, 44100)

print(len(yu))
print(len(yy))

# plt.plot(xu, yu)

signal.plotFFT(U, 44100, "Sinal Original")
signal.plotFFT(Y, 44100, "Sinal Filtrado")
plt.show()

print("tocando audio original")
sd.play(U, 44100)
# aguarda fim do audio
sd.wait()

print("tocando audio filtrado")

sd.play(Y, 44100)
sd.wait()

