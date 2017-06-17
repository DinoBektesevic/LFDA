import detecttrails as dt
import numpy as np


###########################################################################
###############################    BRIGHT    ##############################
###########################################################################

#d = dt.DetectTrails(run=109, camcol=1, filter='i', frame=28)

#d = dt.DetectTrails(run=2888, camcol=1, filter='i', field=139)

#d = dt.DetectTrails(run=94, camcol=4, filter='r', field=168)

#d = dt.DetectTrails(run=3015, camcol=1, filter='i', frame=214)
#d = dt.DetectTrails(run=3015, camcol=1, filter='i', frame=215)
#d = dt.DetectTrails(run=3015, camcol=1, filter='i', frame=216)

#d = dt.DetectTrails(run=8108, camcol=5, filter='i', frame=25)

#d = dt.DetectTrails(run=2728, camcol=3, filter='i', frame=430)

#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=432) #connected to empty trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=433) #photoObj corrupted on SDSS, no extensions availible

#d = dt.DetectTrails(run=5973, camcol=3, filter='i', frame=129)
#d = dt.DetectTrails(run=5973, camcol=3, filter='i', frame=130)
###########################################################################
###############################    DIM    #################################
###########################################################################

#d = dt.DetectTrails(run=94, camcol=1, filter="i", field=311)
#d = dt.DetectTrails(run=94, camcol=1, filter="i", field=312)
#d = dt.DetectTrails(run=94, camcol=1, filter="i", field=313)

#see-through trail, bright but DIM detection
d = dt.DetectTrails(run=2728, camcol=2, filter='g', frame=424) 
#d = dt.DetectTrails(run=2728, camcol=2, filter='g', frame=425)

#d = dt.DetectTrails(run=7178, camcol=3, filter='r', frame=89)
#d = dt.DetectTrails(run=7178, camcol=3, filter='r', frame=90)

#d = dt.DetectTrails(run=2728, camcol=3, filter='u', frame=428)
#d = dt.DetectTrails(run=2728, camcol=3, filter='u', frame=429)

#d = dt.DetectTrails(run=5973, camcol=3, filter='r', frame=131) #connected to a false det.
###########################################################################
###############################    EMPTY   ################################
###########################################################################

#d = dt.DetectTrails(run=94, camcol=1, filter="i", field=262)

#d = dt.DetectTrails(run=211, camcol=1, filter='i', frame=197)

#d = dt.DetectTrails(run=2728, camcol=2, filter='g', frame=280)

#d = dt.DetectTrails(run=2888, camcol=1, filter='i', field=15)
#giant star and a large galaxy
#d = dt.DetectTrails(run=2888, camcol=1, filter='i', field=17)

#d = dt.DetectTrails(run=3614, camcol=1, filter='i', frame=28)
#d = dt.DetectTrails(run=3614, camcol=1, filter='i', frame=39)
#d = dt.DetectTrails(run=3614, camcol=1, filter='i', frame=53)
#d = dt.DetectTrails(run=3614, camcol=1, filter='i', frame=54)
#d = dt.DetectTrails(run=3614, camcol=3, filter='i', frame=74)
#d = dt.DetectTrails(run=3614, camcol=4, filter='i', frame=52)
#d = dt.DetectTrails(run=3614, camcol=5, filter='i', frame=46)
#d = dt.DetectTrails(run=3614, camcol=6, filter='i', frame=58)

#d = dt.DetectTrails(run=3634, camcol=1, filter='i', frame=54)

#d = dt.DetectTrails(run=4569, camcol=4, filter='i', field=146)

#d = dt.DetectTrails(run=5973, camcol=3, filter='u', frame=132)

#very bright star as a false detection generator
#d = dt.DetectTrails(run=7787, camcol=1, filter='i', field=45)

#d = dt.DetectTrails(run=7787, camcol=1, filter='i', field=91)  
#d = dt.DetectTrails(run=7787, camcol=1, filter='i', field=131)
#d = dt.DetectTrails(run=7787, camcol=1, filter='i', field=336)

