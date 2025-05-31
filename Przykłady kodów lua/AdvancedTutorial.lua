-- Advanced FEMM 4.2 Tutorial by Leslie Green CEng MIEE, Dec 2014
-- This LUA script simulates the pull force vs distance curve between two identical cylindrical magnets

-----------------------------------------------------------------------------------------------
-- modify these values to suit your needs
units = "millimeters"	-- should be one of "inches","millimeters","centimeters","mils","meters","micrometers" 
forceUnits= "lbf"		-- should be one of "lbf", "Newtons", "kgf"
magnetDia =   10.0
magnetHeight= 10.0
graphPoints = 100			-- Making this larger will increase simulation time proportionally.
plotRange =   3.0			-- the range of the gap is calculated for a multiple of the biggest of height and diameter of the magnet
magnetType= "NdFeB 40 MGOe"  -- has to be the EXACT name of a material in the materials library
-----------------------------------------------------------------------------------------------

showconsole()		-- does nothing if the console is already displayed
clearconsole()		-- clears both the input and output windows for a fresh start.
remove("c:\\FEMMresult.csv")	-- get rid of the old data file, if it exists

newdocument(0)		-- the 0 specifies a magnetics problem
mi_hidegrid()

-- define the problem type, equivalent to the top level menu    Problem
mi_probdef(0, units, "axi", 1E-8)

-- adds these materials from the Material Library to the project
mi_getmaterial(magnetType)	
mi_getmaterial("Air")

-- this bit is a bit of a pain. Although we have set the problem units above,
-- that has no effect on the calculation of c0 for the Asymptotic Boundary Condition
-- We therefore need to create a scaling factor for c0, dependant on the units
c0_scale=1.0
if units=="micrometers" then c0_scale= 1000000.0 end
if units=="millimeters" then c0_scale= 1000.0 end
if units=="centimeters" then c0_scale= 100.0 end
if units=="meters"      then c0_scale= 1.0 end			-- this is the easy one!
if units=="inches"      then c0_scale= 1.0/0.0254 end
if units=="mils"        then c0_scale= 1000.0/0.0254 end

forceScale = 1.0
if forceUnits=="Newtons" then forceScale= 1.0		end	-- the natural units of the weighted stress tensor
if forceUnits=="lbf"     then forceScale= 0.2248089	end
if forceUnits=="kgf"     then forceScale= 0.1019716	end

outFile, why = openfile("c:\\FEMMresult.csv","w")		-- note that Lua can return multiple values from a function
if outFile==nil then print("Failed to create result file: ", why) end

-- to remove uncertainty, write out a header in the results file
write(outFile, "# Magnet Material=", magnetType, "\n")
write(outFile, "# Magnet Diameter=", magnetDia, " ", units, "\n")
write(outFile, "# Magnet Height=", magnetHeight, " ", units, "\n")
write(outFile, "# Data format is ...", "\n")
write(outFile, "gap in ", units, ", force in ", forceUnits, "\n")

-- this is the main loop that does all the real work

