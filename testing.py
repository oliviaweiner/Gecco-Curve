import unittest

from click import get_current_context
import gecco_curve
import math

class MyTest(unittest.TestCase):

    #test distance function
    def test_distance(self):
        self.assertEqual(gecco_curve.distance(31, 20, 31, 100), 80)
        self.assertEqual(gecco_curve.distance(-6, -10, -2, -7), 5)
        self.assertEqual(gecco_curve.distance(-0.5, -3.75, 5.5, 4.25), 10)
    
    #test hexagonCoords function
    def test_hexagonCoords(self):
        self.assertEqual(len(gecco_curve.hexagonCoords(1, 2, 3)), 6)
        self.assertEqual(gecco_curve.distance(gecco_curve.hexagonCoords(1, 2, 3)[0][0], gecco_curve.hexagonCoords(1, 2, 3)[0][1], \
            gecco_curve.hexagonCoords(1, 2, 3)[1][0], gecco_curve.hexagonCoords(1, 2, 3)[1][1]),  gecco_curve.distance(gecco_curve.hexagonCoords(1, 2, 3)[4][0], \
            gecco_curve.hexagonCoords(1, 2, 3)[4][1], gecco_curve.hexagonCoords(1, 2, 3)[5][0], gecco_curve.hexagonCoords(1, 2, 3)[5][1]))

    #test circlecoordinates function
    def test_circlecoordinates(self):
        self.assertAlmostEqual(gecco_curve.distance( \
            gecco_curve.circlecoordinates(1, 1, 1)[0][250], \
            gecco_curve.circlecoordinates(1, 1, 1)[1][250], \
            gecco_curve.circlecoordinates(1, 1, 1)[0][0], \
            gecco_curve.circlecoordinates(1, 1, 1)[1][0] \
            ), 2)
    
    #test closestcoordinateindex function
    def test_closestcoordinateindex(self):
        self.assertEqual(gecco_curve.closestcoordinateindex(31, 134, [1, 2, 32452, 35], [1, 2, 32452, 35]), 3)

    #test closestcoordinatesindexes function
    def test_closestcoordinatesindexes(self):
        self.assertEqual(gecco_curve.closestcoordinatesindexes([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [5, 5, 5, 5], [1, 1, 1, 1]), (3, 0))

    #test criticalcirclepoints function
    def test_criticalcirclepoints(self):
        testhex = gecco_curve.hexagonCoords(1, 2, 3)
        self.assertEqual(gecco_curve.criticalcirclepoints(testhex, 1), [(0, 417), (83, 0), (334, 417), (417, 0), (0, 83), (83, 166)])

    #test hexagoncirclelist function
    def test_hexagoncirclelist(self):
        testhex = gecco_curve.hexagonCoords(1, 1, 1)
        output = gecco_curve.hexagoncirclelist(testhex, 1)
        self.assertEqual(len(output), 7)
        self.assertEqual(abs(output[3][0][250] - output[3][0][0]), 2)

    #test addpoints function
    def test_addpoints(self):
        output = gecco_curve.addpoints([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], 2, 4)
        self.assertEqual(output, ([3, 4, 5], [4, 3, 2]))

    #test drawshape function
    def test_drawshape(self):
        testhex = gecco_curve.hexagonCoords(1, 1, 1)
        output = gecco_curve.drawshape(testhex, 1)
        
        

    

if __name__ == '__main__':
    unittest.main()
