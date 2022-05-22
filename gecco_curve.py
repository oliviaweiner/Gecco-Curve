import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

#index that x- and y- coordinates will be stored at
XIND = 0
YIND = 1

#number of iterations in each half circle
ITERCIRCLE = 500

#precomputed variables for third iteration curve

#weights represent weighted positions of where gecco curve parts meets other parts
weights = { 'connectives': [(0 + i/3, 1/9 + i/3) for i in range(3)], 
            'centre': [(2/21 + i/3, 3/21 + i/3) for i in range(3)], 
            'edges': [(((3 + i * 7) % 21)/21, ((9 + i * 7) % 21)/21) for i in range(3)]}

#precalculated ordering and instruction for the pieces that iter3 consists of in (weights, iter number, curveportion indicator) format
order_list = [(weights['edges'][1], 2, 1), (weights['connectives'][2], 1, 1), (weights
               ['centre'][0], 2, 2), (weights['connectives'][0], 1, 1), (weights['centre'][1], 2, 2), (weights['connectives'][1], 1, 1), (weights['edges'][2], 2, -1), (weights['connectives'][0], 1, 1), (weights['centre'][1], 2, 2), (weights['connectives'][1], 1, 1), (weights['centre'][2], 2, 2), (weights['connectives'][2], 1, 1), (weights['edges'][0], 2, 1), (weights[ 'connectives'][1], 1, 1), (weights['centre'][2], 2, 2), (weights['connectives'][2], 1, 1), (weights['centre'][0], 2, 2), (weights['connectives'][0], 1, 1), (weights[ 'edges'][1], 2, 1)]

#precalculated amounts third iteration curve pieces should be shifted
shift_list = [(0, 0), (2, -1), (2, -4), (2, -1), (3, 1), 
                (2, -1), (0, 0), (0, 3), (1, 5), (0, 3), (-2, 4), 
                (0, 3), (0, 0), (-1, -2), (-3, -1), (-1, -2), 
                (-1, -5), (-1, -2), (0, 0)]


#function that inputs 2 sets of coordinates and outputs the distance between them
def distance(x_1, y_1, x_2, y_2):
    return ((x_1 - x_2)**2 + (y_1 - y_2)**2)**(1/2)

#function that inputs hexagon length and coordinates and outputs coordinates of a hexagon with 
#side length equal to length,  'centre'd at input coordinates, starting at lower right going anti-clockwise
def hexagoncoords(length, x, y):
    hexagon = [(length/2, -(3)**(1/2)*length/2), (length,0), (length/2, (3)**(1/2)*length/2), 
              (-length/2, (3)**(1/2)*length/2), (-length, 0), (-length/2, -(3)**(1/2)*length/2)]
    hexagon = [(x + x_coord, y + y_coord) for (x_coord, y_coord) in hexagon]
    return hexagon

#function inputs coordinates and radius sizem and outputs coordinates of a circle starting at
#rightmost point going anticlockwise
def circlecoordinates(x, y, r):
    xlist = []
    ylist = []
    for i in range(ITERCIRCLE):
        xlist.append(math.cos(2*math.pi*i/ITERCIRCLE)*r+x)
        ylist.append(math.sin(2*math.pi*i/ITERCIRCLE)*r+y)
    return (xlist, ylist)

#function inputs coordintes (x_1, y_1) and two lists of x- and y- coordinates, outputs list coordinates
#closest to (x_1, y_1)
def closestcoordinateindex(x_1, y_1, x_list, y_list):
    minimum = 2**30
    index = 0
    for c in range(len(x_list)):
        distance = (x_1 - x_list[c])**2 + (y_1 - y_list[c])**2
        if minimum > distance:
            minimum = distance
            index = c
    return index

#function inputs two sets of lists of coordinates and outputs indexes of closest coordinates of each set
def closestcoordinatesindexes(x_list1, y_list1, x_list2, y_list2):
    minimum = 2**30
    c1_min = 0
    c2_min = 0
    for c1 in range(len(x_list1)):
        for c2 in range(len(x_list2)):
            distance = (x_list1[c1] - x_list2[c2])**2 + (y_list1[c1] - y_list2[c2])**2
            if distance < minimum:
                c1_min = c1
                c2_min = c2
                minimum = distance
    return (c1_min, c2_min)

