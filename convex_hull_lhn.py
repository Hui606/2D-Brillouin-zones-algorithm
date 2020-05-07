import CGAL
from CGAL.CGAL_Kernel import Point_2, Line_2, Polygon_2, Segment_2, Polygon_2
from CGAL import CGAL_Convex_hull_2, CGAL_Kernel
from itertools import cycle


class ConvexHullLhn:

    def __init__(self, exm_pnt_lst):

        self.edge_list = []
        self.pnt_list = []
        self.edge_set_list = []  # [{pt1, pt2}, {pt2, pt3}, {pt3, pt4}, ...]
        self.polygon = None
        self.level = None

        self.edges(exm_pnt_lst)  # Note this line must be at the bottom of __init__

    def edges(self, exm_pnt_lst):

        #  generates the counterclockwise sequence of extreme points of the points in the hull

        CGAL_Convex_hull_2.ch_akl_toussaint(exm_pnt_lst, self.pnt_list)

        self.polygon = Polygon_2(self.pnt_list)

        lst_cycle = cycle(self.pnt_list)
        next_elem = next(lst_cycle)

        for i in range(len(self.pnt_list)):
            this_elem, next_elem = next_elem, next(lst_cycle)
            self.edge_list.append(Segment_2(this_elem, next_elem))

            pt_set = {(round(this_elem.x(), 13), round(this_elem.y(), 13)),
                      (round(next_elem.x(), 13), round(next_elem.y(), 13))}  # The two vertexes making up an edge
            self.edge_set_list.append(pt_set)

    def get_edge_list(self):
        return self.edge_list

    def get_vertex_list(self):
        return self.pnt_list  # counterclockwise order

    def get_edge_set_list(self):
        return self.edge_set_list

    def get_polygon(self):
        # Need to use the function of polygon: bounded_side() to check if the point is in the polygon
        return self.polygon

    def get_zone_level(self):
        return self.level

    def set_zone_level(self,num):
        self.level = num
