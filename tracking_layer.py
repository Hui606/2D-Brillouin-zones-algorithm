from __future__ import print_function
import CGAL
from CGAL.CGAL_Kernel import Point_2, Line_2, Segment_2, Polygon_2
from CGAL import CGAL_Convex_hull_2, CGAL_Kernel
from convex_hull_lhn import ConvexHullLhn
import numpy as np
import pyvista as pv
import cairo
import math
from itertools import product
import input
from cario_plotting import CarioPlotting


def closest_node(node, nodes):
    # It should be a function that compute the distance between each point and the center at once
    # and store them in a list, then use a getter to retrieve the layer from it. I will work on this later
    # https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    min_value = min(dist_2)
    indexes = [i for i, x in enumerate(dist_2) if x == min_value]
    return indexes  # get the index of the closest points


def get_bisector(point_1, point_2):
    mid_point = Point_2((point_1.x() + point_2.x()) / 2, (point_1.y() + point_2.y()) / 2)
    line = Line_2(point_1, point_2)
    bisector = line.perpendicular(mid_point)  # 1. calculate the bisector
    return bisector


def get_intersection(ch_obj, bisector):
    # Next we find the intersection point of the biggest convex hull with the bisector

    intersection_pt_lst = []
    for edge in ch_obj.get_edge_list():
        intersection_obj = CGAL_Kernel.intersection(edge, bisector)
        if not intersection_obj.empty():
            if intersection_obj.is_Segment_2():
                print("Intersection is a segemnt")
                pass
                
            else:
                m = intersection_obj.get_Point_2()

            isExistent = False
            if len(intersection_pt_lst) > 0:
                # print('m ', m, 'len(intersection_pt_lst):', len(intersection_pt_lst))
                for pt in intersection_pt_lst:
                    # print('pt:', pt)
                    seg = Segment_2(m, pt)
                    seg_len = seg.squared_length()
                    # print('seg_len: ', seg_len)

                    if 0.0000000001 > seg_len >= 0:
                        # new_val = remove_exponent(seg_len)
                        # print('isExistent')
                        isExistent = True

            if isExistent is False:
                intersection_pt_lst.append(m)  # Add the intersection point to the list

 

    return intersection_pt_lst


def divide_the_polygon(ch_obj, bisector):
    # Next we find the intersection point of the biggest convex hull with the bisector
    intersection_pt_lst = get_intersection(ch_obj, bisector)
    neg_vertex_lst = []
    pos_vertex_lst = []

    center_ans = bisector.oriented_side(center)
    parent_level = ch_obj.get_zone_level()
    if parent_level is None:
        parent_level = 0
    pos_lv_up = 0
    neg_lv_up = 0
    is_pos_side = False
    is_same_side = False

    pos_side_counter = 0
    neg_side_counter = 0

    if len(intersection_pt_lst) > 1:
        # Divide the extreme points to negative and positive side
        pos_lst = []
        neg_lst = []
        # Oriented side: http://www.cs.rpi.edu/courses/spring02/robotic/CGAL-2.3/doc_html/kernel/Chapter_kernel_geometry.html
        for pt in ch_obj.get_vertex_list():
            # ans = 1 left side=neg side=down side; ans = 0 collinear; ans = -1  right side=pos side=upper side
            ans = bisector.oriented_side(pt)
            if ans == 1:

                pos_lst.append(pt)
            elif ans == -1:

                neg_lst.append(pt)


        neg_vertex_lst = intersection_pt_lst + neg_lst  # Get the vertex of the new convex hull
        pos_vertex_lst = intersection_pt_lst + pos_lst

        if center_ans == 1:
            # At the same side with pos_lst
            neg_lv_up = 1
        elif center_ans == -1:
            # At the same side with neg_lst
            pos_lv_up = 1

        pos_lv = pos_lv_up + parent_level
        neg_lv = neg_lv_up + parent_level

        # Make the polygons
        pos_ch = ConvexHullLhn(pos_vertex_lst)
        neg_ch = ConvexHullLhn(neg_vertex_lst)

        pos_ch.set_zone_level(pos_lv)
        neg_ch.set_zone_level(neg_lv)

        return [pos_ch, neg_ch]  # Notice the first is positive, then it is negative

    # if len(intersection_pt_lst) <= 1
    else:

        for pt in ch_obj.get_vertex_list():
            
            # if isSame is False:
            # ans = 1 left side=neg side=down side; ans = 0 collinear; ans = -1  right side=pos side=upper side
            ans = bisector.oriented_side(pt)
            if ans == 1:
                # pos_lst.append(pt)
                pos_side_counter = pos_side_counter + 1
            elif ans == -1:
                # neg_lst.append(pt)
                neg_side_counter = neg_side_counter + 1
            

        if pos_side_counter >= 2:  # It means that polygon at positive side
            is_pos_side = True
        elif neg_side_counter >= 2:
            is_pos_side = False

        if is_pos_side is True and center_ans == 1:
            is_same_side = True
        elif is_pos_side is False and center_ans == 1:
            is_same_side = False
        elif is_pos_side is True and center_ans == -1:
            is_same_side = False
        elif is_pos_side is False and center_ans == -1:
            is_same_side = True

        res_ch = ch_obj  # Copy the big one

        if is_same_side:
            res_ch.set_zone_level(parent_level)
        else:
            res_ch.set_zone_level(parent_level + 1)

        return [res_ch]