#function inputs hexagon coordinates and outputs list of hexagon gecco curve critical point coordinates
def criticalcirclepoints(hexagon, r):
    altered_hex = hexagon.copy()
    altered_hex.append(hexagon[0])
    lst = []
    for i in range(len(altered_hex) - 1):
        criticalpoint = closestcoordinatesindexes(circlecoordinates(altered_hex[i][XIND], altered_hex[i][YIND], r)[XIND], circlecoordinates(altered_hex[i][XIND], altered_hex[i][YIND], r)[YIND], circlecoordinates(altered_hex[i+1][XIND], altered_hex[i+1][YIND], r)[XIND], circlecoordinates(altered_hex[i+1][XIND], altered_hex[i+1][YIND], r)[YIND])
        lst.append(criticalpoint)
    return lst

#function inputs hexagon coordinates and outputs a list of lists of circle coordinates  'centre'd at each
#hexagon coordinate
def hexagoncirclelist(hexagon, r):
    lst = []
    altered_hex = hexagon.copy()
    altered_hex.append(hexagon[0])
    for i in range(len(altered_hex)):
        lst.append(circlecoordinates(altered_hex[i][XIND], altered_hex[i][YIND], r))
    return lst

#function inputs coordinates of a circle and indexes of critical start and end point, and outputs coordinates 
#of portion of circle starting and ending at index start and end point
def addpoints(circle_x, circle_y, critical_start, critical_end):
    j = critical_start
    appendlist_x = []
    appendlist_y = []
    for i in range(len(circle_x)):
        if j == critical_end + 1:
            break
        if j == len(circle_x):
            if j == critical_end:
                break
            j = 0
        appendlist_x.append(circle_x[j])
        appendlist_y.append(circle_y[j])
        j += 1
    return (appendlist_x, appendlist_y)

#function inputs coordinates of hexagon and outputs coorinates of its first iteration gecco curve
def drawshape(hexagon, r):
    x_list = []
    y_list = []
    criticals = criticalcirclepoints(hexagon, r)
    criticals.append(criticals[0])
    circlelist = hexagoncirclelist(hexagon, r)
    circlelist.append(circlelist[0])
    for i in range(len(criticals)-1):
        critical_start = criticals[i][YIND]
        critical_end = criticals[i+1][XIND]
        circle_x = circlelist[i+1][XIND]
        circle_y = circlelist[i+1][YIND]
        if (i % 2) == 0:
            circle_x.reverse()
            circle_y.reverse()
            critical_start = len(circle_x) - critical_start
            critical_end = len(circle_x) - critical_end
<<<<<<< HEAD
        x_add = addpoints(circle_x, circle_y, critical_start, critical_end)[XIND]
        y_add = addpoints(circle_x, circle_y, critical_start, critical_end)[YIND]
        x_list += x_add[1:len(x_add)-1]
        y_list += y_add[1:len(x_add)-1]

=======
        x_list += addpoints(circle_x, circle_y, critical_start, critical_end)[XIND]
        y_list += addpoints(circle_x, circle_y, critical_start, critical_end)[YIND]
>>>>>>> eb96dfa6e7c52bdad839f2ea4d5bcba5385efd63
    return (x_list, y_list)

#function that inputs coordinates of hexagon and outputs coordinates of second gecco iteration
def drawshape2(hexagon):
    radius = distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[1][XIND], hexagon[1][YIND])/2
    iter1 = drawshape(hexagon, radius)
    n_coordinates = len(drawshape(hexagon, radius)[XIND])

    horizontalx = iter1[XIND][int(n_coordinates*2/3):] + iter1[XIND][:int(n_coordinates*4/9)]
    horizontaly = iter1[YIND][int(n_coordinates*2/3):] + iter1[YIND][:int(n_coordinates*4/9)]
    upperx = iter1[XIND][int(n_coordinates*1/3):] + iter1[XIND][:int(n_coordinates*1/9)]
    uppery = iter1[YIND][int(n_coordinates*1/3):] + iter1[YIND][:int(n_coordinates*1/9)]
    lowerx = iter1[XIND][:int(n_coordinates*7/9)]
    lowery = iter1[YIND][:int(n_coordinates*7/9)]
    SHIFT = distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[2][XIND], hexagon[2][YIND])
    HSHIFT = hexagon[1][XIND] - hexagon[3][XIND]

    horizontalx = [x + HSHIFT for x in horizontalx]
    uppery = [y - SHIFT / 2 for y in uppery]
    lowery = [y + SHIFT / 2 for y in lowery]

