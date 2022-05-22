import add_outside
import gecco_curve
import numpy as np

#global varialbes
XIND = 0
YIND = 1
outer_list = [0.01, 0.03, 0.06, 0.09, 0.12]
inner_list = [-0.01, -0.03, -0.06, -0.09, -0.12, -0.15, -0.18]

#creating coordinates of a hexagon with side length 1  centred at (0, 0)
hexlen = 1
(hexcoordx, hexcoordy) = (0, 0)
hexagon = gecco_curve.hexagoncoords(hexlen, hexcoordx, hexcoordy)
radius = gecco_curve.distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[1][XIND], hexagon[1][YIND])/2
d = 0
#max outside curve is d=0.147
#max inside curve is d=-0.198

curve = gecco_curve.drawshape3(hexagon)

outer_list_list = []
for input in outer_list:
    outercurve = add_outside.produceouter(curve, input)
    x = np.array(outercurve[XIND])
    y = np.array(outercurve[YIND])
    outer_list_list.append(x)
    outer_list_list.append(y)

inner_list_list = []
for input in inner_list:
    outercurve = add_outside.produceouter(curve, input)
    x = np.array(outercurve[XIND])
    y = np.array(outercurve[YIND])
    inner_list_list.append(x)
    inner_list_list.append(y)

data_outer = np.column_stack(outer_list_list)
data_inner = np.column_stack(inner_list_list)

datafile_path = "outer_curve_data.txt"
np.savetxt(datafile_path , data_outer, fmt=['%10.5f','%10.5f', '%10.5f', '%10.5f', '%10.5f', '%10.5f','%10.5f', '%10.5f', '%10.5f', '%10.5f'])

datafile_path = "inner_curve_data.txt"
np.savetxt(datafile_path , data_inner, fmt=['%10.5f','%10.5f', '%10.5f', '%10.5f', '%10.5f', '%10.5f','%10.5f', '%10.5f', '%10.5f', '%10.5f','%10.5f', '%10.5f', '%10.5f', '%10.5f'])