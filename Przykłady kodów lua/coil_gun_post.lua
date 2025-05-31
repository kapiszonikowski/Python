outfile = "hollow_cylinder_results.txt"

-- read projectile's position at its centerpoint
handle = openfile("tempfile", "r")
position = read(handle, "*n")
closefile(handle)

-- Select the solenoid coil, to prepare for integration
groupselectblock(2)

-- Option 10 tells you the volume.
-- Option 12 computes mechanical force. 
-- Read the manual; it can compute lots of other things!
force = blockintegral(12)

-- Output volume and force to results file
handle = openfile(outfile,"a")
write(handle, position, "\t", force, "\n")
closefile(handle)

exitpost()