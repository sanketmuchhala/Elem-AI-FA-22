#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sakshi Rathi sakrathi
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#
#added astar and heuristic for each cost function
#cost distance: h(s) - haversine dist from current state to goal state
#cost segments: h(s) - haversine dist from current state to goal state
#cost time: h(s) - haversine dist from current state to goal state / 50 , considering avg speed.
#cost delivery: h(s) - same as time, considering the best case scenario where the package doesn't fall i.e there is not over speeding.
# !/usr/bin/env python3
from ssl import CHANNEL_BINDING_TYPES
import sys
from math import radians, cos, sin, asin, sqrt
import math
from queue import PriorityQueue

# read city-gps.txt
#to get the city latitude and longitude
def read_citygps():
    with open('city-gps.txt') as file:
        for line in file:
            citygps.append(line.strip().split(' '))

# return latitude and longitude of a city from the citygps list
def latlong_city(city):
    for c in citygps:
        if city in c:
            return c
    return False

#find nearest neighbour for inconsistent cities with no lat and long:
def nearest_city(city):
    min = 0
    min_seg = ' '
    for seg in d.keys():
        if city in seg:
            if min == 0 and ((latlong_city(seg.split(' ')[0]) is not False) or (latlong_city(seg.split(' ')[1]) is not False )):
                min = float(d[seg][0])
                min_seg = seg
            if min > float(d[seg][0]) and ((latlong_city(seg.split(' ')[0]) is not False) or (latlong_city(seg.split(' ')[1]) is not False )):
                #print(min)
                min = float(d[seg][0])
                min_seg = seg
    #print(min)
    c = min_seg.split(' ')
    #print("nearest",c)
    #print('no lat long: ',c)
    if c[0] == city:
        #print('nearest mem: ',min_seg,city,)
        return c[1]
    else:
        print('nearest mem: ',min_seg,c)
        return c[0]

# find shortest distance between 2 cities given latitude and longitude
# finding haversine distance
def latlong_dist(start, end):
    if latlong_city(start) is False:
        near = nearest_city(start)
        latlong_dist(near,end)
    else:
        lat1 = float(latlong_city(start)[1])
        long1 = float(latlong_city(start)[2])
        lat2 = float(latlong_city(end)[1])
        long2 = float(latlong_city(end)[2])
        long1, lat1, long2, lat2 = map(math.radians, [long1, lat1, long2, lat2])
        # Haversine formula
        dlong = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlong/ 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 3956  # radius of earth in miles 3956
        #print('latlong_d: ',start,end,c*r)
        return (c * r)

#for a given state, find the possible states that are not visited
# update the visited list for the states found in this function
def successors(state,visited):
    city = state[0]
    new_key = list(d)
    succ = []
    for seg in d.keys():
        l= []
        if city in seg and visited[new_key.index(seg)] is False:
            visited[new_key.index(seg)] = True
            csplit = seg.split(' ')
            if city == csplit[0]:
                l = [csplit[1],float(d[seg][0]),float(d[seg][1]),d[seg][2]]
            else:
                l = [csplit[0],float(d[seg][0]),float(d[seg][1]),d[seg][2]]
            succ.append(l)
    return succ

#goal state
#checking if the current state is the goal state
def is_goal(state,end_city):
    if end_city == state[0]:
        return True
    return False

#h- cost -distance
#heuristic for distance will be the best possible distance which is the haversine distance
def h1(state,end_city):
    city = state[0]
    return latlong_dist(city,end_city)

#a star for cost distance
def astar_route_dist(start_city,end_city):
    min_cost = latlong_dist(start_city,end_city)
    fringe = PriorityQueue()
    initial_state = [start_city,0,0,'NULL']
    fringe.put(((initial_state, []), 1))
    visited = [False for _ in range(len(d))]
    g = 0 #cost of best path from source to state s
    f1 = 0 #the evaluation cost for any state
    g1 = 0 #the cost from source to current state
    path = []
    while not fringe.empty():
        ((state,path),_)= fringe.get()
        g = g + state[1] #cost from initial point to the current point
        if is_goal(state,end_city):
            return path + [state,]
        for s in successors(state,visited):
            g1 = g + s[1] #estimated cost from initial point to current point
            #print(s[0])
            f1 = g1 + h1(s,end_city)
            if h1(s,end_city) == min_cost:  #if the end city is obtained in one go, that is a segment exists from start city to end city, avoiding finding all the successors
                return path + [s,]
            fringe.put(((s, path + [s, ]), f1 ))