#d = dt.DetectTrails(run=8108, camcol=5, filter='i', frame=26)
#d = dt.DetectTrails(run=8108, camcol=5, filter='i', frame=27)

#d = dt.DetectTrails(run=2728, camcol=3, filter='i', frame=431) #empty

#d = dt.DetectTrails(run=2728, camcol=4, filter='i', frame=432) #empty/trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='i', frame=433) #photoObj corrupted on SDSS servers
#d = dt.DetectTrails(run=2728, camcol=4, filter='i', frame=434) #empty/trail debris

#d = dt.DetectTrails(run=2728, camcol=3, filter='r', frame=432) #empty/trail debris
#d = dt.DetectTrails(run=2728, camcol=3, filter='r', frame=433) #empty/trail debris
#d = dt.DetectTrails(run=2728, camcol=3, filter='r', frame=434) #empty/trail debris

#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=434) #empty/very bright trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=435) #empty/very bright trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=436) #empty/very bright trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=437) #empty/trail debris
#d = dt.DetectTrails(run=2728, camcol=4, filter='r', frame=438) #empty/trail debris

#d = dt.DetectTrails(run=2728, camcol=3, filter='u', frame=430)

#d = dt.DetectTrails(run=2728, camcol=2, filter='z', frame=424)
#d = dt.DetectTrails(run=2728, camcol=2, filter='z', frame=425)

###########################################################################
###############################    FAILS   ################################
###########################################################################

#TOO SHORT! BoxHough is ok, but hough fails to detect it on actual image
#d = dt.DetectTrails(run=94, camcol=4, filter='i', frame=497)

#not short, still fails, hough in actual image gets fitted over a star, change nlinesinset?
#########
#d = dt.DetectTrails(run=125, camcol=1, filter='i', frame=216)

#VERY VERY THIN, gets eroded to nothing
#d = dt.DetectTrails(run=273, camcol=6, filter='i', frame=116)

#Erases a massive amount of stars and eats the trail, possible fix?
#d = dt.DetectTrails(run=5415, camcol=1, filter='i', frame=55)


#VERY VERY VERY FAINT
#d = dt.DetectTrails(run=5973, camcol=3, filter='r', frame=132)
#FAINT, but brighter than 5973-3-r-132, erosion eats my trail
#d = dt.DetectTrails(run=5973, camcol=3, filter='u', frame=127)

#again very thin, erosion breaks up the trail too much and no rect are found
#d = dt.DetectTrails(run=7675, camcol=6, filter='i', frame=150)

#d = dt.DetectTrails(run=5973, camcol=3, filter='r', frame=132) #very dim trail, fails

#trail eroded away both times, trail very dim
#d = dt.DetectTrails(run=5973, camcol=3, filter='u', frame=127)
#d = dt.DetectTrails(run=5973, camcol=3, filter='u', frame=128)

#brighter trail transitions into dim, transparent, borderline detection at
#certain parameters
#d = dt.DetectTrails(run=5973, camcol=3, filter='u', frame=128)








d.params_removestars['magcount'] = 3;
d.params_removestars['maxmagdiff'] = 5;
#d.params_removestars['defaultxy'] = 10;

#d.params_removestars["maxmagdiff"] = 5

#d.params_bright['dro'] = 25;
#d.params_bright['lineSetTresh'] = 0.15;
#d.params_bright["dilateKernel"] = np.ones((3,3))

#d.params_dim['minFlux'] = 0.03;
#d.params_dim['dro'] = 25;
#d.params_dim['erodeKernel'] = np.ones((2,2))
#d.params_dim['dilateKernel'] = np.ones((10,10))
#d.params_dim["nlinesInSet"] = 2
#d.params_dim["dro"] = 30

d.params_bright["debug"]=True
d.params_dim["debug"] = True

d.process()
d.results.close()
d.errors.close()
