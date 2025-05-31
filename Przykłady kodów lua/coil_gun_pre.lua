-------------------------------------------------
-- Main program
-------------------------------------------------
project = "hollow_cylinder"
outfile = project .. "_results.txt"
start_time = date()

-- Amount the projectile radius grows
increment = 0.3

handle = openfile(outfile, "w")		-- overwrite old results file!
write(handle, "\nInvestigating radius of hollow cylinder projectile \n")
write(handle, "Start time: ", start_time, "\n" )
write(handle, "Coil is 20mm long\n" )
write(handle, "    3mm inside radius\n" )
write(handle, "    6mm outside radius\n" )
write(handle, "Projectile is 10mm long\n" )
write(handle, "    0.1 inside radius (initial)\n" )
write(handle, "    1.1 outside radius (initial)\n")
closefile(handle)

-- Save model under new name, so it can't affect your carefully prepared
-- starting model. The new name also prevents losing your work if you get
-- a runaway solution that you have to kill in the Task Manager.
save_femm_file("temp.fem")

-- Prepare for selecting and moving the group of points in the projectile.
seteditmode("group")

-- Loop through the sizes of projectile; each one is 'increment' larger
for i=0,5 do
	inside_radius = 0.1 + (i * increment)

	handle = openfile(outfile,"a")
	write(handle, "\nInside radius ", inside_radius, ", iteration ", i, "\n")
	closefile(handle)

	-- Loop through all the projectile positions along firing tube
	for n=1,25 do
		-- Save current position for post-processor
		handle = openfile("tempfile","w")
		pos = n-25
		write(handle, pos)
		closefile(handle)

		-- Solve and save results
		showmesh()
		analyse()
		run_post(project .. "_post.lua")

		-- Nudge projectile downward by 1mm
		selectgroup(1)
		move_translate(0,-1)	
	end

	-- Move projectile back to starting position, and
	-- increase radii by 'increment'
	selectgroup(1)
	move_translate(increment, 25)
end

-----------------------------------------------
-- Document the total run time and finish up --
-----------------------------------------------
handle = openfile(outfile, "a")
end_time = date()
write(handle, "\nEnd time: ", end_time )
closefile(handle)

messagebox("All done!\n\nStarted " .. start_time .. "\nFinished " .. end_time)