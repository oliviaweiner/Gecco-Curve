import gecco_curve
import math
import matplotlib.pyplot as plt
import numpy as np
import argparse


XIND = 0
YIND = 1

# This function inputs two sets of adjascent coordinates and outputs their perpendicular direction vector
def perpendicular(x_1, y_1, x_2, y_2):
    x_direc = x_2 - x_1
    y_direc = y_2 - y_1
    if(x_direc == 0):
        if y_2 > y_1:
            return (1, 0)
        else:
            return (-1, 0)
    if(y_direc == 0):
        if x_2 > x_1: 
            return (0, -1)
        else:
            return (0, 1)
    m = y_direc / x_direc
    m_perpendicular = - 1 / m

    if y_2 > y_1:
        return (1/(1 + m_perpendicular**2)**(1/2), m_perpendicular/(1 + m_perpendicular**2)**(1/2))
    else:
        return (-1/(1 + m_perpendicular**2)**(1/2), - m_perpendicular/(1 + m_perpendicular**2)**(1/2))

# This function inputs two sets of adjascent coordinates on the middle shell and the 'd' value and outputs the coordinates of the inner shell
def outercoordinate(x_1, y_1, x_2, y_2, d):
    (direction_x, direction_y) = perpendicular(x_1, y_1, x_2, y_2)
    return [x_1 + d * direction_x, y_1 + d * direction_y]

# This function inputs two sets of adjascent coordinates on the middle shell and the 'd' value and outputs the coordinates of the outer shell
def innercoordinate(x_1, y_1, x_2, y_2, d):
    (direction_x, direction_y) = perpendicular(x_1, y_1, x_2, y_2)
    return [x_1 - d * direction_x, y_1 - d * direction_y]

def produceinner(curve, d):
    innercoordinatesx = []
    innercoordinatesy = []
    for i in range(len(curve[0])-1):
        coord = innercoordinate(curve[0][i], curve[1][i], curve[0][i+1], curve[1][i+1], d)
        innercoordinatesx.append(coord[0])
        innercoordinatesy.append(coord[1])
    return (innercoordinatesx, innercoordinatesy)

def produceouter(curve, d):
    outercoordinatesx = []
    outercoordinatesy = []
    for i in range(len(curve[0])-1):
        coord = outercoordinate(curve[0][i], curve[1][i], curve[0][i+1], curve[1][i+1], d)
        if i > 1:
            length = len(outercoordinatesx) - 1
            if gecco_curve.distance(coord[0], coord[1], outercoordinatesx[length], outercoordinatesy[length]) < 100 * gecco_curve.distance(outercoordinatesx[length - 1], outercoordinatesy[length - 1], outercoordinatesx[length], outercoordinatesy[length]):
                outercoordinatesx.append(coord[0])
                outercoordinatesy.append(coord[1])
        else:
            outercoordinatesx.append(coord[0])
            outercoordinatesy.append(coord[1])
    return (outercoordinatesx, outercoordinatesy)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('iter_type', help="type of iter"
        "Options: iter1, iter2, iter3.",
        choices=["iter1", "iter2", "iter3"])
    args = argp.parse_args()

    #creating coordinates of a hexagon with side length 1  centred at (0, 0)
    hexlen = 1
    (hexcoordx, hexcoordy) = (0, 0)
    hexagon = gecco_curve.hexagoncoords(hexlen, hexcoordx, hexcoordy)
    radius = gecco_curve.distance(hexagon[0][XIND], hexagon[0][YIND], hexagon[1][XIND], hexagon[1][YIND])/2
    d = 0
    #max outside curve is d=0.147
    #max inside curve is d=-0.198

    if args.iter_type == 'iter1':
        curve = gecco_curve.drawshape(hexagon, radius)
        innercurve = produceinner(curve, d)
        outercurve = produceouter(curve, d)
        x = np.array(innercurve[XIND])
        y = np.array(innercurve[YIND])
    if args.iter_type == 'iter2':
        curve = gecco_curve.drawshape2(hexagon)
        innercurve = produceinner(curve, d)
        outercurve = produceouter(curve, d)
        x = np.array(innercurve[XIND])
        y = np.array(innercurve[YIND])
    if args.iter_type == 'iter3':
        curve = gecco_curve.drawshape3(hexagon)
        outercurve = produceouter(curve, d)
        x = np.array(outercurve[XIND])
        y = np.array(outercurve[YIND])
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'o', color='black')
    plt.show()