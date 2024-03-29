# encoding: utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from woo.qt.ObjectEditor import *
import woo
import woo.qt
import woo.config
from woo.dem import *
#from woo.sparc import *
from woo.core import *

try: from woo.gl import *
except ImportError: pass


class EngineInspector(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        grid=QGridLayout(self); grid.setSpacing(0); grid.setMargin(0)
        self.serEd=SeqObject(parent=None,getter=lambda:woo.master.scene.engines,setter=lambda x:setattr(woo.master.scene,'engines',x),T=Engine,trait=[t for t in Scene._attrTraits if t.name=='engines'][0],path='woo.master.scene.engines')
        grid.addWidget(self.serEd)
        self.setLayout(grid)
#class MaterialsInspector(QWidget):
#    def __init__(self,parent=None):
#        QWidget.__init__(self,parent)
#        grid=QGridLayout(self); grid.setSpacing(0); grid.setMargin(0)
#        self.serEd=SeqObject(parent=None,getter=lambda:O.materials,setter=lambda x:setattr(O,'materials',x),serType=Engine)
#        grid.addWidget(self.serEd)
#        self.setLayout(grid)

class CellInspector(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.layout=QVBoxLayout(self) #; self.layout.setSpacing(0); self.layout.setMargin(0)
        self.periCheckBox=QCheckBox('periodic boundary',self)
        self.periCheckBox.clicked.connect(self.update)
        self.layout.addWidget(self.periCheckBox)
        self.scroll=QScrollArea(self); self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
        self.refresh()
        self.refreshTimer=QTimer(self)
        self.refreshTimer.timeout.connect(self.refresh)
        self.refreshTimer.start(1000)
    def refresh(self):
        S=woo.master.scene
        self.periCheckBox.setChecked(S.periodic)
        editor=self.scroll.widget()
        if not S.periodic and editor: self.scroll.takeWidget()
        if (S.periodic and not editor) or (editor and editor.ser!=S.cell):
            self.scroll.setWidget(ObjectEditor(S.cell,parent=self,showType=True,path='woo.master.cell'))
    def update(self):
        self.scroll.takeWidget() # do this before changing periodicity, otherwise the ObjectEditor will raise exception about None object
        S=woo.master.scene
        S.periodic=self.periCheckBox.isChecked()
        self.refresh()
        
class SceneInspector(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        grid=QGridLayout(self); grid.setSpacing(0); grid.setMargin(0)
        self.serEd=ObjectEditor(woo.master.scene,parent=self,showType=False,path='woo.master.scene')
        grid.addWidget(self.serEd)
        self.setLayout(grid)

def makeBodyLabel(b):
    ret=unicode(b.id)+u' '
    if not b.shape: ret+=u'⬚'
    else:
        typeMap={'Sphere':u'⚫','Facet':u'△','FlexFacet':u'⧋','Wall':u'┃','Box':u'⎕','Cylinder':u'⌭','Clump':u'☍','InfCylinder':u'◎','Ellipsoid':u'⬯','Capsule':u'O'}
        ret+=typeMap.get(b.shape.__class__.__name__,u'﹖')
    if (b.shape.nodes)==1 and b.blocked!='': ret+=u'⚓'
    return ret

def getBodyIdFromLabel(label):
    try:
        return int(unicode(label).split()[0])
    except ValueError:
        print 'Error with label:',unicode(label)
        return -1

class BodyInspector(QWidget):
    def __init__(self,parId=None,parent=None,bodyLinkCallback=None,intrLinkCallback=None):
        QWidget.__init__(self,parent)
        self.parId=(0 if parId==None else parId)
        if 'opengl' in woo.config.features:
            v=woo.qt.views()
            if parId==None and len(v)>0 and v[0].selection>0: self.bodyId=v[0].selection
        self.idGlSync=self.parId
        self.bodyLinkCallback,self.intrLinkCallback=bodyLinkCallback,intrLinkCallback
        self.bodyIdBox=QSpinBox(self)
        self.bodyIdBox.setMinimum(0)
        self.bodyIdBox.setMaximum(1000000000)
        self.bodyIdBox.setValue(self.parId)
        self.intrWithCombo=QComboBox(self);
        self.gotoBodyButton=QPushButton(u'→ #',self)
        self.gotoIntrButton=QPushButton(u'→ #+#',self)
        # id selector
        topBoxWidget=QWidget(self); topBox=QHBoxLayout(topBoxWidget); topBox.setMargin(0); #topBox.setSpacing(0); 
        hashLabel=QLabel('#',self); hashLabel.setFixedWidth(8)
        topBox.addWidget(hashLabel)
        topBox.addWidget(self.bodyIdBox)
        self.plusLabel=QLabel('+',self); topBox.addWidget(self.plusLabel)
        hashLabel2=QLabel('#',self); hashLabel2.setFixedWidth(8); topBox.addWidget(hashLabel2)
        topBox.addWidget(self.intrWithCombo)
        topBox.addStretch()
        topBox.addWidget(self.gotoBodyButton)
        topBox.addWidget(self.gotoIntrButton)
        topBoxWidget.setLayout(topBox)
        # forces display
        forcesWidget=QFrame(self); forcesWidget.setFrameShape(QFrame.Box); self.forceGrid=QGridLayout(forcesWidget); 
        self.forceGrid.setVerticalSpacing(0); self.forceGrid.setHorizontalSpacing(9); self.forceGrid.setMargin(4);
        for i,j in itertools.product((0,1,2,3),(-1,0,1,2)):
            lab=QLabel('<small>'+('force','torque','move','rot')[i]+'</small>' if j==-1 else ''); self.forceGrid.addWidget(lab,i,j+1);
            if j>=0: lab.setAlignment(Qt.AlignRight)
            if i>1: lab.hide() # do not show forced moves and rotations by default (they will appear if non-zero)
        self.showMovRot=False
        #
        self.grid=QGridLayout(self); self.grid.setSpacing(0); self.grid.setMargin(0)
        self.grid.addWidget(topBoxWidget)
        self.grid.addWidget(forcesWidget)
        self.scroll=QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.grid.addWidget(self.scroll)
        self.tryShowBody()
        self.bodyIdBox.valueChanged.connect(self.bodyIdSlot)
        self.gotoBodyButton.clicked.connect(self.gotoBodySlot)
        self.gotoIntrButton.clicked.connect(self.gotoIntrSlot)
        self.refreshTimer=QTimer(self)
        self.refreshTimer.timeout.connect(self.refreshEvent)
        self.refreshTimer.start(1000)
        self.intrWithCombo.addItems(['0']); self.intrWithCombo.setCurrentIndex(0);
        self.intrWithCombo.setMinimumWidth(80)
        if self.parId==None: self.setWindowTitle('Particle')
        else: self.setWindowTitle('Particle #%d'%self.parId)
        self.gotoBodySlot()
    def displayForces(self):
        if self.parId==None: return
        S=woo.master.scene
        b=S.dem.par[self.parId]
        if not b.shape: noshow='no shape'
        elif len(b.shape.nodes)==0: noshow='no nodes'
        elif len(b.shape.nodes)>1: noshow='multinodal'
        elif not b.shape.nodes[0].dem: noshow='no Node.dem'
        else: noshow=None
        if noshow:
            self.forceGrid.itemAtPosition(0,1).widget().setText('<small>'+noshow+'</small>')
            for i,j in ((0,2),(0,3),(1,1),(1,2),(1,3)): self.forceGrid.itemAtPosition(i,j).widget().setText('')
        else:
            try:
                d=b.shape.nodes[0].dem
                val=[d.force,d.torque]
                rows=(0,1)
                for i,j in itertools.product(rows,(0,1,2)): self.forceGrid.itemAtPosition(i,j+1).widget().setText('<small>'+str(val[i][j])+'</small>')
            except IndexError:pass
    def tryShowBody(self):
        try:
            if self.parId==None: raise IndexError()
            b=woo.master.scene.dem.par[self.parId]
            self.serEd=ObjectEditor(b,showType=True,parent=self,path='woo.master.scene.dem.par[%d]'%self.parId)
        except IndexError:
            if self.bodyIdBox.hasFocus(): return False
            self.serEd=QFrame(self)
            self.parId=None
        self.scroll.setWidget(self.serEd)
        return True
    def changeIdSlot(self,newId):
        self.bodyIdBox.setValue(newId);
        self.bodyIdSlot(newId)
    def bodyIdSlot(self,currId):
        self.parId=currId
        if not self.tryShowBody():
            self.bodyIdBox.setStyleSheet('QWidget { background: red }')
            return # we still have focus, don't attempt to change
        else:
            self.bodyIdBox.setStyleSheet('QWidget { background: none }')
        # self.parId=currId # self.bodyIdBox.value()
        if self.parId==None: self.setWindowTitle('Particle')
        else: self.setWindowTitle('Particle #%d'%self.parId)
        self.refreshEvent()
    def gotoBodySlot(self):
        try:
            id=int(getBodyIdFromLabel(self.intrWithCombo.currentText()))
        except ValueError: return # empty id
        if not self.bodyLinkCallback:
            self.bodyIdBox.setValue(id); self.parId=id
        else: self.bodyLinkCallback(id)
    def gotoIntrSlot(self):
        ids=self.bodyIdBox.value(),getBodyIdFromLabel(self.intrWithCombo.currentText())
        if not self.intrLinkCallback:
            self.ii=InteractionInspector(ids)
            self.ii.show()
        else: self.intrLinkCallback(ids)
    def refreshEvent(self):
        S=woo.master.scene
        try: S.dem.par[self.parId]
        except: self.parId=None # invalidate deleted body
        # no body shown yet, try to get the first one...
        if self.parId==None and len(S.dem.par)>0:
            try:
                # print 'SET ZERO'
                b=S.dem.par[0]; self.bodyIdBox.setValue(0); self.parId=0
            except IndexError: pass
        if 'opengl' in woo.config.features:
            v=woo.qt.views()
            if len(v)>0 and v[0].selection!=self.parId:
                if self.idGlSync==self.parId: # changed in the viewer, reset ourselves
                    self.parId=self.idGlSync=v[0].selection; self.changeIdSlot(self.parId)
                    return
                elif self.parId!=None: v[0].selection=self.idGlSync=self.parId # changed here, set in the viewer
        meId=self.bodyIdBox.value(); pos=self.intrWithCombo.currentIndex()
        try:
            meLabel=makeBodyLabel(S.dem.par[meId])
        except IndexError: meLabel=u'…'
        self.plusLabel.setText(' '.join(meLabel.split()[1:])+'  <b>+</b>') # do not repeat the id
        self.bodyIdBox.setMaximum(len(S.dem.par)-1)
        try: others=S.dem.par[meId].con
        except IndexError: others=[]
        #(i.id1 if i.id1!=meId else i.id2) for i in O.interactions.withBody(self.bodyIdBox.value()) if i.isReal]
        others.sort()
        self.intrWithCombo.clear()
        self.intrWithCombo.addItems([makeBodyLabel(S.dem.par[i]) for i in others])
        if pos>self.intrWithCombo.count() or pos<0: pos=0
        self.intrWithCombo.setCurrentIndex(pos);
        other=self.intrWithCombo.itemText(pos)
        if other=='':
            self.gotoBodyButton.setEnabled(False); self.gotoIntrButton.setEnabled(False)
            other=u'∅'
        else:
            self.gotoBodyButton.setEnabled(True); self.gotoIntrButton.setEnabled(True)
        self.gotoBodyButton.setText(u'→ %s'%other)
        self.gotoIntrButton.setText(u'→ %s + %s'%(meLabel,other))
        self.displayForces()
        
class InteractionInspector(QWidget):
    def __init__(self,ids=None,parent=None,bodyLinkCallback=None):
        QWidget.__init__(self,parent)
        self.bodyLinkCallback=bodyLinkCallback
        self.ids=ids
        self.intrLinIxBox=QSpinBox(self)
        self.intrLinIxBox.setMinimum(0)
        self.intrLinIxBox.setMaximum(1000000000)
        self.gotoId1Button=QPushButton(u'#…',self)
        self.gotoId2Button=QPushButton(u'#…',self)
        self.gotoId1Button.clicked.connect(self.gotoId1Slot)
        self.gotoId2Button.clicked.connect(self.gotoId2Slot)
        self.intrLinIxBox.valueChanged.connect(self.setLinIxSlot)
        topBoxWidget=QWidget(self)
        topBox=QHBoxLayout(topBoxWidget)
        topBox.addWidget(self.intrLinIxBox)
        topBox.addWidget(self.gotoId1Button)
        labelPlus=QLabel('+',self); labelPlus.setAlignment(Qt.AlignHCenter)
        topBox.addWidget(labelPlus)
        topBox.addWidget(self.gotoId2Button)
        topBoxWidget.setLayout(topBox)
        self.setWindowTitle(u'No contact')
        self.grid=QGridLayout(self); self.grid.setSpacing(0); self.grid.setMargin(0)
        self.grid.addWidget(topBoxWidget,0,0)
        self.scroll=QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.grid.addWidget(self.scroll)
        self.refreshTimer=QTimer(self)
        self.refreshTimer.timeout.connect(self.refreshEvent)
        self.refreshTimer.start(1000)
        if self.ids: self.setupInteraction()
    def setupInteraction(self):
        'Change view; called whenever the interaction to be displayed changes'
        S=woo.master.scene
        try:
            if self.ids==None: raise IndexError() # to be caught right away
            intr=S.dem.con[self.ids] # also might raise IndexError, if the contact is dead
            if not intr: raise IndexError()
            self.intrLinIxBox.setValue(intr.linIx)
            self.serEd=ObjectEditor(intr,showType=True,parent=self.scroll,path='woo.master.scene.dem.con[%d,%d]'%(self.ids[0],self.ids[1]))
            self.scroll.setWidget(self.serEd)
            self.gotoId1Button.setText('#'+makeBodyLabel(S.dem.par[self.ids[0]]))
            self.gotoId2Button.setText('#'+makeBodyLabel(S.dem.par[self.ids[1]]))
            self.setWindowTitle('Contact #%d + #%d'%(self.ids[0],self.ids[1]))
        except (IndexError,):
            if self.ids:  # reset view (there was an interaction)
                self.ids=None
                self.serEd=QFrame(self.scroll); self.scroll.setWidget(self.serEd) 
                self.setWindowTitle('No contact')
                self.gotoId1Button.setText(u'#…'); self.gotoId2Button.setText(u'#…');
    def gotoId(self,bodyId):
        if self.bodyLinkCallback: self.bodyLinkCallback(bodyId)
        else: self.bi=BodyInspector(bodyId); self.bi.show()
    def setLinIxSlot(self,linIx):
        S=woo.master.scene
        try:
            C=S.dem.con[linIx]
            self.ids=C.id1,C.id2
            self.setupInteraction()
        except IndexError: pass
    def gotoId1Slot(self): self.gotoId(self.ids[0])
    def gotoId2Slot(self): self.gotoId(self.ids[1])
    def refreshEvent(self):
        S=woo.master.scene
        self.intrLinIxBox.setMaximum(len(S.dem.con)-1)
        # no ids yet -- try getting the first interaction, if it exists
        if not self.ids:
            try:
                i=S.dem.con[0]
                self.ids=i.id1,i.id2
                self.setupInteraction()
                return
            except IndexError: return # no interaction exists at all
        try: # try to fetch the contact we have
            c=S.dem.con[self.ids[0],self.ids[1]]
            self.intrLinIxBox.setValue(c.linIx) # update linIx, it can change asynchronously
        except (IndexError,AttributeError):
            self.ids=None
            self.setupInteraction() # will make it empty
            
class SimulationInspector(QWidget):
    def __init__(self,parent=None):
        S=woo.master.scene
        QWidget.__init__(self,parent)
        self.setWindowTitle("Simulation Inspection")
        self.setWindowIcon(QIcon(":/woo-logo.svg"))
        self.tabWidget=QTabWidget(self)
        demField=S.dem if S.hasDem else None
        self.engineInspector=EngineInspector(parent=None)
        self.bodyInspector=BodyInspector(parent=None,intrLinkCallback=self.changeIntrIds) if demField else None
        self.intrInspector=InteractionInspector(parent=None,bodyLinkCallback=self.changeBodyId) if demField else None
        self.cellInspector=CellInspector(parent=None)
        self.sceneInspector=SceneInspector(parent=None)
        for i,name,widget in [(0,'Engines',self.engineInspector),(1,'Particles',self.bodyInspector),(2,'Contacts',self.intrInspector),(3,'Cell',self.cellInspector),(4,'Scene',self.sceneInspector)]:
            if widget: self.tabWidget.addTab(widget,name)

        # add fields
        for i,f in enumerate(S.fields):
            path='woo.master.scene.fields[%d]'%i
            if S.hasDem and f==S.dem: path='woo.master.scene.dem'
            #if S.hasSparc and f==S.sparc: path='woo.master.scene.sparc'
            self.tabWidget.addTab(ObjectEditor(f,parent=None,path=path,showType=True),'%d. '%i+path)
        grid=QGridLayout(self); grid.setSpacing(0); grid.setMargin(0)
        grid.addWidget(self.tabWidget)
        self.setLayout(grid)
    def changeIntrIds(self,ids):
        self.tabWidget.removeTab(2); self.intrInspector.close()
        self.intrInspector=InteractionInspector(ids=ids,parent=None,bodyLinkCallback=self.changeBodyId)
        self.tabWidget.insertTab(2,self.intrInspector,'Contacts')
        self.tabWidget.setCurrentIndex(2)
    def changeBodyId(self,id):
        self.bodyInspector.changeIdSlot(id)
        self.tabWidget.setCurrentIndex(1)
        
