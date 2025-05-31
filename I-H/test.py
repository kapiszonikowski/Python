import femm as f    
import matplotlib.pyplot as plt
import csv
import numpy as np
import time

def geom(r, R_BC, I, freq):
    # Definitions
    f.openfemm()
    f.newdocument(0) # 0 for magnetostatic problem
    f.mi_probdef(freq,'millimeters','planar',1E-8,0,30,1); # frequency,units,type,precision

    # Add materials
    f.mi_getmaterial("Air")
    f.mi_getmaterial("Copper")

    # Add coil properties
    f.mi_addcircprop("Curr", I, 1)
    
    f.mi_addnode(r,0)
    f.mi_addnode(-r,0)
    f.mi_addarc(r,0,-r,0,180,1)
    f.mi_addarc(-r,0,r,0,180,1)

    f.mi_addblocklabel(0,0) # label for winding
    f.mi_selectlabel(0,0) # Associate properties to block labels
    f.mi_setblockprop("Copper",0,0,"Curr",0,1,1) 
    f.mi_clearselected()

    # Powietrze
    f.mi_addblocklabel(2*r,0)
    f.mi_selectlabel(2*r,0)
    f.mi_setblockprop("Air",0,0,"",0,0,1)
    f.mi_clearselected() 

    f.mi_makeABC(7,R_BC,0,0,0)

    f.mi_saveas("skin.fem")


# Stałe geometryczne
r = 3
R_BC = 100
I = 1e3
freq = np.logspace(2,7,30)
L = []
B = []
print(freq)
geom(r, R_BC, I, 10e3)

# Obliczenia
for fr in freq:
    geom(r, R_BC, I, fr)

    f.mi_analyze()
    f.mi_loadsolution()
    
    X = f.mo_getcircuitproperties("Curr")
    L.append(X[2]/I*1e9)
    X1 = f.mo_getpointvalues(0,3)
    print(X1)
    B .append((X1[1]**2+X1[2]**2)**(1/2))
    

# Zapis danych do pliku CSV (freq, L, B)
with open("xxx_freq_ind_B.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["freq_Hz", "L_nH", "B_T"])  # przyjmuję jednostkę tesla
    for f_hz, L_nh, B_t in zip(freq, L, B):
        writer.writerow([f_hz, L_nh, B_t])

# Wykres indukcyjności L(f)
plt.figure()
plt.loglog(freq, L, marker='o')
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Indukcyjność [nH]")
plt.title("Indukcyjność vs. częstotliwość")
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig("xxx_freq_ind.png", dpi=300)
plt.show()

# Wykres pola B(f)
plt.figure()
plt.loglog(freq, B, marker='s')
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wartość pola B (T)")
plt.title("Pole magnetyczne vs. częstotliwość")
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig("xxx_freq_B.png", dpi=300)
plt.show()