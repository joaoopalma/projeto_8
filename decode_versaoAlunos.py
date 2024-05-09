from suaBibSignal import *
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    # Declare um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()

    # Configurações de sounddevice
    sd.default.samplerate = 44100  # taxa de amostragem
    sd.default.channels = 1  # número de canais
    duration = 15  # tempo em segundos para captar o sinal acústico
    numAmostras = sd.default.samplerate * duration
    print(f"A captação começará em {duration} segundos...")
    i = 0
    start = 3
    while i < start:
        print(f"{start - i}...")
        time.sleep(1)
        i += 1

    print("Gravação iniciada.")
    audio = sd.rec(int(numAmostras), samplerate=sd.default.samplerate, channels=1)
    sd.wait()

    # Extrai a parte que interessa da gravação (dados)
    if audio.ndim > 1:
        audio = audio[:, 0]  # assumindo que áudio é estéreo, pegamos apenas um canal
    print("FIM da gravação.")

    # Criação do vetor tempo
    t = np.linspace(0, duration, num=numAmostras, endpoint=False)

    # Plota o áudio gravado
    plt.figure()
    plt.plot(t, audio)
    plt.title("Áudio Gravado")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Calcula e plota a FFT do áudio
    xf, yf = signal.calcFFT(audio, sd.default.samplerate)
    plt.figure()
    plt.plot(xf, yf)
    plt.title("Transformada de Fourier do Áudio")
    plt.xlabel("Frequência [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)

    # Encontrar picos na FFT
    indices = peakutils.indexes(yf, thres=0.4, min_dist=50)
    peak_freqs = xf[indices]
    peak_mags = yf[indices]

    # Exibir picos encontrados
    print("Picos encontrados em:", peak_freqs)

    # Encontrar frequências DTMF
    dtmf_freqs = {
        (679, 1209): '1', (679, 1336): '2', (679, 1477): '3',
        (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
        (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
        (941, 1209): '*', (941, 1336): '0', (941, 1477): '#'
    }

    # Identifica tecla DTMF
    found_keys = []
    for f1, f2 in dtmf_freqs.keys():
        if np.any(np.isclose(peak_freqs, f1, atol=10)) and np.any(np.isclose(peak_freqs, f2, atol=10)):
            found_keys.append(dtmf_freqs[(f1, f2)])

    if found_keys:
        print("Tecla(s) identificada(s):", found_keys)
    else:
        print("Nenhuma tecla DTMF identificada.")

    plt.show()

if __name__ == "__main__":
    main()
