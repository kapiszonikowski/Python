      -- *************************************
      -- ********* Mikes DC magnet ******
      -- *************************************
      
      mi_probdef( 0, "millimeters", "planar", "1E-8")      
      
      --Adding nodes defining the half C-core
      mi_addnode( 0,  60)      -- A
      mi_addnode(-50,  60)      -- B
      mi_addnode(-50,  0)      -- C
      mi_addnode(-70,  0)      -- D
      mi_addnode(-70,  60)      -- E
      mi_addnode(-50,  80)      -- F
      mi_addnode( 0,  80)      -- G
      
      -- Joining nodes to define half C-core
      mi_addsegment( 0,  60, -50,  60)      -- AB
      mi_addsegment(-50,  60, -50,  0)      -- BC
      mi_addsegment(-50,  0, -70,  0)      -- CD
      mi_addsegment(-70,  0, -70,  60)      -- DE
      mi_addarc(-50,  80, -70,  60,  90,  10)      -- EF
      mi_addsegment(-50,  80,  0,  80)      -- FG
      
      --Adding nodes defining left half of keeper
      mi_addnode( 0, -5)      -- H
      mi_addnode(-90, -5)      -- I
      mi_addnode(-90, -15)      -- J
      mi_addnode( 0, -15)      -- K
      
      --Joining nodes to define left half of keeper
      mi_addsegment( 0, -5, -90, -5)      -- HI
      mi_addsegment(-90, -5, -90, -15)      -- IJ
      mi_addsegment(-90, -15,  0, -15)      -- JK
      
      --Adding nodes to define Boundary(Left half)

      mi_addnode( 0,  200)      -- L
      mi_addnode(-200,  200)      -- M
      mi_addnode(-200, -100)      -- N
      mi_addnode( 0, -100)      -- O
      
      --Joining nodes to define Boundary(Left half)

      mi_addsegment( 0,  200, -200,  200)      -- LM
      mi_addsegment(-200,  200, -200, -100)      -- MN
      mi_addsegment(-200, -100,  0, -100)      -- NO
      
      --Adding nodes to define Bottom coil (half)

      mi_addnode( 0,  58)      -- P
      mi_addnode(-35,  58)      -- Q
      mi_addnode(-35,  38)      -- R
      mi_addnode( 0,  38)      -- S
      
      -- Joining nodes to define Bottom coil (half)

      mi_addsegment( 0,  58, -35,  58)      -- PQ
      mi_addsegment(-35,  58, -35,  38)      -- QR
      mi_addsegment(-35,  38,  0,  38)      -- RS
      
      --mirroring to get the top half coil
      mi_selectsegment(-18,  58)      -- PQ
      mi_selectsegment(-35,  48)      -- QR
      mi_selectsegment(-18,  38)      -- RS
      
      mi_mirror(-10,  70,  10,  70,  1)      -- 
      mi_clearselected()      
      
      --Selecting segments for mirroring about Y-axis.
      mi_selectsegment(-18,  58)      -- PQ
      mi_selectsegment(-35,  48)      -- QR
      mi_selectsegment(-18,  38)      -- RS
      mi_selectsegment(-25,  60)      -- AB
      mi_selectsegment(-50,  30)      -- BC
      mi_selectsegment(-60,  0)      -- CD
      mi_selectsegment(-70,  30)      -- DE
      mi_selectsegment(-25,  80)      -- FG
      mi_selectsegment(-18,  82)      -- PQ'
      mi_selectsegment(-35,  92)      -- QR'
      mi_selectsegment(-18,  102)      -- RS'
      mi_selectsegment(-45, -5)      -- HI
      mi_selectsegment(-90, -10)      -- IJ
      mi_selectsegment(-45, -15)      -- JK
      mi_selectsegment(-100,  200)      -- LM
      mi_selectsegment(-200,  50)      -- MN
      mi_selectsegment(-100, -100)      -- NO
      
      mi_mirror( 0,  0,  0,  20,  1)      -- 
      mi_clearselected()      -- 
      
      mi_addarc( 70,  60,  50,  80,  90,  10)      -- FE'
      --Geometry, including Boundary completes here.
      mi_zoomnatural()      
      messagebox("Geometry entered.")      
      
      --Defining Boundary Condition
      mi_addboundprop("outer",  0,  0,  0,  0,  0,  0,  0,  0,  0)      
      
      --Defining Excitations
      mi_addcircprop("plus",  2500,  0,  0,  0)      
      mi_addcircprop("minus",  2500,  0,  0,  0)      
      
      -- Assigning boundary condition
      mi_selectsegment(-100,  200)      -- LM
      mi_selectsegment(-200,  50)      -- MN
      mi_selectsegment(-100, -100)      -- NO
      mi_selectsegment( 100,  200)      -- LM'
      mi_selectsegment( 200,  50)      -- MN'
      mi_selectsegment( 100, -100)      -- NO'
      mi_setsegmentprop("outer",  1,  1,  0,  0)      
      mi_clearselected()      
      
      -- Defining materials
      mi_addmaterial("Steel 1010",  800,  800,  0,  0,  0,  0,  0,  0,  1,  0)      
      
      mi_addbhpoint("Steel 1010", 0.066, 51)      
      mi_addbhpoint("Steel 1010", 0.132, 104)      
      mi_addbhpoint("Steel 1010", 0.201, 148)      
      mi_addbhpoint("Steel 1010", 0.279, 168)      
      mi_addbhpoint("Steel 1010", 0.358, 179)      
      mi_addbhpoint("Steel 1010", 0.440, 193)      
      mi_addbhpoint("Steel 1010", 0.533, 215)      
      mi_addbhpoint("Steel 1010", 0.640, 245)      
      mi_addbhpoint("Steel 1010", 0.750, 279)      
      mi_addbhpoint("Steel 1010", 0.850, 318)      
      mi_addbhpoint("Steel 1010", 0.929, 366)      
      mi_addbhpoint("Steel 1010", 1.009, 414)      
      mi_addbhpoint("Steel 1010", 1.080, 462)      
      mi_addbhpoint("Steel 1010", 1.136, 509)      
      mi_addbhpoint("Steel 1010", 1.179, 557)      
      mi_addbhpoint("Steel 1010", 1.214, 605)      
      mi_addbhpoint("Steel 1010", 1.239, 642)      
      mi_addbhpoint("Steel 1010", 1.259, 675)      
      mi_addbhpoint("Steel 1010", 1.286, 728)      
      mi_addbhpoint("Steel 1010", 1.311, 796)      
      mi_addbhpoint("Steel 1010", 1.360, 963)      
      mi_addbhpoint("Steel 1010", 1.419, 1185)      
      mi_addbhpoint("Steel 1010", 1.476, 1477)      
      mi_addbhpoint("Steel 1010", 1.519, 1859)      
      mi_addbhpoint("Steel 1010", 1.555, 2338)      
      mi_addbhpoint("Steel 1010", 1.587, 2852)      
      mi_addbhpoint("Steel 1010", 2.080, 47747)      
      
      mi_addmaterial("air",  1,  1,  0,  0,  0,  0,  0,  0,  1,  0)      
      mi_addmaterial("copper",  1,  1,  0,  0,  0,  0,  0,  0,  1,  0)      
      
      -- Assigning material properties
      mi_addblocklabel( 0,  151)      
      mi_selectlabel( 0,  151)      
      mi_setblockprop("air",  0,  10,  0,  0,  0,  0)      
      mi_clearselected()      
      
      mi_addblocklabel( 0, -10)      
      mi_selectlabel( 0, -10)      
      mi_setblockprop("Steel 1010",  0,  3,  0,  0,  4,  0)      
      mi_clearselected()      
      
      mi_addblocklabel( 0,  70)      
      mi_selectlabel( 0,  70)      
      mi_setblockprop("Steel 1010",  0,  4,  0,  0,  0,  0)      
      mi_clearselected()      
      
      
      mi_addblocklabel( 0,  48)      
      mi_selectlabel( 0,  48)      
      mi_setblockprop("copper",  0,  7.5, "plus",  0,  0,  0)      
      mi_clearselected()      
      
      mi_addblocklabel( 0,  87)      
      mi_selectlabel( 0,  87)      
      mi_setblockprop("copper",  0,  7.5, "minus",  0,  0,  0)      
      mi_clearselected()      
      
      mi_zoomnatural()      
      
      mi_saveas("C:\\Data\\DavidMeekerMagnetics\\femm42\\examples\\Mikes DC Magnet\\mikesDC.fem")      
      messagebox("Saved as mikesDC.fem")      
      mi_createmesh()      
      mi_analyze( 1)      
      messagebox("Meshed and analyzed")      
      
      mi_loadsolution()      
      messagebox("Solution loaded")      
      
      mo_smooth("on")      
      mo_showdensityplot( 1,  0,  1.5,  0, "bmag")      
      mo_savebitmap("C:\\Data\\DavidMeekerMagnetics\\femm42\\examples\\Mikes DC Magnet\\density.bmp")      
      messagebox("Density plotted and saved")      
      -- Add first contour
      mo_seteditmode("contour")      
      mo_addcontour(-130, -2.5)      
      mo_addcontour( 130, -2.5)      
      
      -- B,n plot
      mo_makeplot( 2,  200)      
      
      mo_makeplot( 2,  200, "C:\\Data\\DavidMeekerMagnetics\\femm42\\examples\\Mikes DC Magnet\\mikesDC_1.txt",  0)      
      messagebox("B.n plotted and saved")      
      
      mo_clearcontour()      
      -- Add second contour
      mo_seteditmode("contour")      
      mo_addcontour( 0, -2)      
      mo_addcontour( 0, -18)      
      -- B,n plot
      mo_makeplot( 2,  200)      
      
      mo_makeplot( 2,  200, "C:\\Data\\DavidMeekerMagnetics\\femm42\\examples\\Mikes DC Magnet\\mikesDC_2.txt",  0)      
      messagebox("B.n plotted and saved")      
      
      mo_clearcontour()      