<<<<<<< HEAD
    upperx = upperx[1:len(uppery)]
    uppery = uppery[1:len(uppery)]

    returnx = lowerx + upperx + horizontalx
    returny = lowery + uppery + horizontaly

    return (returnx, returny)
=======
    return (lowerx + upperx + horizontalx, lowery + uppery + horizontaly)
>>>>>>> eb96dfa6e7c52bdad839f2ea4d5bcba5385efd63

#function inputs weighted curve critical points, curves, and indicator, and outputs curve in indicator
#n. of parts added up of curve, cut off at weight proportionate critical points of curve
def curveportion(weights, curve, indicator):
    curvelen = len(curve[XIND])
    weight1 = weights[XIND]
    weight2 = weights[YIND]
    if indicator == 1:
<<<<<<< HEAD
        x_curve = curve[XIND][int(curvelen*weight1): int(curvelen*weight2)-2]
        y_curve = curve[YIND][int(curvelen*weight1): int(curvelen*weight2)-2]
    if indicator == 2:
        x_curve = curve[XIND][int(curvelen*weight2):] + curve[XIND][:int(curvelen*weight1)-2]
        y_curve = curve[YIND][int(curvelen*weight2):] + curve[YIND][:int(curvelen*weight1)-2] 
=======
        x_curve = curve[XIND][int(curvelen*weight1): int(curvelen*weight2)]
        y_curve = curve[YIND][int(curvelen*weight1): int(curvelen*weight2)]
    if indicator == 2:
        x_curve = curve[XIND][:int(curvelen*weight1)] + curve[XIND][int(curvelen*weight2):]
        y_curve = curve[YIND][:int(curvelen*weight1)] + curve[YIND][int(curvelen*weight2):]
>>>>>>> eb96dfa6e7c52bdad839f2ea4d5bcba5385efd63
    if indicator == -1:
        x_curve = curve[XIND][int(curvelen*weight1):] + curve[XIND][:int(curvelen*weight2)]
        y_curve = curve[YIND][int(curvelen*weight1):] + curve[YIND][:int(curvelen*weight2)]
    return (x_curve, y_curve)

#inputs curve coordinates and amount it should be shifted in each direction and outputs shifted curve
def generatecurve(curve, x_shift, y_shift):
        newx = [x + x_shift for x in curve[XIND]]
        newy = [y + y_shift for y in curve[YIND]]
        return (newx, newy)

#function that inputs coordinates of hexagon and outputs coordinates of third gecco iteration
def drawshape3(hexagon):
    iter2 = drawshape2(hexagon)
    radius = distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[1][XIND], hexagon[1][YIND])/2
    iter1 = drawshape(hexagon, radius)

    yshift = hexagon[1][YIND] - hexagon[0][YIND]
    xshift = hexagon[2][XIND] - hexagon[4][XIND]

    x_curve = []
    y_curve = []
    for i in range(len(order_list)):
        if order_list[i][1] == 2:
            shape = iter2
        else:
            shape = iter1
        portion = curveportion(order_list[i][0], shape, order_list[i][2])
        curve = generatecurve(portion, shift_list[i][0] * xshift, shift_list[i][1] * yshift)
<<<<<<< HEAD
        
        x_add = curve[XIND]
        y_add = curve[YIND]
        x_curve += x_add
        y_curve += y_add
=======
        x_curve += curve[XIND]
        y_curve += curve[YIND]
>>>>>>> eb96dfa6e7c52bdad839f2ea4d5bcba5385efd63

    return (x_curve, y_curve)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('iter_type', help="type of iter"
        "Options: iter1, iter2, iter3.",
        choices=["iter1", "iter2", "iter3"])
    args = argp.parse_args()

    #creating coordinates of a hexagon with side length 1  centred at (0, 0)
    hexlen = 1
    (hexcoordx, hexcoordy) = (0, 0)
    hexagon = hexagoncoords(hexlen, hexcoordx, hexcoordy)
    radius = distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[1][XIND], hexagon[1][YIND])/2

    if args.iter_type == 'iter1':
        x = np.array(drawshape(hexagon, radius)[XIND])
        y = np.array(drawshape(hexagon, radius)[YIND])
    if args.iter_type == 'iter2':
        x = np.array(drawshape2(hexagon)[XIND])
        y = np.array(drawshape2(hexagon)[YIND]) 
    if args.iter_type == 'iter3':
        x = np.array(drawshape3(hexagon)[XIND])
        y = np.array(drawshape3(hexagon)[YIND]) 
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'o', color='black')
    plt.show()