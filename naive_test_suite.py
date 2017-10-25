from convexhull import clockwiseSort
#from convexhull import naiveHull2 as naiveHull
from convexhull import naiveHull
import unittest
import random

# Test suite for naive implementation of convex hull
class TestNaiveHull(unittest.TestCase):
    def test_single(self):
        points = [(100,100)]
        hull = naiveHull(points)
        self.assertEqual(points , hull)

    # tests 100 randomly generated non colinear pair of points
    def test_two_points(self):
        for i in range(100):
            x1 = 0
            y1 = 0
            x2 = 0        
            y2 = 0
            while x1 == x2:
                x1 = random.randint(100,900)
                x2 = random.randint(100, 900) 
            while y1 == y2:
                y1 = random.randint(100,600)
                y2 = random.randint(100, 600)
            points = [(x1,y1) , (x2,y2)]
            hull = naiveHull(points)
            clockwiseSort(points)
            self.assertEqual(points, hull)

    # tests two points that are the same point
    def test_two_same_points(self):
        points = [(100, 100) , (100,100)]
        hull = naiveHull(points) 
        self.assertEqual(hull , [(100,100)])

    # tests 3 points, none colinear
    def test_three_points(self):
        counter = 0
        valueList = [0] * 6
        # populate value list with 6 unique integers
        while counter < 6:
            num = random.randint(100, 600)
            if num not in valueList:
                valueList[counter] = num
                counter = counter + 1
        # turn valueList into a list of 3 unique, noncolinear point
        points = [(valueList[0] , valueList[1]) , (valueList[2] , valueList[3]) , (valueList[4] , valueList[5])]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # tests 3 points in a horizonal line
    def test_horizonal_line_three(self):
        points = [(100,100), (200,100), (300,100)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test 3 points in a vertical line
    def test_vertical_line_three(self):
        points = [(100,100), (100,200), (100,300)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # tests 3 points, two of which are the same point
    def test_three_two_same(self):
        points = [(100,100), (100,100), (100,300)]
        hull = naiveHull(points)
        realHull = [(100, 100) , (100,300)]
        clockwiseSort(realHull)
        self.assertEqual(realHull, hull)


    # test 3 points, two of which are colinear 
    def test_three_two_colin(self):
        points = [(100,200), (300,200), (200,100)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test 4 points in a line (horizontal)
    def test_four_horiz_line(self):
        points = [(100,200), (200,100), (300,100) , (400,100)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test 4 points in a vertical line
    def test_four_vert_line(self):
        points = [(100,200), (100,100), (100,300) , (100,400)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test a triangle with a point in the exact center
    def test_triangle_point_center(self):
        points = [(100,200), (300,200) , (200, 150), (200,100)]
        hull = naiveHull(points)
        hullActual = [(100,200) , (300,200), (200,100)]
        clockwiseSort(hullActual)
        self.assertEqual(hullActual, hull)

    # test 4 point square
    def test_square(self):
        points = [(100,100), (200,100) , (100, 200), (200,200)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test 4 point square with point in center
    def test_square_with_center_point(self):
        points = [(100,100), (200,100) ,(150,150), (100, 200), (200,200)]
        hull = naiveHull(points)
        hullActual =[(100,100), (200,100) , (100, 200), (200,200)]
        clockwiseSort(hullActual)
        self.assertEqual(hullActual, hull)


    # test 4 points, 3 of which are colinear
    def test_four_three_colin(self):
        points = [(100,100), (100,200) , (100, 300), (200,200)]
        hull = naiveHull(points)
        clockwiseSort(points)
        self.assertEqual(points, hull)

    # test 6 points, 4 of which are on the hull and 2 of which are in the center and the same point
    def test_square_duplicate_point_center(self):
        points = [(100,100), (200,100) , (150,150) , (100, 200), (200,200), (150, 150)]
        hull = naiveHull(points)
        hullActual = [(100,100), (200,100) , (100, 200), (200,200)]
        clockwiseSort(hullActual)
        self.assertEqual(hullActual, hull)

    # test 6 points, 4 of which are the hull, 2 of which are internal, but not the same point
    def test_square_with_multiple_nondupe_central(self):
        points = [(100,100), (200,100) , (150,150) , (100, 200), (200,200), (155, 170)]
        hull = naiveHull(points)
        hullActual = [(100,100), (200,100) , (100, 200), (200,200)]
        clockwiseSort(hullActual)
        self.assertEqual(hullActual, hull)


    # test 5 points, 4 of which are colinear and of those 2 of which are the same point
    def test_colin_duplicate_triangle(self):
        points = [(100,100), (100,200) , (100, 300), (200,200), (100, 200)]
        hull = naiveHull(points)
        hullActual =[(100,100), (100,200) , (100, 300), (200,200)]
        clockwiseSort(hullActual)
        self.assertEqual(hullActual, hull)

    # generates numerous points in the confines of a house shaped hull, tests
    def test_500_points(self):
        hullActual = [(450,100) , (100,200) , (100,600) , (900, 200) , (900,600)]
        clockwiseSort(hullActual)
        points = []
        for i in range(500):
            x = random.randint(101 , 899)
            y = random.randint(201, 599)
            points.append((x,y))
        # now we need to insert the actual hull values into the point list
        for i in range(5):
            points.insert((i+1) * 50 , hullActual[i])
        hull = naiveHull(points)
        self.assertEqual(hull , hullActual)

# runnable from command line
if __name__ == '__main__':
    unittest.main()
