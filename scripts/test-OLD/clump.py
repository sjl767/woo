from woo.core import*
from woo.dem import *
O.scene.engines=[
    ForceResetter(),
    InsertionSortCollider([
        Bo1_Sphere_Aabb(),
        Bo1_Box_Aabb(),
    ]),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(),Ig2_Box_Sphere_ScGeom()],
        [Ip2_FrictMat_FrictMat_FrictPhys()],
        [Law2_ScGeom_FrictPhys_CundallStrack()]
    ),
    GravityEngine(gravity=[0,0,-9.81]),
    NewtonIntegrator(damping=.2,exactAsphericalRot=True)
]
# support
O.dem.par.append(utils.box([0,0,-1.5],[3,3,.2],dynamic=False))
# stand-alone sphere
O.dem.par.append(utils.sphere([0,0,0],.5))
# clumps
relPos=[(0,-.5,-.5),(0,.5,0),(.5,0,0),(0,0,.5)]
coords=[(-2,0,0),(2,0,0),(0,2,0),(0,-2,0)]
for i,cc in enumerate(coords):
    # This shorthand command does something like this:
    # O.bodies.appendClumped([utils.sphere(...),utils.sphere(...),utils.sphere(...)])
    # and returns tuple of clumpId,[bodyId1,bodyId2,bodyId3]
    clump,spheres=O.dem.parappendClumped([utils.sphere([relPos[j][0]+coords[i][0],relPos[j][1]+coords[i][1],relPos[j][2]+coords[i][2]],.5) for j in range(0,i+1)])
    print clump,spheres
O.scene.dt=utils.PWaveTimeStep()
O.saveTmp('init')

