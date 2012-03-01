#!/usr/bin/python
#http://www.electricmonk.nl/log/2008/08/07/dependency-resolving-algorithm/
#http://code.google.com/p/joblaunch/source/browse/trunk/joblaunch.py

NOT_RUN = 0
RUNNING = 1
FAILED  = 2
FINISH  = 3

PENDING = 4
DFINISH = 5
DFAILED = 6

class Node:
    def __init__(self, name):
        self.name   = name
        self.status = 0
        self.edges  = []
 
    def addEdge(self, node):
        self.edges.append(node)

    def status(self):
        return self.status

    def dependency(self):
        res = None
        for edge in self.edges:
            if   edge.status() == NOT_RUN:
                return PENDING
            elif edge.status() == RUNNING:
                return PENDING
            elif edge.status() == FAILED:
                return DFAILED
            elif edge.status() == FINISH:
                return DFINISH


def dep_resolve_simple(node):
   #print node.name
   for edge in node.edges:
      dep_resolve_simple(edge)
 
def dep_resolve_res1(node, resolved):
   #print node.name
   for edge in node.edges:
      dep_resolve_res1(edge, resolved)
   resolved.append(node)

def dep_resolve_res2(node, resolved):
   #print node.name
   for edge in node.edges:
      if edge not in resolved:
         dep_resolve_res2(edge, resolved)
   resolved.append(node)

def dep_resolve_res3(node, resolved, seen):
   #print node.name
   seen.append(node)
   for edge in node.edges:
      if edge not in resolved:
         if edge in seen:
            raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
         dep_resolve_res3(edge, resolved, seen)
   resolved.append(node)

def dep_resolve_res4(node, resolved, unresolved):
   unresolved.append(node)
   for edge in node.edges:
      if edge not in resolved:
         if edge in unresolved:
            raise Exception('Circular reference detected: %s -> %s' % (node.name, edge.name))
         dep_resolve_res4(edge, resolved, unresolved)
   resolved.append(node)
   unresolved.remove(node)

def dep_resolve(node, resolved, unresolved):
   unresolved.append(node)
   for edge in node.edges:
      if edge not in resolved:
         if edge in unresolved:
            raise Exception('Circular reference detected: %s -> %s' % (node.name, edge.name))
         dep_resolve(edge, resolved, unresolved)
   resolved.append(node)
   unresolved.remove(node)


if __name__ == "__main__":
    f1 = Node('f1')
    f2 = Node('f2')
    f3 = Node('f3')
    l1 = Node('l1')

    f4 = Node('f4')
    f5 = Node('f5')
    f6 = Node('f6')
    l2 = Node('l2')

    d1 = Node('d1')

    #Next, we define the relationships between our nodes:

    l1.addEdge(f1)    # a depends on b
    l1.addEdge(f2)    # a depends on b
    l1.addEdge(f3)    # a depends on b

    l2.addEdge(f4)    # a depends on b
    l2.addEdge(f5)    # a depends on b
    l2.addEdge(f6)    # a depends on b

    d1.addEdge(l1)
    d1.addEdge(l2)

    print "DEP RESOLVE SIMPLE"
    dep_resolve_simple(d1)


    print "DEP RESOLVE 1"
    resolved1 = []
    dep_resolve_res1(d1, resolved1)
    for node in resolved1:
        print node.name,
    print ""

    print "DEP RESOLVE 2"
    resolved2 = []
    dep_resolve_res2(d1, resolved2)
    for node in resolved2:
        print node.name,
    print ""

    
    print "DEP RESOLVE 3"
    resolved3 = []
    dep_resolve_res3(d1, resolved3, [])
    for node in resolved3:
        print node.name,
    print ""

    print "DEP RESOLVE 4"
    resolved4 = []
    dep_resolve_res4(d1, resolved4, [])
    for node in resolved4:
        print node.name,
    print ""

    print "DEP RESOLVE"
    resolved = []
    dep_resolve(d1, resolved, [])
    for node in resolved:
        print node.name,
    print ""