def divide_and_replace(bisector_line):
    global ch_list
    copy_list = ch_list[:]


    pos_vertex_lst, neg_vertex_lst = [], []

    for ch_big in ch_list:

        divided_list = divide_the_polygon(ch_big, bisector_line)

        if len(divided_list) == 1:
            copy_list.remove(ch_big)
            copy_list.append(divided_list[0])


        elif len(divided_list) == 2:

            pos_ch = divided_list[0]
            neg_ch = divided_list[1]

            copy_list.remove(ch_big)
            copy_list.append(pos_ch)
            copy_list.append(neg_ch)

    ch_list = copy_list[:]


def get_closest_point():
    global pnt_obj_list
    global point_list

    idx_lst = closest_node((center_x, center_y), point_list)
    pt_lst = []
    for i in idx_lst:
        pt_lst.append(pnt_obj_list[i])

    a_list, b_list = [], []

    for i in idx_lst:
        a_list.append(pnt_obj_list[i])
        b_list.append(point_list[i])

    for a in a_list:
        pnt_obj_list.remove(a)

    for b in b_list:
        point_list.remove(b)

    return pt_lst


def get_closest_pt_dict():
    pt_dict = {}
    layer = 0
    while len(pnt_obj_list) > 0:
        pt_dict[layer] = get_closest_point()
        layer += 1

    return pt_dict


def get_plotting_vtx(vertex_lst):
    leftmost, rightmost, top, bottom = Point_2(), Point_2(), Point_2(), Point_2()
    CGAL_Convex_hull_2.ch_n_point(vertex_lst, top)  # maximal y coordinate.
    CGAL_Convex_hull_2.ch_e_point(vertex_lst, rightmost)  # maximal x coordinate.
    CGAL_Convex_hull_2.ch_s_point(vertex_lst, bottom)  # minimal y coordinates
    CGAL_Convex_hull_2.ch_w_point(vertex_lst, leftmost)  # minimal x coordinate

    lt, rt = leftmost.x(), rightmost.x()
    tp, btm = top.y(), bottom.y()

    draw_pt_list = []
    for pair in product([lt, rt], [tp, btm]):
        draw_pt_list.append(pair)

    # left_btm_x, left_btm_y= draw_pt_list[1]

    delta_x = (lt + rt) / 2 - 0
    delta_y = (tp + btm) / 2 - 0

    ch_height = tp - btm
    ch_width = rt - lt

    return ch_height, ch_width, delta_x, delta_y


