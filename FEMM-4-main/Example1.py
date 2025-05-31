import femm as f    

# Definitions
f.openfemm()
f.newdocument(0) # 0 for magnetostatic problem
f.mi_probdef(0,"millimeters","axi", 1e-8) # frequency,units,type,precision

# Parameters
I = 1 # current

# Draw the geometry
f.mi_drawline(5,50,6,50)
f.mi_drawline(6,50,6,-50)
f.mi_drawline(6,-50,5,-50)
f.mi_drawline(5,-50,5,50)

# Add block labels
f.mi_addblocklabel(5.5,46) # label for winding
f.mi_addblocklabel(25,60)  # label for air

# Add materials
f.mi_getmaterial("Air")
f.mi_getmaterial("1mm")

# Add coil properties
f.mi_addcircprop("Coil", I, 1) # 1 is for series circuit (coil)

# Associate properties to  block labels
# Winding
f.mi_selectlabel(5.5,46)
f.mi_setblockprop("1mm",0,0,"Coil",0,0,100) # 100 turns
f.mi_clearselected()

# Air
f.mi_selectlabel(25,60)
f.mi_setblockprop("Air",0,0,"",0,0,1)
f.mi_clearselected()

# Create boundary conditions using default parameters
f.mi_makeABC()

# zoom and save
f.mi_zoomnatural()

f.mi_saveas("inductor.fem")



####################################################################################################################

# Analyze and load solution
f.mi_analyze()
f.mi_loadsolution()

# Hide flux lines (contour) and show density plot of B
f.mo_hidecontourplot()
f.mo_showdensityplot(1, 0, 1.25e-3, 0, "bmag")

# Inductance calculation
Coil_props = f.mo_getcircuitproperties("Coil") # current, voltage, flux
L = Coil_props[2]
print("Inductance (uH)= ", L*1e6)
print(Coil_props)

    





