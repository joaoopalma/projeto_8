import time
import sounddevice as sd
import soundfile as sf

sd.default.samplerate = 44100  # taxa de amostragem
sd.default.channels = 1  # número de canais
duration = 5  # tempo em segundos para captar o sinal acústico
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
sd.wait()  # Espera a gravação terminar

# Salva o arquivo .wav
filename = 'output.wav'
sf.write(filename, audio, sd.default.samplerate)
print(f"Áudio salvo em {filename}.")
