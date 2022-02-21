import math
import matplotlib.pyplot as plt
import numpy as np

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
    RADIUS = distance(hexagon[0][0], hexagon[0][1], hexagon[1][0], hexagon[1][1])/2
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
    xind = 0
    yind = 1
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


#function that inputs coordinates of hexagon and outputs coordinates of third gecco iteration
def drawshape3(hex):
    iter2 = drawshape2(hexagon)
    LEN2 = len(iter2[0])

    xind = 0
    yind = 1

    #weights represent weighted positions where centre iter2 of gecco curve meets other copies
    weights = [(2/21 + i/3, 3/21 + i/3) for i in range(3)]
    centreshape = iter2
    centre_parts = {'upper': curveportion(weights[0], centreshape, 2), 'left': curveportion(weights[1], centreshape, 2), 'right': curveportion(weights[2], centreshape, 2)}
    for word in centre_parts:
        globals()[word + 'x'] = centre_parts[word][xind]
        globals()[word + 'y'] = centre_parts[word][yind]

    #weights represent weighted positions where iter1 connectives gecco curve meet
    iter1weights = [(0 + i/3, 1/9 + i/3) for i in range(3)] 
    iter1 = drawshape(hex, RADIUS)
    iter1_parts = {'right': curveportion(iter1weights[0], iter1, 1), 'left': curveportion(iter1weights[1], iter1, 1), 'bottom': curveportion(iter1weights[2], iter1, 1)}
    for word in iter1_parts:
        globals()['iter1' + word + 'x'] = iter1_parts[word][xind]
        globals()['iter1' + word + 'y'] = iter1_parts[word][yind]
    
    iter2weights = [(((3 + i * 7) % 21)/21, ((9 + i * 7) % 21)/21) for i in range(3)]
    iter2 = centreshape
    iter2_parts = {'left': curveportion(iter2weights[0], iter2, 1), 'bottom': curveportion(iter2weights[1], iter2, 1), 'right': curveportion(iter2weights[2], iter2, -1)}



    for word in iter2_parts:
        globals()['iter2' + word + 'x'] = iter2_parts[word][xind]
        globals()['iter2' + word + 'y'] = iter2_parts[word][yind]


    YSHIFT = hex[1][1] - hex[0][1]
    XSHIFT = hex[2][0] - hex[4][0]

    iter1curvey1 = [y - YSHIFT for y in iter1bottomy]
    iter1curvex1 = [x + 2 * XSHIFT for x in iter1bottomx]

    iter2curvey2 = [y - 4 * YSHIFT for y in uppery]
    iter2curvex2 = [x + 2 * XSHIFT for x in upperx]

    iter1curvey3 = [y - YSHIFT for y in iter1righty]
    iter1curvex3 = [x + 2 * XSHIFT for x in iter1rightx]

    iter2curvey4 = [y + YSHIFT for y in lefty]
    iter2curvex4 = [x + 3 * XSHIFT for x in leftx]

    iter1curvey5 = [y - YSHIFT for y in iter1lefty]
    iter1curvex5 = [x + 2 * XSHIFT for x in iter1leftx]

    iter1curvey6 = [y + 3 * YSHIFT for y in iter1righty]
    iter1curvex6 = [x + 0 * XSHIFT for x in iter1rightx]

    iter2curvey7 = [y + 5 * YSHIFT for y in lefty]
    iter2curvex7 = [x + 1 * XSHIFT for x in leftx]

    iter1curvey8 = [y + 3 * YSHIFT for y in iter1lefty]
    iter1curvex8 = [x + 0 * XSHIFT for x in iter1leftx]

    iter2curvey9 = [y + 4 * YSHIFT for y in righty]
    iter2curvex9 = [x - 2 * XSHIFT for x in rightx]

    iter1curvey10 = [y + 3 * YSHIFT for y in iter1bottomy]
    iter1curvex10 = [x + 0 * XSHIFT for x in iter1bottomx]

    iter1curvey11 = [y - 2 * YSHIFT for y in iter1lefty]
    iter1curvex11 = [x - 1 * XSHIFT for x in iter1leftx]

    iter2curvey12 = [y - 1 * YSHIFT for y in righty]
    iter2curvex12 = [x - 3 * XSHIFT for x in rightx]

    iter1curvey13 = [y - 2 * YSHIFT for y in iter1bottomy]
    iter1curvex13 = [x - 1 * XSHIFT for x in iter1bottomx]

    iter2curvey14 = [y - 5 * YSHIFT for y in uppery]
    iter2curvex14 = [x - 1 * XSHIFT for x in upperx]

    iter1curvey15 = [y - 2 * YSHIFT for y in iter1righty]
    iter1curvex15 = [x - 1 * XSHIFT for x in iter1rightx]

    return (iter2bottomx + iter1curvex1 + iter2curvex2 + iter1curvex3 + iter2curvex4 + iter1curvex5 + iter2rightx + iter1curvex6 + iter2curvex7 + iter1curvex8 + iter2curvex9 + iter1curvex10 + iter2leftx + iter1curvex11 + iter2curvex12 + iter1curvex13 + iter2curvex14 + iter1curvex15 + iter2bottomx, iter2bottomy + iter1curvey1 + iter2curvey2 + iter1curvey3 + iter2curvey4 + iter1curvey5 + iter2righty + iter1curvey6 + iter2curvey7 + iter1curvey8 + iter2curvey9 + iter1curvey10 + iter2lefty + iter1curvey11 + iter2curvey12 + iter1curvey13 + iter2curvey14 + iter1curvey15 + iter2bottomy)

#creating coordinates of a hexagon with side length 1 centred at (0, 0)
HEXLEN = 1
(HEXCOORDX, HEXCOORDY) = (0, 0)
hexagon = hexagonCoords(HEXLEN, HEXCOORDX, HEXCOORDY)
RADIUS = distance(hexagon[0][0], hexagon[0][1], hexagon[1][0], hexagon[1][1])/2
l = len(drawshape2(hexagon)[0])

#call drawshape on hexagon to create iter-1 gecco curve and plot x- and y-coordinates in matplotlib
x = np.array(drawshape3(hexagon)[0])
y = np.array(drawshape3(hexagon)[1]) 
#x = np.concatenate((x[int(25*len(x)/9):], x[:int(2*len(x)/3)]))
#y = np.concatenate((y[int(25*len(y)/9):], y[:int(2*len(y)/3)]))
plt.style.use('seaborn-whitegrid')
plt.plot(x, y, 'o', color='black')
plt.show()

