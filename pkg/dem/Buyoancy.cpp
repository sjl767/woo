#include<woo/pkg/dem/Buyoancy.hpp>
WOO_PLUGIN(dem,(HalfspaceBuyoancy));
WOO_IMPL__CLASS_BASE_DOC_ATTRS(woo_dem_HalfspaceBuyoancy_CLASS_BASE_DOC_ATTRS);

void HalfspaceBuyoancy::postLoad(HalfspaceBuyoancy&, void*){
	// check for valid attributes
	if(!node) throw std::runtime_error("HalfspaceBuyoancy.node may not be None!");
}


void HalfspaceBuyoancy::run(){
	DemField& dem=field->cast<DemField>();
	for(const auto& p: *dem.particles){
		// check mask
		if(mask!=0 && ((mask&p->mask)==0)) continue;
		// check that the particle is uninodal
		if(!p->shape || p->shape->nodes.size()!=1) continue;
		// all uninodal particles should have volumetrically equivalent radius
		// we will treat everything as sphere (even Ellipsoid or Capsule)
		Real rad=p->shape->equivRadius();
		if(isnan(rad)) continue; // but we check anyway...
		// depth, in local coordinates
		Real h=node->glob2loc(p->shape->nodes[0]->pos).z();
		// entirely above the liquid level, no force to apply
		if(h>=2*rad) continue;

		// force and torque applied to the particle (must be eventually applied in global coords!)
		// so make it clear what CS we use
		Vector3r F,T;

		// implement something meaningful here
		// gravity is dem.gravity (a Vector3r in global CS)
		F=T=Vector3r::Zero();



		// DemData instance for the node
		auto& dyn(p->shape->nodes[0]->getData<DemData>());
		// if we were in parallel section, use this for access sync: dyn.addForceTorque(F,T);
		dyn.force+=F; dyn.torque+=T;
	}
}

