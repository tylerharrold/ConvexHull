import copy
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
        elif len(points) <= 6: # here we implement a naive, brute force approach
            hullPoints = []
            numPoints = len(points)
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
        else:
            # our recursive implementation
            # first we split the points
            min_x = max_x = points[0][0]
            min_y = max_y = points[0][1]
            for point in points:
                if point[0] < min_x:
                    min_x = point[0]
                if point[0] > max_x:
                    max_x = point[0]    
                if point[1] < min_y:
                    min_y = point[1]
                if point[1] > max_y:
                    max_y = point[1]
            demarkation_line = (max_x + min_x) / 2
            # split the points
            leftPoints = []
            rightPoints = []
            for point in points:
                x_val = point[0]
                if x_val <= demarkation_line:
                    leftPoints.append(point)
                else:
                    rightPoints.append(point)
            return merge(computeHull(leftPoints) , computeHull(rightPoints), min_y , max_y, demarkation_line)

def merge(left , right, min_y , max_y, x_value):
    l_hull = copy.deepcopy(left)
    r_hull = copy.deepcopy(right)
    # first we want to find the upper tangent
    i = j = 1

    while(yint(l_hull[i] , r_hull[mod_cclockwise(j , len(r_hull))] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y , max_y)[1]
            or yint(l_hull[mod_clockwise(i , len(l_hull))] , r_hull[j] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y, max_y)[1]):
            if yint(l_hull[i] , r_hull[mod_cclockwise(j , len(r_hull))] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y , max_y)[1]:
                j = mod_cclockwise(j , len(r_hull))
            else:
                i = mod_clockwise(i , len(l_hull))


    # find lower tangent
    k = l = 1

    while(yint(l_hull[mod_cclockwise(k , len(l_hull))] , r_hull[l] , x_value , min_y , max_y)[1] > yint(l_hull[k] , r_hull[l] , x_value, min_y, max_y)[1] or
        yint(l_hull[k] , r_hull[mod_clockwise(l , len(r_hull))] , x_value, min_y, max_y)[1] >  yint(l_hull[k] , r_hull[l] , x_value , min_y , max_y)[1]):
            if yint(l_hull[mod_cclockwise(k , len(l_hull))] , r_hull[l] , x_value , min_y , max_y)[1] > yint(l_hull[k] , r_hull[l] , x_value, min_y, max_y)[1]:
                k = mod_cclockwise(k , len(l_hull))
            else:
                l = mod_clockwise(l , len(r_hull))


    # now we need to remove points from l_hull that are clockwise between i and k
    start = mod_clockwise(i , len(l_hull))
    while start != k:
       l_hull.pop(start) 
       start = mod_clockwise(start-1 , len(l_hull))

    # now we need to remove points from r_hull that are clockwise between l and j
    start = mod_clockwise(l , len(r_hull))
    while start != j:
        r_hull.pop(start)
        start = mod_clockwise(start-1 , len(r_hull))

    new_convex_hull = l_hull + r_hull
    clockwiseSort(new_convex_hull)
    return new_convex_hull

    

def mod_clockwise(x , length):
    return (x+1) % length
def mod_cclockwise(x , length):
    return (x - 1) % length

