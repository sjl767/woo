# File generated by kdevelop's qmake manager. 
# ------------------------------------------- 
# Subdir relative project main directory: ./plugins/CollisionFunctor/CollisionFunctor4SDECContactModel/Sphere2Sphere4SDECContactModel
# Target is a library:  

LIBS += -lSphere \
        -lM2D \
        -lM3D \
        -lRand \
        -lConstants \
        -lSerialization \
        -rdynamic 
INCLUDEPATH = ../../../../plugins/GeometricalModel/Sphere \
              ../../../../toolboxes/Math/M2D \
              ../../../../toolboxes/Math/M3D \
              ../../../../toolboxes/Math/Rand \
              ../../../../toolboxes/Math/Constants \
              ../../../../toolboxes/Libraries/Serialization 
MOC_DIR = $(YADECOMPILATIONPATH) 
UI_DIR = $(YADECOMPILATIONPATH) 
OBJECTS_DIR = $(YADECOMPILATIONPATH) 
QMAKE_LIBDIR = ../../../../plugins/GeometricalModel/Sphere/$(YADEDYNLIBPATH) \
               ../../../../toolboxes/Math/M2D/$(YADEDYNLIBPATH) \
               ../../../../toolboxes/Math/M3D/$(YADEDYNLIBPATH) \
               ../../../../toolboxes/Math/Rand/$(YADEDYNLIBPATH) \
               ../../../../toolboxes/Math/Constants/$(YADEDYNLIBPATH) \
               ../../../../toolboxes/Libraries/Serialization/$(YADEDYNLIBPATH) \
               $(YADEDYNLIBPATH) 
DESTDIR = $(YADEDYNLIBPATH) 
CONFIG += release \
          warn_on \
          dll 
TEMPLATE = lib 
