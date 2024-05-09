from suaBibSignal import *
import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import math

def filtro(a,b,c,d,e,audio):
    # Verifica se o áudio é mono ou estéreo
    U = audio

    Y = [U[0], U[1]]

    for i in range(2, len(U)):
        equacao = -d*Y[i-1] - e*Y[i-2] + a*U[i-1] + b*U[i-2]
        Y.append(equacao)
    return U,Y

def normaliza(lista):
    listaFinal = []
    maximo = max(lista)
    minimo = min(lista)
    if abs(maximo) > abs(minimo):
        maxim = abs(maximo)
    else:
        maxim = abs(minimo)

    for i in range(len(lista)):
        listaFinal.append(lista[i]/maxim)
    return listaFinal

signal = signalMeu()

sd.default.samplerate = 44100  # taxa de amostragem
sd.default.channels = 1  # número de canais

filename = 'modulado.wav'

audio, samplerate = sf.read(filename)

xa,ya = signal.calcFFT(audio, samplerate)

plt.plot(xa,ya)
plt.show()

C = 1 # Amplitude
frequencia = 14000
phase = 0
demodulado = []
for t in range(len(audio)):
    portadora = C * math.sin(math.pi * 2 * frequencia * t/samplerate + phase)
    demodulado.append(audio[t] * portadora)

a = 0.003873
b = 0.003646
c = 1
d = -1.827
e = 0.8341

U,Y = filtro(a, b, c, d, e, demodulado)

signal.plotFFT(U, samplerate, "Sinal Original")
signal.plotFFT(Y, samplerate, "Sinal Filtrado")
plt.show()

U = normaliza(U)
Y = normaliza(Y)

print("tocando audio final")
sd.play(Y, samplerate)
sd.wait()