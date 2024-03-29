o=Omega()

o.engines=[
    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Box_Aabb(),Bo1_Facet_Aabb()]),
    InteractionLoop([Ig2_Facet_Sphere_Dem3DofGeom()],[Ip2_FrictMat_FrictMat_FrictPhys()],[Law2_Dem3DofGeom_FrictPhys_CundallStrack()],),
    GravityEngine(gravity=[0,0,-10]),
    NewtonIntegrator(damping=0.01),
]
O.materials.append(FrictMat(young=1e3))
O.bodies.append([
    utils.facet([[-1,-1,0],[1,-1,0],[0,1,0]],dynamic=False,color=[1,0,0]),
    utils.facet([[1,-1,0],[0,1,0,],[1,.5,.5]],dynamic=False)
])
import random
if 1:
    for i in range(0,100):
        O.bodies.append(utils.sphere([random.gauss(0,1),random.gauss(0,1),random.uniform(1,2)],random.uniform(.02,.05),))
        O.bodies[len(O.bodies)-1].state['vel']=Vector3(random.gauss(0,.1),random.gauss(0,.1),random.gauss(0,.1))
else:
    O.bodies.append(utils.sphere([0,0,.6],.5))
O.dt=1e-4
O.saveTmp('init')
import woo.log
#woo.log.setLevel("InsertionSortCollider",woo.log.TRACE);
# compare 2 colliders:
if 0:
    O.timingEnabled=True
    from woo import timing
    for collider in InsertionSortCollider(),PersistentSAPCollider(haveDistantTransient=True):
        for i in range(2):
            O.loadTmp('init')
            utils.replaceCollider(collider)
            O.run(100,True)
            timing.reset()
            O.run(50000,True)
            timing.stats()
else:
    #O.run(100,True)
    O.step()
    print len(O.interactions)
    #O.bodies[2].phys['se3']=[-.6,0,.6,1,0,0,0]
    #O.step()
