import femm as f    
import matplotlib.pyplot as plt
import csv
import numpy as np


def generate_linear_points(p1, p2, N):
    """
    p1, p2: krotki (x, y) – końce odcinka
    N: int – liczba punktów do wygenerowania pomiędzy p1 i p2 (wraz z p1,p2)
    """
    x1, y1 = p1
    x2, y2 = p2
    # krok w kierunku x i y
    dx = (x2 - x1) / (N - 1)
    dy = (y2 - y1) / (N - 1)

    points = []
    for i in range(0, N):
        xi = x1 + dx * i
        yi = y1 + dy * i
        points.append((xi, yi))

    return points


def geom(r_tube, r_coil, R_coil, H_coil, N, R_el, H_el, H0, R_BC, I, freq):
    # Definitions
    f.openfemm()
    f.newdocument(0) # 0 for magnetostatic problem
    f.mi_probdef(freq,"millimeters","axi", 1e-8) # frequency,units,type,precision

    # Add materials
    f.mi_getmaterial("Air")
    f.mi_getmaterial("Copper")
    f.mi_getmaterial("Aluminum, 1100")

    # Add coil properties
    f.mi_addcircprop("Curr", I, 1)

    f.mi_addnode(0,0)

    # Add coil Geometry, material & circuit
    windings_pos = generate_linear_points((r_coil,0),(R_coil,H_coil),N)
    for i in range(0,len(windings_pos)):
        p = windings_pos[i]
        r = p[0]
        h = p[1]
        f.mi_addnode(r,h)
        f.mi_addnode(r+r_tube,h)
        f.mi_addarc(r,h,r+r_tube,h,180,1)
        f.mi_addarc(r+r_tube,h,r,h,180,1)
        f.mi_selectnode(r,h)
        f.mi_selectnode(r+r_tube,h)
        f.mi_setnodeprop("Coil",3)
        f.mi_clearselected()

        f.mi_addblocklabel(r+r_tube/2,h) # label for winding
        f.mi_selectlabel(r+r_tube/2,h) # Associate properties to block labels
        f.mi_setblockprop("Copper",0,0,"Curr",0,3,1) # 100 turns
        f.mi_clearselected()
    
    # Add aluminum geom & material
    f.mi_addnode(0,H0-H_el/2)
    f.mi_addnode(0,H0+H_el/2)
    f.mi_addnode(R_el,H0+H_el/2)
    f.mi_addnode(R_el,H0-H_el/2)

    f.mi_selectnode(0,H0-H_el/2)
    f.mi_selectnode(0,H0+H_el/2)
    f.mi_selectnode(R_el,H0+H_el/2)
    f.mi_selectnode(R_el,H0-H_el/2)
    f.mi_setnodeprop("Al",1)
    f.mi_clearselected() 

    f.mi_drawline(0,H0-H_el/2,0,H0+H_el/2)
    f.mi_drawline(0,H0+H_el/2,R_el,H0+H_el/2)
    f.mi_drawline(R_el,H0+H_el/2,R_el,H0-H_el/2)
    f.mi_drawline(R_el,H0-H_el/2,0,H0-H_el/2)

    f.mi_selectsegment(0,H0)
    f.mi_selectsegment(R_el/2,H0+H_el/2)
    f.mi_selectsegment(R_el,H0)
    f.mi_selectsegment(R_el/2,H0-H_el/2)
    f.mi_setsegmentprop("Al",0,0,0,1)
    f.mi_clearselected() 

    f.mi_addblocklabel(R_el/2,H0)
    f.mi_selectlabel(R_el/2,H0)
    f.mi_setblockprop("Aluminum, 1100",0,0,"",0,1,1)
    f.mi_clearselected() 

    # Powietrze
    f.mi_addblocklabel(R_coil,0)
    f.mi_selectlabel(R_coil,0)
    f.mi_setblockprop("Air",0,0,"",0,0,1)
    f.mi_clearselected() 

    f.mi_makeABC(7,R_BC,0,H_coil/2,0)

    f.mi_saveas("IH.fem")

# Stałe geometryczne
r_tube = 6
r_coil = 10
R_coil = 30
H_coil = 60
N_windings = 8
R_el = 7.5     # mm
H_el = 20      # mm
H0 = 40        # mm – optymalna wysokość zawieszenia
R_BC = 140
freq = 1e5     # Hz

# Zakres natężeń prądu
I_values = np.linspace(100, 500, 10)  
F_em = []

# Obliczenia
for I in I_values:
    geom(r_tube, r_coil, R_coil, H_coil, N_windings, R_el, H_el, H0, R_BC, I, freq)

    f.mi_analyze()
    f.mi_loadsolution()

    f.mo_groupselectblock(1)
    F_em.append(f.mo_blockintegral(19))  # Siła elektromagnetyczna w N

# Zapis danych do pliku CSV
with open("I_influence_10mmx30mm_coil.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Current_A", "F_em_N"])
    for I, Fem in zip(I_values, F_em):
        writer.writerow([I, Fem])

# Wykres
plt.figure()
plt.plot(I_values, F_em, marker='o', color='green')
plt.xlabel("Current [A]")
plt.ylabel("Electromagnetic force [N]")
plt.title("Electromagnetic force vs. current")
plt.grid(True)
plt.tight_layout()
plt.savefig("F_vs_I_10mmx30mm_coil.png", dpi=300)
plt.show()