def start_algo(base_pt_list, d_1, d_2, e1_range, e2_range, START, STOP,image_name, center_idx):

    # Initialize
    global center, center_x, center_y

    c_1 = (e1_range - 1) / 2
    c_2 = (e2_range - 1) / 2

    for base in base_pt_list:
        
        for e_1 in range(0, e1_range, 1):

            v_1 = np.dot(d_1, e_1)

            for e_2 in range(0, e2_range, 1):
                v_2 = np.dot(d_2, e_2)

                if e_1 == c_1 and e_2 == c_2 and base_pt_list.index(base) == center_idx:  # all points but center
                    pt = np.add(base, (v_1 + v_2))

                    center_x, center_y = tuple(pt.tolist())
                    
                else:

                    pt = np.add(base, (v_1 + v_2))

                    x, y = tuple(pt.tolist())
                    point_list.append((x, y))
                    pnt_obj_list.append(Point_2(x, y))
                    # print(x, y)

    point_list_bkup = point_list+[(center_x,center_y)]

    center = Point_2(center_x, center_y)
    vertex_lst = []
    CGAL_Convex_hull_2.convex_hull_2(pnt_obj_list,
                                     vertex_lst)  # This function returns a list of all points of the hull

    ch_lhn = ConvexHullLhn(vertex_lst)  # To get the list of edges
    ch_list.append(ch_lhn)  # The first convex hull is added to the list

    cloest_pt_dict = get_closest_pt_dict()

    # Dividing, replacing and tracking
    for layer in cloest_pt_dict.keys()[:]:
        print('Find the ' + str(layer+1) + '-closest points to center')
        clost_pt_lst = cloest_pt_dict.get(layer)  # Get the list of points of this layer

        # This loop handle the first layer
        for closest_pt in clost_pt_lst:  # range(len(closest_pnt_idx))
            
            bisector_line = get_bisector(center, closest_pt)
            divide_and_replace(bisector_line)

    print("\nDividing, replacing and tracking done.")

    zone_dict = {}
    for ch in ch_list:
        level = ch.get_zone_level()
        if zone_dict.get(level) is None:
            zone_dict[level] = [ch]
        else:
            zone_dict.get(level).append(ch)


    print('\nHOW MANY POLYGONS: ', len(ch_list))
    print('HOW MANY ZONES: ', len(zone_dict.keys()))

 

    def get_plotter(start=0, stop=0):
        plot_range = ()

        if not start < stop:
            plot_range = (0, len(zone_dict.keys()))  # Plot all
            ch_height, ch_width, delta_x, delta_y = get_plotting_vtx(vertex_lst)
            cplot = CarioPlotting(ch_height, ch_width, delta_x, delta_y, plot_range)
        else:
            plot_range = (start, stop)

            # zone_level = stop - 1  # The most external zone plotted

            pt_lst = []
            vtx_lst = []
            for level in range(start, stop):
                for ch in zone_dict.get(level):
                    pt_lst += ch.get_vertex_list()  # all points belong to the most external zone

            CGAL_Convex_hull_2.convex_hull_2(pt_lst,
                                             vtx_lst)

            ch_height, ch_width, delta_x, delta_y = get_plotting_vtx(vtx_lst)
            cplot = CarioPlotting(ch_height, ch_width, delta_x, delta_y, plot_range)

        return cplot

    plotter = get_plotter(START, STOP)

    plotter.plot(zone_dict, image_name, 'center_'+str((center.x(),center.y())), point_list_bkup)

    del pnt_obj_list[:]
    del point_list[:]
    del ch_list[:]


ch_list = []
pnt_obj_list = []
point_list = []
center = None
center_x = None
center_y = None


class Algo:

    def __init__(self, base_pt_list, d_1, d_2, e1_range, e2_range, START, STOP, image_name):
        for center_idx in range(len(base_pt_list)):
            print('********************* Start with center',base_pt_list[center_idx],'**********************\n')
            start_algo(base_pt_list, d_1, d_2, e1_range, e2_range, START, STOP, image_name, center_idx)


d_1 = input.d_1
d_2 = input.d_2
base_pt_list = input.base_pt_list
e1_range, e2_range = input.e1_range, input.e2_range  # Must be an odd number
START = input.START-1
STOP = input.STOP-1
image_name = input.image_name
ag = Algo(base_pt_list, d_1, d_2, e1_range, e2_range, START, STOP,image_name)
