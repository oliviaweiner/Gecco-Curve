import math
import matplotlib.pyplot as plt
import numpy as np
import argparse

#global variables that will be used throughout code
xind = 0
yind = 1

#function that inputs 2 sets of coordinates and outputs the distance between them
def distance(x_1, y_1, x_2, y_2):
    return ((x_1 - x_2)**2 + (y_1 - y_2)**2)**(1/2)

#function that inputs hexagon length and coordinates and outputs coordinates of a hexagon with 
#side length equal to length, centred at input coordinates, starting at lower right going anti-clockwise
def hexagonCoords(length, x, y):
    hexagon = [(length/2, -(3)**(1/2)*length/2), (length,0), (length/2, (3)**(1/2)*length/2), \
              (-length/2, (3)**(1/2)*length/2), (-length, 0), (-length/2, -(3)**(1/2)*length/2)]
    hexagon = [(x + x_coord, y + y_coord) for (x_coord, y_coord) in hexagon]
    return hexagon

#function inputs coordinates and radius sizem and outputs coordinates of a circle starting at
#rightmost point going anticlockwise
def circlecoordinates(x, y, r):
    xlist = []
    ylist = []
    for i in range(500):
        xlist.append(math.cos(2*math.pi*i/500)*r+x)
        ylist.append(math.sin(2*math.pi*i/500)*r+y)
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
def criticalcirclepoints(hex, r):
    altered_hex = hex.copy()
    altered_hex.append(hex[0])
    list = []
    for i in range(len(altered_hex) - 1):
        criticalpoint = closestcoordinatesindexes(circlecoordinates(altered_hex[i][0], altered_hex[i][1], r)[0], circlecoordinates(altered_hex[i][0], altered_hex[i][1], r)[1], circlecoordinates(altered_hex[i+1][0], altered_hex[i+1][1], r)[0], circlecoordinates(altered_hex[i+1][0], altered_hex[i+1][1], r)[1])
        list.append(criticalpoint)
    return list

#function inputs hexagon coordinates and outputs a list of lists of circle coordinates centred at each
#hexagon coordinate
def hexagoncirclelist(hex, r):
    list = []
    altered_hex = hex.copy()
    altered_hex.append(hex[0])
    for i in range(len(altered_hex)):
        list.append(circlecoordinates(altered_hex[i][0], altered_hex[i][1], r))
    return list

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
        critical_start = criticals[i][1]
        critical_end = criticals[i+1][0]
        circle_x = circlelist[i+1][0]
        circle_y = circlelist[i+1][1]
        if (i % 2) == 0:
            circle_x.reverse()
            circle_y.reverse()
            critical_start = len(circle_x) - critical_start
            critical_end = len(circle_x) - critical_end
        x_list += addpoints(circle_x, circle_y, critical_start, critical_end)[0]
        y_list += addpoints(circle_x, circle_y, critical_start, critical_end)[1]
    return (x_list, y_list)

#function that inputs coordinates of hexagon and outputs coordinates of second gecco iteration
def drawshape2(hex):
    RADIUS = distance(hex[0][0], hex[0][1], hex[1][0], hex[1][1])/2
    iter1 = drawshape(hex, RADIUS)
    LEN = len(drawshape(hex, RADIUS)[0])

    horizontalx = iter1[0][int(LEN*2/3):] + iter1[0][:int(LEN*4/9)]
    horizontaly = iter1[1][int(LEN*2/3):] + iter1[1][:int(LEN*4/9)]
    upperx = iter1[0][int(LEN*1/3):] + iter1[0][:int(LEN*1/9)]
    uppery = iter1[1][int(LEN*1/3):] + iter1[1][:int(LEN*1/9)]
    lowerx = iter1[0][:int(LEN*7/9)]
    lowery = iter1[1][:int(LEN*7/9)]
    SHIFT = distance(hex[0][0], hex[0][1], hex[2][0], hex[2][1])
    HSHIFT = hex[1][0] - hex[3][0]

    horizontalx = [x + HSHIFT for x in horizontalx]
    uppery = [y - SHIFT / 2 for y in uppery]
    lowery = [y + SHIFT / 2 for y in lowery]

    return (lowerx + upperx + horizontalx, lowery + uppery + horizontaly)

#function inputs weighted curve critical points, curves, and indicator, and outputs curve in indicator
#n. of parts added up of curve, cut off at weight proportionate critical points of curve
def curveportion(weights, curve, indicator):
    curvelen = len(curve[0])
    weight1 = weights[0]
    weight2 = weights[1]
    if indicator == 1:
        x_curve = curve[xind][int(curvelen*weight1): int(curvelen*weight2)]
        y_curve = curve[yind][int(curvelen*weight1): int(curvelen*weight2)]
    if indicator == 2:
        x_curve = curve[xind][:int(curvelen*weight1)] + curve[xind][int(curvelen*weight2):]
        y_curve = curve[yind][:int(curvelen*weight1)] + curve[yind][int(curvelen*weight2):]
    if indicator == -1:
        x_curve = curve[xind][int(curvelen*weight1):] + curve[xind][:int(curvelen*weight2)]
        y_curve = curve[yind][int(curvelen*weight1):] + curve[yind][:int(curvelen*weight2)]
    return (x_curve, y_curve)

