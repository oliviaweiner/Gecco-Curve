import unittest
import gecco_curve
import add_outside
import math

class MyTest(unittest.TestCase):

    #test distance function
    def test_distance(self):
        self.assertEqual(gecco_curve.distance(31, 20, 31, 100), 80)
        self.assertEqual(gecco_curve.distance(-6, -10, -2, -7), 5)
        self.assertEqual(gecco_curve.distance(-0.5, -3.75, 5.5, 4.25), 10)
    
    #test hexagoncoords function
    def test_hexagoncoords(self):
        self.assertEqual(len(gecco_curve.hexagoncoords(1, 2, 3)), 6)
        self.assertEqual(gecco_curve.distance(gecco_curve.hexagoncoords(1, 2, 3)[0][0], gecco_curve.hexagoncoords(1, 2, 3)[0][1],  
            gecco_curve.hexagoncoords(1, 2, 3)[1][0], gecco_curve.hexagoncoords(1, 2, 3)[1][1]),  gecco_curve.distance(gecco_curve.hexagoncoords(1, 2, 3)[4][0],  
            gecco_curve.hexagoncoords(1, 2, 3)[4][1], gecco_curve.hexagoncoords(1, 2, 3)[5][0], gecco_curve.hexagoncoords(1, 2, 3)[5][1]))

    #test circlecoordinates function
    def test_circlecoordinates(self):
        self.assertAlmostEqual(gecco_curve.distance(  
            gecco_curve.circlecoordinates(1, 1, 1)[0][250],  
            gecco_curve.circlecoordinates(1, 1, 1)[1][250],  
            gecco_curve.circlecoordinates(1, 1, 1)[0][0],  
            gecco_curve.circlecoordinates(1, 1, 1)[1][0]  
            ), 2)
    
    #test closestcoordinateindex function
    def test_closestcoordinateindex(self):
        self.assertEqual(gecco_curve.closestcoordinateindex(31, 134, [1, 2, 32452, 35], [1, 2, 32452, 35]), 3)

    #test closestcoordinatesindexes function
    def test_closestcoordinatesindexes(self):
        self.assertEqual(gecco_curve.closestcoordinatesindexes([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [5, 5, 5, 5], [1, 1, 1, 1]), (3, 0))

    #test criticalcirclepoints function
    def test_criticalcirclepoints(self):
        testhex = gecco_curve.hexagoncoords(1, 2, 3)
        self.assertEqual(gecco_curve.criticalcirclepoints(testhex, 1), [(0, 417), (83, 0), (334, 417), (417, 0), (0, 83), (83, 166)])

    #test hexagoncirclelist function
    def test_hexagoncirclelist(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        output = gecco_curve.hexagoncirclelist(testhex, 1)
        self.assertEqual(len(output), 7)
        self.assertEqual(abs(output[3][0][250] - output[3][0][0]), 2)

    #test addpoints function
    def test_addpoints(self):
        output = gecco_curve.addpoints([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1], 2, 4)
        self.assertEqual(output, ([3, 4, 5], [4, 3, 2]))

    #test drawshape function by checking that curve is smooth by assessing gradient
    def test_drawshape(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        output = gecco_curve.drawshape(testhex, 1)
        prevgrad = None
        for i in range(len(output)-1):
            grad = (output[1][i+1] - output[1][i])/(output[1][i+1] - output[1][i])
            if prevgrad != None:
                self.assertAlmostEqual(prevgrad, grad)
            prevgrad = grad
    
    #test drawshape2 function by checking that curve is smooth by assessing gradient
    def test_drawshape2(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        output = gecco_curve.drawshape2(testhex)
        prevgrad = None
        for i in range(len(output)-1):
            grad = (output[1][i+1] - output[1][i])/(output[1][i+1] - output[1][i])
            if prevgrad is not None:
                self.assertAlmostEqual(prevgrad, grad)
            prevgrad = grad
        
    #test curveportion function
    def test_curveportion(self):
        curve = gecco_curve.curveportion((1, 3), ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]), -1)
        self.assertEqual(curve, ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]))

    #test generatecurve function
    def test_generatecurve(self):
        curve = gecco_curve.generatecurve(([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]), -10, 5)
        newcurve =  ([-9, -8, -7, -6, -5], [6, 7, 8, 9, 10])
        self.assertEqual(curve, newcurve)
    
    #test drawshape3 function
    def test_drawshape3(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        output = gecco_curve.drawshape3(testhex)
        prevgrad = None
        for i in range(len(output)-1):
            grad = (output[1][i+1] - output[1][i])/(output[1][i+1] - output[1][i])
            if prevgrad != None:
                self.assertAlmostEqual(prevgrad, grad)
            prevgrad = grad

    #test none of iterations are empth lists
    def test_nonempth(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        output1 = gecco_curve.drawshape(testhex, 1)
        output2 = gecco_curve.drawshape2(testhex)
        output3 = gecco_curve.drawshape3(testhex)
        outputs = [output1, output2, output3]
        for output in outputs:
            self.assertIsNotNone(output)
            self.assertIsNot(output, ())
            self.assertIsNot(output, ([], []))

    #test iter3 inside curve function
    def test_drawshape3_outer(self):
        testhex = gecco_curve.hexagoncoords(1, 1, 1)
        iter3 = gecco_curve.drawshape3(testhex)
        innercoords = add_outside.produceouter(iter3, 1)
        prevgrad = None
        for i in range(len(innercoords)-1):
            grad = (innercoords[1][i+1] - innercoords[1][i])/(innercoords[1][i+1] - innercoords[1][i])
            if prevgrad != None:
                self.assertAlmostEqual(prevgrad, grad)
            prevgrad = grad

if __name__ == '__main__':
    unittest.main()