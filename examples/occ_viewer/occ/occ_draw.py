'''
Created on Sep 30, 2016

@author: jrmarti3
'''
from atom.api import (
   Typed
)

from .draw import (
    ProxyPoint, ProxyVertex, ProxyLine, ProxyCircle, ProxyEllipse, 
    ProxyHyperbola, ProxyParabola, ProxyEdge, ProxyWire
)

from .occ_shape import OccShape

from OCC.gp import gp_Pnt, gp_Lin, gp_Circ, gp_Elips, gp_Hypr, gp_Parab
from OCC.TopoDS import TopoDS_Vertex
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,\
    BRepBuilderAPI_MakeVertex
from OCC.gce import gce_MakeLin

class OccPoint(OccShape, ProxyPoint):
    #: A reference to the toolkit shape created by the proxy.
    shape = Typed(gp_Pnt)
    
    def create_shape(self):
        d = self.declaration
        self.shape = gp_Pnt(d.x,d.y,d.z)
        
    def set_x(self, x):
        self.create_shape()
        
    def set_y(self, y):
        self.create_shape()    
        
    def set_z(self, z):
        self.create_shape()
        
class OccVertex(OccShape, ProxyVertex):
    #: A reference to the toolkit shape created by the proxy.
    shape = Typed(TopoDS_Vertex)
    
    def create_shape(self):
        d = self.declaration
        v = BRepBuilderAPI_MakeVertex(gp_Pnt(d.x,d.y,d.z))
        self.shape = v.Vertex()
        
    def set_x(self, x):
        self.create_shape()
        
    def set_y(self, y):
        self.create_shape()    
        
    def set_z(self, z):
        self.create_shape()
    
        
class OccEdge(OccShape, ProxyEdge):
    shape = Typed(BRepBuilderAPI_MakeEdge)
    
    def make_edge(self,*args):
        self.shape = BRepBuilderAPI_MakeEdge(*args)

class OccLine(OccEdge, ProxyLine):
    
    def create_shape(self):
        pass
    
    def init_layout(self):
        self.update_shape()
    
    def update_shape(self):
        d = self.declaration
        if len(d.children)==2:
            points = [c.shape for c in self.children()]
            shape = gce_MakeLin(points[0],points[1]).Value()
        else:
            shape = gp_Lin(d.axis)
        self.make_edge(shape)
    
    def child_added(self, child):
        super(OccLine, self).child_added(child)
        if not isinstance(child, (OccPoint, OccVertex)):
            raise TypeError("Line can only have Points or Vertices as children")
        self.create_shape()
        
    def child_removed(self, child):
        super(OccLine, self).child_removed(child)
        self.create_shape()

class OccCircle(OccEdge, ProxyCircle):
    def create_shape(self):
        d = self.declaration
        self.make_edge(gp_Circ(d.axis,d.radius))
        
    def set_radius(self, r):
        self.create_shape()

class OccEllipse(OccEdge, ProxyEllipse):
    
    def create_shape(self):
        d = self.declaration
        self.make_edge(gp_Elips(d.axis,d.major_radius,d.minor_radius))
        
    def set_major_radius(self, r):
        self.create_shape()
        
    def set_minor_radius(self, r):
        self.create_shape()
        
class OccHyperbola(OccEdge, ProxyHyperbola):
    
    def create_shape(self):
        d = self.declaration
        self.make_edge(gp_Hypr(d.axis,d.major_radius,d.minor_radius))
        
    def set_major_radius(self, r):
        self.create_shape()
        
    def set_minor_radius(self, r):
        self.create_shape()
        
class OccParabola(OccEdge, ProxyParabola):
    
    def create_shape(self):
        d = self.declaration
        self.make_edge(gp_Parab(d.axis,d.focal_length))
        
    def set_focal_length(self, l):
        self.create_shape()
    

        
class OccWire(OccShape, ProxyWire):
    shape = Typed(BRepBuilderAPI_MakeWire)
    
    def create_shape(self):
        pass
    
    def init_layout(self):
        self.update_shape()
    
    def update_shape(self):
        d = self.declaration
        shape = BRepBuilderAPI_MakeWire()
        for c in self.children():
            shape.Add(c.shape.Edge())
        assert shape.IsDone(), 'Edges must be connected'
        self.shape = shape
        
    def child_added(self, child):
        super(OccWire, self).child_added(child)
        self.create_shape()
        
    def child_removed(self, child):
        super(OccWire, self).child_removed(child)
        self.create_shape()
        