#heuristic for segments
#considering it to be the haversine, assuming the one with the minimum haversine distance will have minimum number of segments
def h2(state,end_city):
    city = state[0]
    return latlong_dist(city,end_city)
def astar_route_seg(start_city,end_city):
    fringe = PriorityQueue()
    initial_state = [start_city, 0, 0, 'NULL']
    fringe.put(((initial_state, []), 1))
    visited = [False for _ in range(len(d))]
    g = 0  # number of segments from initial state to current state
    f2 = 0  #evaluation function
    g2 = 0  #no of segments from initial state to current state
    while not fringe.empty():
        ((state, path), _) = fringe.get()
        g = g + 1  # the cost from initial state to current state, the number of segments will increment by 1 as we traverse through every state.
        if is_goal(state,end_city):
            return path + [state, ]
        for s in successors(state, visited):
            g2 = g + 1  # number of segments will increment by 1 as we traverse through very state
            f2 = g2 + h2(s,end_city)
            fringe.put(((s, path + [s, ]), f2))

#heuristic for time
# dist/speed = haversine dist/ 50 mph considering 50 mph as the avg speed.
def h3(state,end_city):
    return h1(state)/50
#cost-time
def astar_route_time(start_city,end_city):
    fringe = PriorityQueue()
    initial_state = [start_city, 0, 0, 'NULL']
    fringe.put(((initial_state, []), 1))
    visited = [False for _ in range(len(d))]
    g = 0  # time from source to current state
    f3 = 0 #evaluation cost for a state
    g3 = 0 #time from source to current state - local variable
    while not fringe.empty():
        ((state, path), _) = fringe.get()
        g = g + state[1]/state[2]  # cost from initial point to the current point, updating it by the state distance/state speed
        if is_goal(state,end_city):
            return path + [state, ]
        for s in successors(state, visited):
            g3 = g + s[1]/s[2]  # estimated time from initial point to current point
            f3 = g3 + h3(s,end_city)
            fringe.put(((s, path + [s, ]), f3))
#cost-delivery
#considering the best case of no overspeeding and package not falling
#so considering the time to be haversine dist/50
def h4(state,end_city):
    return h1(state,end_city)/50    #add the extra time not added yet
def astar_route_deliv(start,end):
    fringe = PriorityQueue()
    initial_state = [start_city, 0, 0, 'NULL']
    fringe.put(((initial_state, []), 1))
    visited = [False for _ in range(len(d))]
    g = 0  # cost of best path from source to state s
    f = 0
    g4 = 0
    while not fringe.empty():
        ((state, path), _) = fringe.get()
        #time from initial point to the current point
        #is troad + 2*p*(troad + ttrip)
        #here ttrip is the time it took to get from the start city to the beginning of the road,
        #and troad is the time it takes to drive the length of the road segment.
        l = state[1]  # l is the length of road segment
        p = math.tanh(l / 1000) #prob of package falling off
        g = g + 2*p*(g + state[1]/state[2])
        if is_goal(state):
            return path + [state, ]
        for s in successors(state, visited):
            l = s[1]  # l is the length of current road segment
            p = math.tanh(l / 1000) #prob of package falling off
            g4 = g + 2*p*(g + state[1] / state[2]) # total time if the package falls off
            f4 = g4 + h4(s,end_city)
            fringe.put(((s, path + [s, ]), f2))
# get route a star
def get_route(start, end, cost):
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    if cost == 'distance':
        route = astar_route_dist(start_city,end_city)

    if cost == 'segments':
        route = astar_route_seg(start_city,end_city)

    if cost == 'time':
        route = astar_route_time(start_city,end_city)

    if cost == 'delivery':
        route == astar_route_deliv(start_city,end_city)

    """route_taken = [("Martinsville,_Indiana", "IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana", "IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana", "IN_37 for 7 miles")]"""
    dist = 0
    hours = 0
    for r in route:
        #print(r)
        dist = dist + r[1] #distance
        hours = hours + r[2]/r[1]
    return route

    """return {"total-segments": len(route),
            "total-miles": dist,
            "total-hours": hours,
            "total-delivery-hours": 0,
            "route-taken": route}"""

# Please don't modify anything below this line
#
if __name__ == "__main__":
    #create a dictionary for the roadseg file
    citygps = []
    read_citygps()
    d = {}
    with open('road-segments.txt') as file:
        for line in file:
            city_info = line.strip().split(' ')
            d[f"{city_info[0]} {city_info[1]}"] = city_info[2:]

    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    print(result)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])