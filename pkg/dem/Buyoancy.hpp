#pragma once
#include<woo/core/Engine.hpp>
#include<woo/pkg/dem/Particle.hpp>
struct HalfspaceBuyoancy: public Engine{
	bool acceptsField(Field* f) override { return dynamic_cast<DemField*>(f); }
	void postLoad(HalfspaceBuyoancy&, void*);
	virtual void run() override;
	#define woo_dem_HalfspaceBuyoancy_CLASS_BASE_DOC_ATTRS \
		HalfspaceBuyoancy,Engine,"Apply buyoancy force for uninodal particles, depending on their position in the :math:`-z` half-space in local coordinate system (:obj:`node`). TODO: references to papers, wikipedia with formulas, or write formulas here.", \
		((shared_ptr<Node>,node,make_shared<Node>(),AttrTrait<Attr::triggerPostLoad>(),"local coordinate system, of which :math:`-z` halfspace is active.")) \
		((uint,mask,uint(DemField::defaultMovableMask),,"Mask for particles buyoancy is applied to.")) \
		((Real,liqRho,1000,,"Density of the medium.")) \
		((Real,dragCoef,0.47,,"Drag coefficient."))
	WOO_DECL__CLASS_BASE_DOC_ATTRS(woo_dem_HalfspaceBuyoancy_CLASS_BASE_DOC_ATTRS);
};
WOO_REGISTER_OBJECT(HalfspaceBuyoancy);
