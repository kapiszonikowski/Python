import femm as f    
import matplotlib.pyplot as plt
import csv

# Parameters
I = 1 # current
r = 5
R = 6
Hp = 50
Lp = -Hp

def geom(r,R,I):
    # Definitions
    f.openfemm()
    f.newdocument(0) # 0 for magnetostatic problem
    f.mi_probdef(0,"millimeters","axi", 1e-8) # frequency,units,type,precision

    # Add materials
    f.mi_getmaterial("Air")
    f.mi_getmaterial("1mm")

    # Add coil properties
    f.mi_addcircprop("Coil", I, 1) # 1 is for series circuit (coil)

    # Draw the geometry
    f.mi_drawline(r,Hp,R,Hp)
    f.mi_drawline(R,Hp,R,-Hp)
    f.mi_drawline(R,-Hp,r,-Hp)
    f.mi_drawline(r,-Hp,r,Hp)


    # Make it group
    f.mi_selectnode(r,Hp)
    f.mi_selectnode(r,Hp)
    f.mi_selectnode(R,-Hp)
    f.mi_selectnode(R,-Hp)
    f.mi_setnodeprop("",0)
    f.mi_clearselected()

    # Add block labels
    f.mi_addblocklabel((r+R)/2,(Hp+Lp)/2) # label for winding
    f.mi_selectlabel((r+R)/2,(Hp+Lp)/2) # Associate properties to block labels
    f.mi_setblockprop("1mm",0,0,"Coil",0,0,100) # 100 turns
    f.mi_clearselected()

    # Air
    f.mi_addblocklabel(25,60)  # label for air
    f.mi_selectlabel(25,60)
    f.mi_setblockprop("Air",0,0,"",0,1,0)
    f.mi_clearselected()

    # Create boundary conditions using default parameters
    f.mi_makeABC(7,100,0,0,0)

    f.mi_saveas("inductor.fem")

####################################################################################################################

geom(r,R,I)


L = []
Coil_radius = []

for i in range(0,10):

    geom(r+i,R+i,I)
    
    # Analyze and load solution
    f.mi_analyze()
    f.mi_loadsolution()

    # Inductance calculation
    Coil_props = f.mo_getcircuitproperties("Coil") # current, voltage, flux
    L.append(Coil_props[2]/I)
    print(L)
    Coil_radius.append((r+R)/2+i)
    print(Coil_radius)

Lu = [val*1e6 for val in L]
print("Inductance [uH]= ", Lu)
print("Coil raduses [mm] = ", Coil_radius)

with open("inductance_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Coil_radius_mm", "Inductance_uH"])
    for r_val, L_val in zip(Coil_radius, Lu):
        writer.writerow([r_val, L_val])

plt.plot(Coil_radius, Lu, marker='o')
plt.xlabel("Coil Radius [mm]")
plt.ylabel("Inductance [μH]")
plt.title("Inductance vs. Coil Radius")
plt.grid(True)
plt.savefig("inductance_plot.png", dpi=300)  # Zapis wykresu do pliku
plt.show()
