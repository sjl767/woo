# File generated by kdevelop's qmake manager. 
# ------------------------------------------- 
# Subdir relative project main directory: ./yade/Body
# Target is a library:  

LIBS += -lActionVecVec \
        -lInteractionDescriptionSet \
        -rdynamic 
INCLUDEPATH = $(YADEINCLUDEPATH) 
MOC_DIR = $(YADECOMPILATIONPATH) 
UI_DIR = $(YADECOMPILATIONPATH) 
OBJECTS_DIR = $(YADECOMPILATIONPATH) 
QMAKE_LIBDIR = ../../toolboxes/DataStructures/ActionContainer/ActionVecVec/$(YADEDYNLIBPATH) \
               ../../plugins/Geometry/InteractionGeometry/InteractionGeometrySet/$(YADEDYNLIBPATH) \
               ../../plugins/Geometry/CollisionGeometry/CollisionGeometrySet/$(YADEDYNLIBPATH) \
               $(YADEDYNLIBPATH) 
QMAKE_CXXFLAGS_RELEASE += -lpthread \
                          -pthread 
QMAKE_CXXFLAGS_DEBUG += -lpthread \
                        -pthread 
DESTDIR = $(YADEDYNLIBPATH) 
CONFIG += debug \
          warn_on \
          dll 
TEMPLATE = lib 
HEADERS += Body.hpp \
           BodyContainer.hpp \
           ComplexBody.hpp \
           SimpleBody.hpp \
           BodyPhysicalParameters.hpp 
SOURCES += Body.cpp \
           BodyContainer.cpp \
           ComplexBody.cpp \
           SimpleBody.cpp \
           BodyPhysicalParameters.cpp 
