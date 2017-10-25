import copy
import math
import sys
import random

EPSILON = sys.float_info.epsilon



testPoints = [(84, 323), (225, 106), (406, 311), (216, 515), (563, 422), (746, 420), (855, 100), (598, 115)]

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
            clockwiseSort(points)
            return points
        # for points numbering less than 7, we can brute force our convex hull
        elif len(points) <= 6: 
            return naiveHull(points)  
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
            # if either of our left or right points is empty, we should just return the sorted non empty one
            if not leftPoints:
               clockwiseSort(rightPoints)
               return rightPoints
            if not rightPoints:
                clockwiseSort(leftPoints)
                return leftPoints
            return merge(computeHull(leftPoints) , computeHull(rightPoints), min_y , max_y, demarkation_line)

def merge(left , right, min_y , max_y, x_value):
    # invariant - left, right both contain clockwise sorted convex hulls, each of at least n=1 point
    l_hull = copy.deepcopy(left)
    r_hull = copy.deepcopy(right)
    # search left for the rightmost point
    rightmost = 0
    for x in range(0 , len(l_hull)):
        if l_hull[x][0] > l_hull[rightmost][0]:
            rightmost = x

    # search right for the leftmost point
    leftmost = 0 # we assume the leftmost node is the first one
    for x in range(0 , len(r_hull)):
        if r_hull[x][0] < r_hull[leftmost][0]:
            leftmost = x

    # we can get our x val here too
    x_value = (r_hull[leftmost][0] + l_hull[rightmost][0]) / 2
    

    # first we want to find the upper tangent
    i = rightmost 
    j = leftmost

    while(yint(l_hull[i] , r_hull[mod_clockwise(j , len(r_hull))] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y , max_y)[1]
            or yint(l_hull[mod_cclockwise(i , len(l_hull))] , r_hull[j] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y, max_y)[1]):
            if yint(l_hull[i] , r_hull[mod_clockwise(j , len(r_hull))] , x_value , min_y , max_y)[1] < yint(l_hull[i] , r_hull[j] , x_value, min_y , max_y)[1]:
                j = mod_clockwise(j , len(r_hull))
            else:
                i = mod_cclockwise(i , len(l_hull))


    # find lower tangent
    k = rightmost
    l = leftmost

    while(yint(l_hull[mod_clockwise(k , len(l_hull))] , r_hull[l] , x_value , min_y , max_y)[1] > yint(l_hull[k] , r_hull[l] , x_value, min_y, max_y)[1] or
        yint(l_hull[k] , r_hull[mod_cclockwise(l , len(r_hull))] , x_value, min_y, max_y)[1] >  yint(l_hull[k] , r_hull[l] , x_value , min_y , max_y)[1]):
            if yint(l_hull[mod_clockwise(k , len(l_hull))] , r_hull[l] , x_value , min_y , max_y)[1] > yint(l_hull[k] , r_hull[l] , x_value, min_y, max_y)[1]:
                k = mod_clockwise(k , len(l_hull))
            else:
                l = mod_cclockwise(l , len(r_hull))

    sup_points = []
    # now we need to remove points from l_hull that are clockwise between i and k
    start = mod_clockwise(i , len(l_hull))
    while start != k:
       sup_points.append(l_hull[start]) 
       start = mod_clockwise(start , len(l_hull))

    # now we need to remove points from r_hull that are clockwise between l and j
    start = mod_clockwise(l , len(r_hull))
    while start != j:
        sup_points.append(r_hull[start])
        start = mod_clockwise(start , len(r_hull))
    new_convex_hull = l_hull + r_hull
    finalList = []
    for point in new_convex_hull:
        if point not in sup_points:
            finalList.append(point)
    clockwiseSort(finalList)
    return finalList


def mod_clockwise(x , length):
    return (x+1) % length
def mod_cclockwise(x , length):
    return (x - 1) % length

# Naive implementation of the convex hull algorithm. This 
def naiveHull(pointsList):
    hullPoints = []
    # we want to remove duplicates to avoid issues
    points = copy.deepcopy(pointsList)
    numPoints = len(points)
    if(numPoints == 1):
        return points
    if numPoints == 2 and (points[0] == points[1]):
        return [points[0]]

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
            if onHull and (points[i] != points[j]):
                if points[i] not in hullPoints:
                    hullPoints.append(points[i])
                if points[j] not in hullPoints:
                    hullPoints.append(points[j])
            j = (j + 1) % numPoints
    clockwiseSort(hullPoints)
    return hullPoints

def naiveHull2(input_points):
    # copy points
    points = copy.deepcopy(input_points)
    # remove any duplicates

    if len(points) == 1:
        return points
    if len(points) == 2 and (points[0] == points[1]):
        return [points[0]]
    
    hull = []
    for i in range(0 , len(points)):
        j = (i+1) % len(points)
        while j != i:
            above = []
            below = []
            for k in range(0 , len(points)):
                if collinear(points[i] , points[j] , points[k]):
                    pass
                elif cw(points[i] , points[j] , points[k]):
                    above.append(k)
                else:
                    below.append(k)
            # we add this point only if one of the two lists was empty, also we dont care if i and j are same point, as there is nothing on either side
            if (not above or not below) and (points[i] != points[j]):
                # this is on the hull
                if points[i] not in hull:
                    hull.append(points[i])
                if points[j] not in hull:
                    hull.append(points[j])
            j = (j+1) % len(points)
    clockwiseSort(hull)
    return hull
            
    
    