for n= 1, graphPoints do			-- don't start from zero or you will get a zero gap
	print( "step ", n, " of ", graphPoints)			-- announce the step number to show progress
	
	if magnetDia > magnetHeight then
		gap = (magnetDia * plotRange * n)/graphPoints		-- note: the gap is never set to zero
	else
		gap = (magnetHeight * plotRange * n)/graphPoints		
	end
		
	-- set the size of the solution sphere radius as the larger of the magnet diameter and (twice the magnet height + twice the gap)
	radius = 2.0 * (magnetHeight + gap)
	if radius < magnetDia	then
	   radius = magnetDia
	end
	mi_zoom(-radius*0.1, -radius*1.05, radius*1.5, radius*1.05)	  -- set the window to a nice size for the problem
	
	-- as the radius changes we need to change the boundary condition to suit
	mi_deleteboundprop("ABC")
	c1=0
	c0= c0_scale/(uo*radius)
	mi_addboundprop("ABC",0,0,0,0,0,0,c0,c1,2)		-- create the Asymptotic Boundary Condition for the problem
	
	-- draw the r=0 axis and the outer boundary
	mi_addnode(0,-radius)
	mi_addnode(0, radius)
	mi_addsegment(0,-radius,0,radius)
	mi_addarc(0,-radius,0,radius,180,1)
	mi_selectarcsegment(0,radius)
	mi_setarcsegmentprop(1,"ABC",0,0)	-- make sure we set the Asymptotic boundary condition for the problem
	mi_refreshview()

	-- draw the upper magnet --------------------------------------------------------
	mi_addnode(0.0,gap/2.0)								-- bottom left
	mi_addnode(0.0, magnetHeight + gap/2.0)				-- top left
	mi_addsegment(0.0,gap/2.0,0.0,magnetHeight + gap/2.0)
	mi_addnode(magnetDia/2.0, magnetHeight + gap/2.0)	-- top right
	mi_addsegment(0.0,magnetHeight + gap/2.0,magnetDia/2.0,magnetHeight + gap/2.0)
	mi_addnode(magnetDia/2.0, gap/2.0)					-- bottom right
	mi_addsegment(magnetDia/2.0, magnetHeight + gap/2.0, magnetDia/2.0, gap/2.0)
	mi_addsegment(magnetDia/2.0, gap/2.0, 0.0, gap/2.0)
	mi_refreshview()
	
	-- draw the lower magnet --------------------------------------------------------
	mi_addnode(0.0, -gap/2.0)							-- top left
	mi_addnode(0.0, -magnetHeight -gap/2.0)				-- bottom left
	mi_addsegment(0.0, -gap/2.0, 0.0, -magnetHeight - gap/2.0)
	mi_addnode(magnetDia/2.0, -magnetHeight - gap/2.0)	-- bottom right
	mi_addsegment(0.0,-magnetHeight -gap/2.0, magnetDia/2.0, -magnetHeight - gap/2.0)
	mi_addnode(magnetDia/2.0, -gap/2.0)					-- top right
	mi_addsegment(magnetDia/2.0, -magnetHeight - gap/2.0, magnetDia/2.0, -gap/2.0)
	mi_addsegment(magnetDia/2.0, -gap/2.0, 0.0, -gap/2.0)
	mi_refreshview()
	
	-- add and set block properties --------------------------------------------------
	if (magnetDia/2.0) > magnetHeight then
		magMesh = magnetHeight/20.0
	else
		magMesh = magnetDia / 40.0
	end
	
	if (gap/3.0) < (radius/50.0) then
		airMesh = (gap/3.0)
	else
		airMesh = radius/50.0
	end
	
	mi_clearselected()
	mi_addblocklabel(magnetDia/4.0,  (magnetHeight+gap)/2.0)		-- upper magnet
	mi_selectlabel  (magnetDia/4.0,  (magnetHeight+gap)/2.0)
	mi_setblockprop(magnetType, 0, magMesh, "", 90, 0)
	
	mi_clearselected()
	mi_addblocklabel(magnetDia/4.0, -(magnetHeight+gap)/2.0)		-- lower magnet
	mi_selectlabel  (magnetDia/4.0, -(magnetHeight+gap)/2.0)	
	mi_setblockprop(magnetType, 0, magMesh, "", 90, 0)
	
	mi_clearselected()
	mi_addblocklabel(magnetDia/10.0, radius*0.9)					-- air
	mi_selectlabel  (magnetDia/10.0, radius*0.9)
	mi_setblockprop("Air", 0, airMesh, "", 0, 0)
	
	mi_clearselected()
	mi_refreshview()

	------------------ meshing and analysis
	mi_saveas("temp21354.fem")			-- you need to save before creating a mesh for some reason
	--mi_createmesh()		-- not strictly necessary, but helpful to see what is going on  --- UNCOMMENT for debugging
	mi_refreshview()
    mi_analyze()
    mi_loadsolution()		-- brings up the post-processor window of the solution
	
	mo_selectblock(magnetDia/4.0,  (magnetHeight+gap)/2.0)
    force = -forceScale * mo_blockintegral(19)	-- 19 is the z part of steady-state weighted stress tensor force
	write(outFile, gap, ",", force, "\n")

	----------------------------  get ready to start all over again by deleting all the nodes and labels
	if n==graphPoints then break end	-- leave a nice picture up at the end of the run
	mo_close()					-- close the post processor output window
	mi_purgemesh()
	mi_selectcircle(0,0,radius*1.1,0)
	mi_selectcircle(0,0,radius*1.1,1)
	mi_selectcircle(0,0,radius*1.1,2)
	mi_selectcircle(0,0,radius*1.1,3)
	mi_deleteselected();
	mi_refreshview()
end

result, why= flush(outFile)
if result==nil then print("Failed to flush file: ", why) end

result, why= closefile(outFile)
if result==nil then	print("Failed to close file: ", why) end