#inputs curve coordinates and amount it should be shifted in each direction and outputs shifted curve
def generatecurve(curve, x_shift, y_shift):
        newx = [x + x_shift for x in curve[xind]]
        newy = [y + y_shift for y in curve[yind]]
        return (newx, newy)

#function that inputs coordinates of hexagon and outputs coordinates of third gecco iteration
def drawshape3(hex):
    iter2 = drawshape2(hex)

    #weights represent weighted positions where centre iter2 of gecco curve meets other copies
    weights = [(2/21 + i/3, 3/21 + i/3) for i in range(3)]
    centreshape = iter2
    centre_parts = {'upper': curveportion(weights[0], centreshape, 2), 'left': curveportion(weights[1], centreshape, 2), 'right': curveportion(weights[2], centreshape, 2)}
    for word in centre_parts:
        globals()[word + 'x'] = centre_parts[word][xind]
        globals()[word + 'y'] = centre_parts[word][yind]
        globals()[word] = centre_parts[word]
    RADIUS = distance(hex[0][0], hex[0][1], hex[1][0], hex[1][1])/2

    #weights represent weighted positions where iter1 connectives gecco curve meet
    iter1weights = [(0 + i/3, 1/9 + i/3) for i in range(3)] 
    iter1 = drawshape(hex, RADIUS)
    iter1_parts = {'right': curveportion(iter1weights[0], iter1, 1), 'left': curveportion(iter1weights[1], iter1, 1), 'bottom': curveportion(iter1weights[2], iter1, 1)}
    for word in iter1_parts:
        globals()['iter1' + word + 'x'] = iter1_parts[word][xind]
        globals()['iter1' + word + 'y'] = iter1_parts[word][yind]
        globals()['iter1' + word] = iter1_parts[word]
    
    #weights represent weighted positions where iter2 connectives gecco curve meet
    iter2weights = [(((3 + i * 7) % 21)/21, ((9 + i * 7) % 21)/21) for i in range(3)]
    iter2 = centreshape
    iter2_parts = {'left': curveportion(iter2weights[0], iter2, 1), 'bottom': curveportion(iter2weights[1], iter2, 1), 'right': curveportion(iter2weights[2], iter2, -1)}
    for word in iter2_parts:
        globals()['iter2' + word + 'x'] = iter2_parts[word][xind]
        globals()['iter2' + word + 'y'] = iter2_parts[word][yind]
        globals()['iter2' + word] = iter2_parts[word]


    YSHIFT = hex[1][1] - hex[0][1]
    XSHIFT = hex[2][0] - hex[4][0]

    #This list specifies the shift index and curve type that each step in our third iteration gecco
    #curve will be comprised of
    order_list = [(iter2bottom, 0, 0), (iter1bottom, 2, -1), (upper, 2, -4), (iter1right, 2, -1), (left, 3, 1), \
                (iter1left, 2, -1), (iter2right, 0, 0), (iter1right, 0, 3), (left, 1, 5), (iter1left, 0, 3), (right, -2, 4), \
                (iter1bottom, 0, 3), (iter2left, 0, 0), (iter1left, -1, -2), (right, -3, -1), (iter1bottom, -1, -2), \
                (upper, -1, -5), (iter1right, -1, -2), (iter2bottom, 0, 0)]

    x_curve = []
    y_curve = []
    for i, triple in enumerate(order_list):
            curve = generatecurve(triple[0], triple[1] * XSHIFT, triple[2] * YSHIFT)
            x_curve += curve[xind]
            y_curve += curve[yind]

    return (x_curve, y_curve)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('iter_type', help="type of iter"
        "Options: iter1, iter2, iter3.",
        choices=["iter1", "iter2", "iter3"])
    args = argp.parse_args()

    #creating coordinates of a hexagon with side length 1 centred at (0, 0)
    HEXLEN = 1
    (HEXCOORDX, HEXCOORDY) = (0, 0)
    hexagon = hexagonCoords(HEXLEN, HEXCOORDX, HEXCOORDY)
    RADIUS = distance(hexagon[0][0], hexagon[0][1], hexagon[1][0], hexagon[1][1])/2

    if args.iter_type == 'iter1':
        x = np.array(drawshape(hexagon, RADIUS)[0])
        y = np.array(drawshape(hexagon, RADIUS)[1])
    if args.iter_type == 'iter2':
        x = np.array(drawshape2(hexagon)[0])
        y = np.array(drawshape2(hexagon)[1]) 
    if args.iter_type == 'iter3':
        x = np.array(drawshape3(hexagon)[0])
        y = np.array(drawshape3(hexagon)[1]) 
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'o', color='black')
    plt.show()