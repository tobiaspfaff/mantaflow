#
# explicit / implicit wave equation solve , as in 07IntroToPDEs.pdf
#
from manta import *

res = 100
gs  = vec3(res,res,1)
s   = Solver(name='main', gridSize = gs, dim=2)

# wave eq settings
implicit   = True
s.timestep = 1.0
cSqr       = 0.1
normalizeMass     = True
useCrankNicholson = False

# allocate grids
h     = s.create(RealGrid)
hprev = s.create(RealGrid)
hnew  = s.create(RealGrid)

flags = s.create(FlagGrid)
vel   = s.create(MACGrid)
curv  = s.create(RealGrid)
vel   = s.create(RealGrid)

flags.initDomain()
flags.fillGrid()

if (GUI):
    gui = Gui()
    gui.show( True )
    gui.pause()

source = s.create(Box, p0=gs*vec3(0.3,0.3,0.3), p1=gs*vec3(0.5,0.5,0.5))
source.applyToGrid(grid=h,     value=1)
hprev.copyFrom(h)
    
for t in range(1500):

	mass = totalSum( height=h )
	#print "Current mass %f " % mass

	if implicit:
		# implicit solve , cf. 07IntroToPDEs.pdf, page 19
		cgSolveWE( flags=flags, ut=h, utm1=hprev, out=hnew , cSqr=cSqr, crankNic=useCrankNicholson );

	else: 
		if	1:
			# explicit solve , cf. 07IntroToPDEs.pdf, page 16
			hnew.copyFrom(h)
			calcSecDeriv2d(h, curv)

			hnew.addScaledReal(h    ,  1.)
			hnew.addScaledReal(hprev, -1.) 
			hnew.addScaledReal(curv, cSqr * s.timestep*s.timestep) 

			hprev.copyFrom(h)
			h.copyFrom(hnew)

		else:
			# explicit solve , easier-to-read version with explicit velocity integration
			calcSecDeriv2d(h, curv)

			vel.addScaledReal(curv, cSqr * s.timestep)

			h.addScaledReal(vel,s.timestep)


	if normalizeMass:
		normalizeSumTo(h, mass)
	#massAfter = totalSum( height=h )
	#print "Current mass after normalization %f " % massAfter

	#gui.screenshot( 'out_%04d.png' % t );
	s.step()
