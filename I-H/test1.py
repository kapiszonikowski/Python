import numpy as np
import matplotlib.pyplot as plt
import csv

# Wczytanie danych z CSV
freq = []
L = []

with open('xxx_freq_ind.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        freq.append(float(row['freq_Hz']))
        L.append(complex(row['L_nH']))  # Konwersja tekstu na liczbę zespoloną

freq = np.array(freq)
L = np.array(L)

# Wykres
plt.figure()
plt.plot(freq, np.abs(L), marker='o', color='green')
plt.xscale('log')
plt.xlabel("Frequency [Hz]")
plt.ylabel("Inductance |L| [nH]")
plt.title("Inductance magnitude vs Frequency")
plt.grid(True, which='both', ls='--')
plt.tight_layout()
plt.savefig("xxx_freq_ind.png", dpi=300)
plt.show()
