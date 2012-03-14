#!/usr/bin/python

"""
This class creates a jobs schedule once given an dict with target classes (objects)
as keys and its dependencies (objects) as a set.
The output is a list containing the objects in the onder in which they can be
executed.
Each object MUST have a getStatus function which returns TRUE if class has been
completed or FALSE if it hasn't

TODO:
    - accept more statuses:
        -running
        -failed

#http://code.activestate.com/recipes/577413-topological-sort/
"""
try:
    from functools import reduce
except:
    pass


def toposort2(data):
    """
    Performs a tepological sorting of dependecies taking into consideration
    the status of each object (as completed or not).
    It takes as input a dict containing the desired jobs objects as keys and
    its dependencies objects as value in a set:
    {
        OBJ1: SET(OBJ2, OBJ3)
        OBJ2: SET(OB3)
        OBJ3: SET()
    }
    
    It returns a list in which each element is a list containing the objects that
    can be run:
    [
        [obj3]
        [obj2]
        [obj1]
    ]
    
    Inside each element each object can be run in any particular order.
    
    Objects must have a callable function getStatus in order to check its status
    and not call it in case of completion.
    """

    for k, v in data.items():
        v.discard(k) # Ignore self dependencies
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item:set() for item in extra_items_in_deps})
    resList = []
    while True: # while there are elements in ordered
        selected=[]
        for item,dep in data.items():
            #print "CHECKING ITEM " + str(item)
            if item.getStatus():
                #print "  IGNORING " + str(item) + " DUE TO COMPLETION"
                pass
            else:
                if dep:
                    #print "  HAS DEPENDENCIES"
                    res = True
                    for d in dep:
                        #print "    DEP " + str(d) + " STATUS " + str(d.getStatus())
                        res = res and d.getStatus()

                    if res:
                        #print "    ADDING " + str(item) + ". ALL DEPENDENCIES MET BUT ITEM NOT RUN"
                        selected.append(item)
                    else:
                        #print "    IGNORING " + str(item) + ". NOT ALL DEPENDENCIES MET AND NOT RUN. WAITING FOR NEXT ROUND"
                        pass
                else:
                    #print "    ADDING " + str(item) + " DUE TO NOT CONCLUSION AND NO DEPENDENCIES"
                    selected.append(item)
        ordered=set(selected)
        #ordered = set(item for item,dep in data.items() if not dep)

        if not ordered:
            break

        resList.append(sorted(ordered))

        data = {item: (dep - ordered) for item,dep in data.items()
                if item not in ordered}

    #assert not data, "A cyclic dependency exists amongst %r" % data
    return resList

if __name__ == "__main__":
    data = {
        'des_system_lib':   set('std synopsys std_cell_lib des_system_lib dw02 dw01 ramlib ieee'.split()),
        'dw01':             set('ieee dw01 dware gtech'.split()),
        'dw02':             set('ieee dw02 dware'.split()),
        'dw03':             set('std synopsys dware dw03 dw02 dw01 ieee gtech'.split()),
        'dw04':             set('dw04 ieee dw01 dware gtech'.split()),
        'dw05':             set('dw05 ieee dware'.split()),
        'dw06':             set('dw06 ieee dware'.split()),
        'dw07':             set('ieee dware'.split()),
        'dware':            set('ieee dware'.split()),
        'gtech':            set('ieee gtech'.split()),
        'ramlib':           set('std ieee'.split()),
        'std_cell_lib':     set('ieee std_cell_lib'.split()),
        'synopsys':         set(),
        }

    class obj():
        def __init__(self, name, status):
            self.val    = name
            self.status = status
        def getStatus(self):
            return self.status
        def setStatus(self, status):
            self.status = status
        def __str__(self):
            return self.val
        def __repr__(self):
            return self.val

    f1 = obj('f1', False )
    f2 = obj('f2', False )
    f3 = obj('f3', True  )
    l1 = obj('l1', True  )
    f4 = obj('f4', True  )
    f5 = obj('f5', True  )
    f6 = obj('f6', True  )
    l2 = obj('l2', False )
    d1 = obj('d1', False )


    data = {
        f1: set(),
        f2: set(),
        f3: set(),
        l1: set([f1, f2, f3]),
        f4: set(),
        f5: set(),
        f6: set(),
        l2: set([f4, f5, f6]),
        d1: set([l1, l2]),
        }

    print str(data)

    runCount = 0
    while True:
        runCount += 1
        res = toposort2(data)
        if not res:
            break
        tasks = res[0]
        for task in tasks:
            task.setStatus(True)
        print str(runCount) + " " + str(tasks)
