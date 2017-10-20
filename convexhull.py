import math
import sys

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''
def computeHull(points):
        # first base case
        if len(points) <= 3:
            return points
        else: # here we implement a naive, brute force approach
            hullPoints = []
            numPoints = len(points)
            '''
            for i in range(0 , numPoints):
                notFound = True
                j = (i + 1) % len(points) 
                while j != i and notFound:
                    # here we check all lines from point i to all other points for a hull
                    k = (j + 1) % len(points)
                    if collinear(points[i] , points[j] , points[k]):
                        pass
                    else:
                        currentTri = cw(points[i] , points[j] , points[k])
                        allOnOneSide = True
                        while k != i and allOnOneSide: 
                            if cw(points[i] , points[j] , points[k]) != currentTri:
                                allOnOneSide = False
                            k = (k + 1) % len(points)
                        if allOnOneSide:
                            notFound = False
                            # we add points i and j
                            if points[i] not in hullPoints:
                                hullPoints.append(points[i])
                            if points[j] not in hullPoints:
                                 hullPoints.append(points[i])
                    j = (j + 1) % len(points)
            '''
            for i in range (0 , numPoints):
                j = (i + 1) % numPoints
                while j != i:
                    # we assume ij is on hull
                    onHull = True
                    firstTest = True
                    ccValue = False
                    for k in range(0 , numPoints):
                        if not collinear(points[i] , points[j] , points[k]):
                            # get if these points are clockwise or counterclockwise
                            curValue = cw(points[i] , points[j] , points[k])
                            if firstTest:
                                ccValue = curValue
                                firstTest = False
                            else:
                                if curValue != ccValue:
                                    onHull = False
                        if not onHull:
                            break
                    if onHull:
                        if points[i] not in hullPoints:
                            hullPoints.append(points[i])
                        if points[j] not in hullPoints:
                            hullPoints.append(points[j])
                    j = (j + 1) % numPoints
            clockwiseSort(hullPoints)
            return hullPoints
