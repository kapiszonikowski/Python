# -*- coding: utf-8 -*-
import femm
import numpy as np
import matplotlib.pyplot as plt

femm.openfemm()
femm.opendocument("EF25-N87.fem");
femm.mi_saveas("temp.fem")

Min=0.5; Max = 3.5; Step = 0.2
Npoints = int( (Max-Min)/Step )
I = np.arange(Min, Max, Step, dtype=np.float)
W = np.arange(Min, Max, Step, dtype=np.float)
L = np.arange(Min, Max, Step, dtype=np.float)

print("FEMM Results: ")
for k in range (0, Npoints):
    femm.mi_modifycircprop("Coil", 1, I[k])
    femm.mi_analyze()
    femm.mi_loadsolution()  
    femm.mo_selectblock(12.4,0)     # air gap
    femm.mo_selectblock(7.4,2.3)    # left winding
    femm.mo_selectblock(17.4,2.3)   # right winding
    femm.mo_selectblock(15.3,10.9)  # core
    W[k]=femm.mo_blockintegral(2)   # field energy
    L[k]=2*W[k]/I[k]**2             # inductance
    print(I[k], L[k]) 
femm.closefemm()   
    
# Plotting
# Inductance versus current
plt.figure(1)
plt.plot(I, L*1e3, "rs--")
plt.grid(True)
plt.ylabel("Inductance (mH)")
plt.xlabel("Current (A)")
plt.savefig("L_vs_current.png", dpi=300)




