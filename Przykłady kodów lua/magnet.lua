-- Creates a new preprocessor document (magnetics problem)
newdocument(0)
-- Main problem parameters
-- 0 frequency
-- mm units
-- planar problem
-- solver precision
-- depth, set to 1 m so to have results per m length
mi_probdef(0, "millimeters", "planar", 1e-8, 1000)

-- A few variables
w_coil = 99
h_coil = 22
x_bck = 800
y_bck = 400
workfolder = "C:\\temp\\"
filename = "dipole"

-- Current and number of turns per coil block
current = 450
turns = 18

-- Mesh parameters
mshf = 1
msh_yoke = 10*mshf
msh_coil = 8*mshf
msh_gap = 1*mshf
msh_bck = 25*mshf

-- Material properties, from the available library
mi_getmaterial("Air")
mi_getmaterial("Pure Iron")
mi_getmaterial("Copper")

-- Boundary conditions
mi_addboundprop("B parallel", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
mi_addboundprop("B perpendicular", 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0)

-- A circuit, multiple ones are possible
mi_addcircprop("Coil", current, 1)

-- Yoke (array of points, for convenience)
x_yoke, y_yoke = {}, {}
x_yoke[1], y_yoke[1] = 0, 25
x_yoke[2], y_yoke[2] = 71, 25
x_yoke[3], y_yoke[3] = 71, 24.2
x_yoke[4], y_yoke[4] = 90, 24.2
x_yoke[5], y_yoke[5] = 105, 60
x_yoke[6], y_yoke[6] = 105, 295
x_yoke[7], y_yoke[7] = 55, 345
x_yoke[8], y_yoke[8] = -409, 345
x_yoke[9], y_yoke[9] = -459, 295
x_yoke[10], y_yoke[10] = -459, 0
x_yoke[11], y_yoke[11] = -249, 0
x_yoke[12], y_yoke[12] = -249, 127
x_yoke[13], y_yoke[13] = -105, 127
x_yoke[14], y_yoke[14] = -105, 60
x_yoke[15], y_yoke[15] = -90, 24.2
x_yoke[16], y_yoke[16] = -71, 24.2
x_yoke[17], y_yoke[17] = -71, 25
np_yoke = getn(x_yoke)

for ip_yoke = 1, np_yoke do
    mi_addnode(x_yoke[ip_yoke], y_yoke[ip_yoke])
end

for ip_yoke = 1, np_yoke-1 do
    mi_addsegment(x_yoke[ip_yoke], y_yoke[ip_yoke], x_yoke[ip_yoke+1], y_yoke[ip_yoke+1])
end

mi_addsegment(x_yoke[np_yoke], y_yoke[np_yoke], x_yoke[1], y_yoke[1])

--
mi_addblocklabel(0, 150)
mi_selectlabel(0, 150)
mi_setblockprop("Pure Iron", 0, msh_yoke)
mi_clearselected()

-- Coil
mi_addnode(127, 100)
mi_addnode(127+w_coil, 100)
mi_addnode(127+w_coil, 100+h_coil)
mi_addnode(127, 100+h_coil)
mi_addsegment(127, 100, 127+w_coil, 100)
mi_addsegment(127+w_coil, 100, 127+w_coil, 100+h_coil)
mi_addsegment(127+w_coil, 100+h_coil, 127, 100+h_coil)
mi_addsegment(127, 100+h_coil, 127, 100)

--
mi_addblocklabel(127+w_coil/2, 100+h_coil/2)
mi_selectlabel(127+w_coil/2, 100+h_coil/2)
mi_setblockprop("Copper", 0, msh_coil, "Coil", 0, 0, turns)

-- copies
mi_selectrectangle(127, 100, 127+w_coil, 100+h_coil, 4)
mi_copytranslate(0, -(h_coil+5), 2, 4)
mi_selectrectangle(127, 100-2*(h_coil+5), 127+w_coil, 100+h_coil, 4)
mi_copytranslate(-336, 0, 1, 4)

-- change sign of current on one side
mi_selectrectangle(127, 100-2*(h_coil+5), 127+w_coil, 100+h_coil, 2)
mi_setblockprop("Copper", 0, msh_coil, "Coil", 0, 0, -turns)
mi_clearselected()

-- Air region (background and gap)
mi_addnode(0, 0)
mi_addnode(130, 0)
mi_addnode(-130, 0)
mi_addsegment(130, 0, x_yoke[4], y_yoke[4])
mi_addsegment(-130, 0, x_yoke[15], y_yoke[15])
--

mi_addnode(-500, 0)
mi_addnode(x_bck, 0)
mi_addnode(x_bck, y_bck)
mi_addnode(-500, y_bck)
mi_addsegment(-500, 0, x_bck, 0)
mi_addsegment(x_bck, 0, x_bck, y_bck)
mi_addsegment(x_bck, y_bck, -500, y_bck)
mi_addsegment(-500, y_bck, -500, 0)
--

mi_addblocklabel(0, 10)
mi_selectlabel(0, 10)
mi_setblockprop("Air", 0, msh_gap)
mi_clearselected()
--

mi_addblocklabel(150, 150)
mi_selectlabel(150, 150)
mi_setblockprop("Air", 0, msh_bck)
mi_clearselected()
--

mi_addblocklabel(-150, 20)
mi_selectlabel(-150, 20)
mi_setblockprop("Air", 0, 6*msh_gap)
mi_clearselected()

-- hide lines in post-processor
mi_selectsegment((130+x_yoke[4])/2, y_yoke[4]/2)
mi_selectsegment((-130+x_yoke[15])/2, y_yoke[15]/2)
mi_setsegmentprop("", 0, 1, 1)
mi_clearselected()

-- Boundary conditions on segments
mi_selectrectangle(-500, 0, x_bck, 0, 1)
mi_setsegmentprop("B perpendicular")
mi_clearselected()
mi_selectsegment(x_bck, y_bck/2)
mi_selectsegment((x_bck-500)/2, y_bck)
mi_selectsegment(-500, y_bck/2)
mi_setsegmentprop("B parallel")
mi_clearselected()

-- Zoom out
mi_zoomnatural()

-- Save
mi_saveas(workfolder .. filename .. ".fem")

-- Mesh
mi_createmesh()



-- Solve
mi_analyze()

-- Post-processing
mi_loadsolution()

-- Post-processing
-- The flux lines plot is loaded by default
mi_loadsolution()

-- mo_savebitmap(workfolder .. filename .. "_flux.bmp")
mo_savemetafile(workfolder .. filename .. "_flux.emf")

-- Field density plot
B_min = 0
B_max = 1.5
mo_showdensityplot(1,B_min,B_max,0,"bmag")

-- Field at 0,0
A, B1, B2 = mo_getpointvalues(0, 0)
print("B @ x=0; y=0")
print("Bx = ", B1, " T")
print("By = ", B2, " T")

-- Plot field in the aperture
w_GFR = 120
mo_addcontour(-w_GFR/2, 0)
mo_addcontour(w_GFR/2, 0)

-- mo_makeplot(2, 200) -- plot in FEMM
mo_makeplot(2, 50, workfolder .. filename .. "_By_midplane.emf") -- save image
mo_makeplot(2, 50, workfolder .. filename .. "_By_midplane.txt", 0) -- print it to a file
mo_clearcontour()

-- Lorentz forces in the coil
mo_selectblock(127+w_coil/2, 100+h_coil/2)
mo_selectblock(127+w_coil/2, 100+h_coil/2-(h_coil+5))
mo_selectblock(127+w_coil/2, 100+h_coil/2-2*(h_coil+5))
Fx = mo_blockintegral(11)
print("Fx = ", Fx, " N")
Fy = mo_blockintegral(12)
print("Fy = ", Fy, " N")
mo_clearblock()

-- Energy
mo_groupselectblock()
U = mo_blockintegral(2)
print("Energy = ", U, " J")
mo_clearblock()

-- Inductance
-- --> from concatenated flux
curr, volts, flux_re = mo_getcircuitproperties("Coil")
print("Fy = ", flux_re, " N")
L_fl = 2*flux_re/curr
print("Inductance (from concatenated flux) = ", L_fl*1000, " mH")

-- alternative: select all coil blocks then get the flux linkage as mo_blockintegral(0)
-- --> from energy
mo_groupselectblock()
U = mo_blockintegral(2)
mo_clearblock()
L_en = 2*2*U/curr^2
print("Inductance (from energy) = ", L_en*1000, " mH")

--
-- LUA script to compute multipoles in FEMM
--
-- Few standard cases are considered:
-- * dipole 180 deg (ex. C shape)
-- * dipole 90 deg (ex. H shape)
-- * quadrupole 45 deg (ex. standard symmetric quadrupole)
--
-- In all cases, the center is 0, 0 and the skew coefficients are 0
--
-- The script computes two sets of multipoles:
-- * one from A (the vector potential)
-- * another one from a radial projection of B
-- They should be the same, so the difference in a way shows
-- how much to trust these numbers; the ones from A should be better,
-- as this is the finite element solution without further manipulations
-- (derivation, radial projection) while B is rougher (linear elements,
-- so B is constant over each triangle), but then it's smoothed out in the postprocessor
--

case_index = 1
-- 1 ===> dipole 180 deg (ex. C shape)
-- 2 ===> dipole 90 deg (ex. H shape)
-- 3 ===> quadrupole 45 deg (ex. standard symmetric quadrupole)

nh = 15 -- number of harmonics
np = 256 -- number of samples points
R = 2*25/3 -- reference radius
Rs = 0.95*25 -- sampling radius, can be the same as R or the largest still in the air