# encoding: utf-8
# 2008 © Václav Šmilauer <eudoxos@arcig.cz>
"""Functions for accessing timing information stored in engines and functors.

See `timing section <https://yade-dem.org/doc/current/prog.html#timing>`_ of the Yade manual, `wiki page <http://yade-dem.org/index.php/Speed_profiling_using_TimingInfo_and_TimingDeltas_classes>`_ for some examples.

"""

from woo.core import *
from woo.dem import *


def _resetEngine(e):
    if e.timingDeltas: e.timingDeltas.reset()
    if isinstance(e,Functor): return
    if isinstance(e,Dispatcher):
        for f in e.functors: _resetEngine(f)
    elif isinstance(e,ParallelEngine):
        for s in e.slaves: _resetEngine(s)
    e.execTime,e.execCount=0,0

def reset():
    "Zero all timing data."
    import woo
    S=woo.master.scene
    for e in S.engines: _resetEngine(e)

_statCols={'label':38,'count':20,'time':20,'relTime':20}
_maxLev=3

def _formatLine(label,time,count,threads,totalTime,level,count2=-1):
    sp,negSp=' '*level*2,' '*(_maxLev-level)*2
    raw=[]
    raw.append(label)
    raw.append((str(count)+(' [/%d]'%threads if threads>1 else '')) if count>=0 else '')
    if count2>=0: raw[-1]='(%d) %s'%(count2,raw[-1]) # for nFullRuns for some colliders
    raw.append(('%.1f'%(time/1000000.)) if time>=0 else '')
    raw.append(('%6.2f'%(time*100./totalTime)) if totalTime>0 else '')
    #raw.append('[%2.1f]'%(time*100./totalTime/threads) if totalTime>0 and threads>1 else '')
    return u' '.join([
        (sp+raw[0]).ljust(_statCols['label']),
        (raw[1]+negSp).rjust(_statCols['count']),
        (raw[2]+negSp).rjust(_statCols['time']),
        (raw[3]+negSp).rjust(_statCols['relTime']),
        #raw[4]
    ])

def _delta_stats(deltas,totalTime,level):
    ret=0
    deltaTime=sum([d[1] for d in deltas.data])
    for d in deltas.data:
        print _formatLine(d[0],d[1],d[2],d[3],totalTime,level); ret+=1
    if len(deltas.data)>1:
        print _formatLine('TOTAL',deltaTime,-1,-1,totalTime,level); ret+=1
    return ret

def _engines_stats(engines,totalTime,level):
    lines=0; hereLines=0
    for e in engines:
        if not isinstance(e,Functor): print _formatLine(u'"'+e.label+'"' if e.label else e.__class__.__name__,e.execTime,e.execCount,-1,totalTime,level,count2=(e.nFullRuns if hasattr(e,'nFullRuns') else -1)); lines+=1; hereLines+=1
        if e.timingDeltas: 
            if isinstance(e,Functor):
                print _formatLine(e.__class__.__name__,-1,-1,-1,-1,level); lines+=1; hereLines+=1
                execTime=sum([d[1] for d in e.timingDeltas.data])
            else: execTime=e.execTime
            lines+=_delta_stats(e.timingDeltas,execTime,level+1)
        if isinstance(e,Dispatcher): lines+=_engines_stats(e.functors,e.execTime,level+1)
        if isinstance(e,ContactLoop):
            lines+=_engines_stats(e.geoDisp.functors,e.execTime,level+1)
            lines+=_engines_stats(e.phyDisp.functors,e.execTime,level+1)
            lines+=_engines_stats(e.lawDisp.functors,e.execTime,level+1)
        elif isinstance(e,ParallelEngine): lines+=_engines_stats(e.slave,e.execTime,level+1)
    if hereLines>1:
        print _formatLine('TOTAL',totalTime,-1,-1,totalTime,level); lines+=1
    return lines

def stats():
    """Print summary table of timing information from engines and functors. Absolute times as well as percentages are given. Sample output:

    .. code-block:: none

        Name                                     Count                 Time        Rel. time
        ------------------------------------------------------------------------------------
        ForceResetter                        400               9449μs            0.01%      
        BoundingVolumeMetaEngine             400            1171770μs            1.15%      
        PersistentSAPCollider                400            9433093μs            9.24%      
        InteractionGeometryMetaEngine        400           15177607μs           14.87%      
        InteractionPhysicsMetaEngine         400            9518738μs            9.33%      
        ConstitutiveLawDispatcher            400           64810867μs           63.49%      
          ef2_Spheres_Brefcom_BrefcomLaw                                                    
             setup                            4926145            7649131μs           15.25%  
             geom                             4926145           23216292μs           46.28%  
             material                         4926145            8595686μs           17.14%  
             rest                             4926145           10700007μs           21.33%  
             TOTAL                                              50161117μs          100.00%  
        "damper"                             400            1866816μs            1.83%      
        "strainer"                           400              21589μs            0.02%      
        "plotDataCollector"                  160              64284μs            0.06%      
        "damageChecker"                        9               3272μs            0.00%      
        TOTAL                                             102077490μs          100.00%      

    """
    import woo
    S=woo.master.scene
    print 'Name'.ljust(_statCols['label'])+' '+'Count'.rjust(_statCols['count'])+' '+'Time [ms]'.rjust(_statCols['time'])+' '+'Rel. time [%]'.rjust(_statCols['relTime'])
    print '-'*(sum([_statCols[k] for k in _statCols])+len(_statCols)-1)
    _engines_stats(S.engines,sum([e.execTime for e in S.engines]),0)
    print
