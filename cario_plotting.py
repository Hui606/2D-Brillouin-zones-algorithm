import cairo
import random
import math
import input


color_list = [
    (0.439216, 0.858824, 0.576471),
    (0.62352, 0.372549, 0.623529),
    (0.647059, 0.164706, 0.164706),
    (0.372549, 0.623529, 0.623529),
    (0.258824, 0.258824, 0.435294),
    (0.556863, 0.137255, 0.419608),
    (0.439216, 0.576471, 0.858824),
    (0.137255, 0.556863, 0.137255),
    (0.8, 0.498039, 0.196078),
    (0.858824, 0.858824, 0.439216),
    (0.576471, 0.858824, 0.439216),
    (0.309804, 0.184314, 0.184314),
    (0.623529, 0.623529, 0.372549),
    (0.74902, 0.847059, 0.847059),
    (0.560784, 0.560784, 0.737255),
    (0.196078, 0.8, 0.196078),
    (0.419608, 0.137255, 0.556863),
    (0.196078, 0.8, 0.6),
    (0.196078, 0.196078, 0.8),
    (0.419608, 0.556863, 0.137255),
    (0.917647, 0.917647, 0.678431),
    (0.576471, 0.439216, 0.858824),
    (0.258824, 0.435294, 0.258824),
    (0.439216, 0.858824, 0.858824),
    (0.858824, 0.439216, 0.576471),
    (0.184314, 0.184314, 0.309804),
    (0.137255, 0.137255, 0.556863),
    (1, 0.5, 0.0),
    (0.858824, 0.439216, 0.858824),
    (0.560784, 0.737255, 0.560784),
    (0.737255, 0.560784, 0.560784),
    (0.917647, 0.678431, 0.917647),
    (0.435294, 0.258824, 0.258824),
    (0.137255, 0.556863, 0.419608),
    (0.556863, 0.419608, 0.137255),
    (0.196078, 0.6, 0.8),
    (0.137255, 0.419608, 0.556863),
    (0.858824, 0.576471, 0.439216),
    (0.847059, 0.74902, 0.847059),
    (0.678431, 0.917647, 0.917647),
    (0.309804, 0.184314, 0.309804),
    (0.8, 0.196078, 0.6),
    (0.847059, 0.847059, 0.74902),
    (0.6, 0.8, 0.196078),
    (0.22, 0.69, 0.87),
    (0.35, 0.35, 0.67),
    (0.71, 0.65, 0.26),
    (0.72, 0.45, 0.20),
    (0.55, 0.47, 0.14),
    (0.65, 0.49, 0.24),
    (0.90, 0.91, 0.98),
    (0.85, 0.85, 0.10),
    (0.81, 0.71, 0.23),
    (0.82, 0.57, 0.46),
    (0.85, 0.85, 0.95),
    (1.00, 0.43, 0.78),
    (0.53, 0.12, 0.47),
    (0.30, 0.30, 1.00),
    (0.85, 0.53, 0.10),
    (0.89, 0.47, 0.20),
    (0.91, 0.76, 0.65),
    (0.65, 0.50, 0.39),
    (0.52, 0.37, 0.26),
    (1.00, 0.11, 0.68),
    (0.42, 0.26, 0.15),
    (0.36, 0.20, 0.09),
    (0.96, 0.80, 0.69),
    (0.92, 0.78, 0.62),
    (0.00, 0.00, 0.61),
    (0.35, 0.16, 0.14),
    (0.36, 0.25, 0.20),
    (0.59, 0.41, 0.31),
    (0.32, 0.49, 0.46),
    (0.29, 0.46, 0.43),
    (0.52, 0.39, 0.39),
    (0.13, 0.37, 0.31),
    (0.55, 0.09, 0.09),

]

