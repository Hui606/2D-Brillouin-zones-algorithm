import math

Radians75 = math.radians(75)
cos75 = math.cos(Radians75)  # x
sin75 = math.sin(Radians75)  # y

Radians60 = math.radians(60)
cos60 = math.cos(Radians60)  # x
sin60 = math.sin(Radians60)  # y

Radians_n30 = math.radians(-30)
cos_n30 = math.cos(Radians_n30)  # x
sin_n30 = math.sin(Radians_n30)  # y

############################################################# Please ingore the above code

# d_1 = (cos75, sin75)
# d_2 = (cos_n30, sin_n30)

d_1 = (1, 0)  # Follow these directions to add unit cells
d_2 = (0, 1)

base_pt_1 = (0, 0)
base_pt_2 = (0.25, 0)
base_pt_3 = (0, 0.7)
# base_pt_4 = (6, 0)

# The points in a unit cell
base_pt_list = [
    base_pt_1,
    base_pt_2,
    base_pt_3,
    # base_pt_4
]

e1_range, e2_range = 5, 5  # Must be an odd number

START = 1 # start from 1
STOP = 1

image_name = "BZ"

folder_path = '/Users/bumptious/Documents/FYP-CGAL-Project/cgal-bind/examples/python-exa/lhn/Union'