class CarioPlotting:

    def __init__(self, ch_height, ch_width, delta_x, delta_y, plot_range):

        self.start, self.stop = plot_range

        scaling = 1.05
        self.window_width = scaling * ch_width
        self.window_height = scaling * ch_height
        window_width = scaling * ch_width
        window_height = scaling * ch_height
        # self.box_x = window_width / 50
        self.box_x = 0
        self.box_y = window_height / 20
        self.box_width, self.box_height = window_width / 20, window_height / 20

        self.column = 6

        # WIDTH = 20
        # HEIGHT = 20
        self.PIXEL_SCALE = 500
        PIXEL_SCALE = 500
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                          int(window_width * PIXEL_SCALE),
                                          int(window_height * PIXEL_SCALE))

        self.surface_color_box = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                                    int((window_width / 20) * self.column * PIXEL_SCALE),
                                                    int(window_height * PIXEL_SCALE))

        self.ctx_color_box = cairo.Context(self.surface_color_box)
        self.ctx_color_box.scale(PIXEL_SCALE, PIXEL_SCALE)
        self.ctx_color_box.set_source_rgb(0.8, 0.8, 1)
        self.ctx_color_box.paint()

        self.ctx = cairo.Context(self.surface)
        self.ctx.scale(PIXEL_SCALE, PIXEL_SCALE)
        # fx = 1
        # fy = -1  # https://www.cairographics.org/cookbook/matrix_transform/
        # mtrx = cairo.Matrix(fx, 0, 0, fy, 0, (self.surface.get_height()/2)*(fy-1))  # (fx,0,0,fy,cx*(1-fx),cy*(fy-1))
        # mtrx = cairo.Matrix(fx, 0, 0, fy, 0, (self.window_width/2)*(fy-1))  # (fx,0,0,fy,cx*(1-fx),cy*(fy-1))
        # mtrx = cairo.Matrix(fx, 0, 0, fy, 0, 0)  # (fx,0,0,fy,cx*(1-fx),cy*(fy-1))


        # self.ctx.transform(mtrx)
        # self.ctx.translate(0,-ch_height)

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.arc(0, (self.surface.get_width()/2), 0.055, 0, 2 * math.pi)
        self.ctx.fill()

        self.ctx.save()
        self.ctx.set_source_rgb(0.8, 0.8, 1)
        self.ctx.paint()
        self.ctx.restore()

        # self.ctx.translate(0, 0)

        trans_x = window_width / 2 - delta_x
        trans_y = window_height / 2 - delta_y
        # print(trans_x,trans_y)
        self.ctx.translate(trans_x, trans_y)

        # self.box_width, self.box_height = window_width/20, window_height/40
        # self.box_x = window_width*18/20
        # self.box_y = self.surface.get_height()/2000
        # self.box_y = -1.5

    def draw_polygon_cario(self, coor_list, color_tuple):
        # https://www.pythoninformer.com/python-libraries/pycairo/drawing-shapes/
        r, g, b = color_tuple

        x, y = coor_list[0]
        self.ctx.move_to(x, y)
        # print(x,y)

        for pt in coor_list[1:]:
            x, y = pt
            self.ctx.line_to(x, y)
            # print(x, y)

        self.ctx.close_path()

        self.ctx.set_source_rgb(r, g, b)
        self.ctx.fill_preserve()

        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.set_line_width(0)
        self.ctx.stroke()

        return

    def draw_point(self, pt):
        # print(",,,,")
        r, g, b = (0, 0, 0)
        x, y = pt

        self.ctx.set_source_rgb(r, g, b)
        self.ctx.arc(x, y, 0.015, 0, 2 * math.pi)
        self.ctx.fill()

        self.ctx.stroke()

    def draw_point_1(self, pt):

        r, g, b = (1, 1, 1)
        x, y = pt

        self.ctx.set_source_rgb(r, g, b)
        self.ctx.arc(x, y, 0.015, 0, 2 * math.pi)
        self.ctx.fill()

        self.ctx.stroke()

    def plot(self, zone_dict,image_name, suffix, point_list):

        for layer_num in zone_dict.keys()[self.start:self.stop]:  # layer_dict.keys()
            self.color_box(layer_num)
            print('\n' + 'Drawing zone: ' + str(layer_num+1))

            ch_list_cur = zone_dict.get(layer_num)  # the ch list current layer
            print('Number of polygons: ' + str(len(ch_list_cur)))

            for ch in ch_list_cur:

                vtx_list = ch.get_vertex_list()
                # print()
                tuple_lst = []
                for vtx in vtx_list:
                    x = vtx.x()
                    y = vtx.y()
                    tuple_lst.append((x, y))

                self.draw_polygon_cario(tuple_lst, color_list[layer_num])

        for pt in point_list:

            self.draw_point(pt)


        self.union(image_name, suffix)

        print("\nDONE\n")

    def color_box(self, layer_num):
        if self.box_y > self.window_height * 17 / 20:
            self.box_y = self.window_height / 20
            self.box_x = self.box_x + 1.5 * self.box_width

        r, g, b = color_list[layer_num]
        # print('box_y',self.box_y)
        self.ctx_color_box.set_source_rgb(r, g, b)
        self.ctx_color_box.rectangle(self.box_x, self.box_y, self.box_width, self.box_height)
        self.ctx_color_box.fill()

        # Drawing code
        self.ctx_color_box.set_source_rgb(r, g, b)
        self.ctx_color_box.set_font_size(0.1)
        self.ctx_color_box.select_font_face("Arial",
                                            cairo.FONT_SLANT_NORMAL,
                                            cairo.FONT_WEIGHT_NORMAL)
        self.ctx_color_box.move_to(self.box_x + self.box_width, self.box_y)
        self.ctx_color_box.show_text(str(layer_num + 1))
        # End of drawing code

        self.box_y = self.box_y + 1.5 * self.box_height

    def union(self,image_name, suffix):
        self.surface_union = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                                int(self.window_width * self.PIXEL_SCALE + int(
                                                    (self.window_width / 20) * self.column * self.PIXEL_SCALE)),
                                                int(self.window_height * self.PIXEL_SCALE))
        self.ctx_union = cairo.Context(self.surface_union)

        self.ctx_union.set_source_surface(self.surface, 0, 0)
        self.ctx_union.paint()

        self.ctx_union.set_source_surface(self.surface_color_box, self.surface.get_width(), 0)
        self.ctx_union.paint()

        self.surface_union.write_to_png(
            input.folder_path+'/' + image_name+'_'+suffix + '.png')
