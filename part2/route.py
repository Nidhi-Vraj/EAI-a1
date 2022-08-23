#!/usr/local/bin/python3
# route.py: find routes through maps
#
# Code by: Nidhi Vraj Sadhuvala, Aditi Soni, Srinivas Vaddi, Username - nsadhuva-adisoni-svaddi
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#


import heapq
import sys
from math import radians, cos, sin, tanh, atan2, asin, sqrt


#reading the file "city-gps.txt" and city_loc has all the assigned key-value pairs for easy access. Key is the city name and its associated values are --
#Longitutude,longitude.
def get_gps():
    city_locations = []
    city_loc = {}
    with open("city-gps.txt", "r") as f:
        for line in f.readlines():
            city_gps_data = line.split()
            city = city_gps_data[0]
            latitude = float(city_gps_data[1])
            longitude = float(city_gps_data[2])
            city_locations.append([city, latitude, longitude])
    for i in city_locations:
        if i[0] not in city_loc:
            city_loc[i[0]] = (i[1], i[2]) #key-value pairs
    return city_loc

#reading the file "road-segments.txt" and assigning key-value pairs for easy access. Key is the city_A name and its associated values are --
# city_B name, lenght in miles, speed, highway name. I'm appending the succcessors as values (all the possible next cities from this city_A) into this key.
# Since the path from city_A to city_B is same as city_B to city_A, this road_dict consists of all the successors of both cities A and B.
def get_road_segments():
    road_segments = []
    road_dict = {}
    with open("road-segments.txt", "r") as f:
        for line in f.readlines():
            segments = line.split()
            city_1 = segments[0]
            city_2 = segments[1]
            length_miles = segments[2]
            speed = segments[3]
            highway_name = segments[4]
            road_segments.append([city_1, city_2, length_miles, speed, highway_name])
            road_segments.append([city_2, city_1, length_miles, speed, highway_name])
    for i in road_segments:
        if i[0] in road_dict:
            road_dict[i[0]].append((i[1], i[2], i[3], i[4]))

        else:
            road_dict[i[0]] = [(i[1], i[2], i[3], i[4])]
    return road_dict


# Used Haversine Distance as it is a very accurate way of computing distances between two points on the surface of the sphere--
# using langitude and latitude of those two points. This is the heuristic function for distance as it doesn't overestimate the lowest--
# possible cost to the goal state.
def distance(city_loc, start_city, end_city):
    if start_city not in city_loc or end_city not in city_loc:
        return 0
    latitude1 = float(city_loc[start_city][0]) #latitude of start_city
    latitude2 = float(city_loc[end_city][0]) #latitude of end_city

    longitude1 = float(city_loc[start_city][1]) #longitude of start_city
    longitude2 = float(city_loc[end_city][1]) #longitude of end_city
    radius = 3958.8 #radius of earth in miles

    dlat = radians(latitude2 - latitude1)
    dlong = radians(longitude2 - longitude1)

    x = sin(dlat / 2) ** 2 + cos(radians(latitude1)) \
        * cos(radians(latitude2)) * sin(dlong / 2) ** 2

    y = 2 * atan2(sqrt(x), sqrt(1 - x))
    d = radius * y

    return d

#Heuristic function for time. 
def time(road_dict, start_city, end_city):
    road_dict = get_road_segments()
    city_loc = get_gps()
    dist = distance(city_loc, start_city, end_city) #dist is the haversine distance between start_city and end_city
    speed = []
    for i in road_dict:
        for j in road_dict[i]:
            speed.append(j[2]) #storing all the speed values in the list "speed"
    speed.sort() #sorting all the values in ascending order to extract the last element
    max_speed = speed[-1] #return maximum speed from the list

    heuristic_time = dist / int(max_speed) #time=distance/speed
    return heuristic_time

#Heuristic function for delivery so that it will never overestimate the actual delivery hours taken by delivery person if he drops a packet.
def heuristic_delivery(road_dict, start_city, end_city, time_so_far):
    road_dict = get_road_segments()
    delivery_hrs = 0.0
    dist = distance(get_gps(), start_city, end_city)

    for j in road_dict[start_city]:
        if j[0] == end_city:
            if float(j[2]) >= 50.0: #if speed exceeds 50 mph 
                p = tanh(float(j[1]) / 1000)
                #haversine distance between two cities divided by speed it took to travel that distance
                t_road = dist / float(j[2])                                  
                t_trip = time_so_far
                delivery_hrs = t_road + p * 2 * (t_road + t_trip)
            else:
                delivery_hrs = dist / float(j[2]) #time=distance/speed --> haversine distance of two points divided by speed of that particular segment
    return delivery_hrs

#Calculating actual delivery hours when a delivery person drops a packet.
def other_delivery(road_dict, start_city, end_city, time_so_far):
    road_dict = get_road_segments()
    delivery_hrs = 0.0

    for j in road_dict[start_city]:
        if j[0] == end_city:
            if float(j[2]) >= 50.0:
                p = tanh(float(j[1]) / 1000)
                t_road = (float(j[1]) / float(j[2]))
                t_trip = time_so_far
                delivery_hrs = t_road + p * 2 * (t_road + t_trip)
            else:
                delivery_hrs = (float(j[1]) / float(j[2]))
    return delivery_hrs

#Heuristic function for segments. 
def segments(road_dict, start_city, end_city):
    road_dict = get_road_segments()
    segment = []
    dist = distance(get_gps(), start_city, end_city)
    for i in road_dict:
        for j in road_dict[i]:
            segment.append(j[1])
    segment.sort()
    max_segment_length = segment[-1] #gives maximum segment length in the entire dataset of "road-segments.txt"
    return dist / int(max_segment_length) #Haversine distance by maximum segment length in the entire dataset


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


    road_dict = get_road_segments()
    city_loc = get_gps()
    curr_city, distance_so_far, time_so_far, delivery, route_taken = start, 0, 0, 0, []

    #fringe has current city location, distance travelled so far, time taken so far, delivery hours if a person drops a packet--
    #and the route taken has the path that contains next city,highway name and speed from the current city.
    #The first element in the fringe is the cost of the heuristic value such that the lesser value gets popped every time to get the optimal solution.
    fringe = [(0, (curr_city, distance_so_far, time_so_far, delivery, route_taken))]
    
    #code starting from here has been taken as a reference from the site- "https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/"
    heapq.heapify(fringe)
    #code ends here
    visited = [] #has all the visited cities 

    while fringe:
        (curr_city, distance_so_far, time_so_far, delivery, route_taken) = heapq.heappop(fringe)[1] #heapq.heappop function removes and returns the smallest element from the fringe
        #visited.append(curr_city)

        if curr_city == end: #if we reach final destination then we return the output in below format

            return {"total-segments": len(route_taken),
                    "total-miles": distance_so_far,
                    "total-hours": time_so_far,
                    "total-delivery-hours": delivery,
                    "route-taken": route_taken}
        else:

            for i in road_dict[curr_city]: #generates all successors of the current city  
                if i[0] not in visited: 
                    visited.append(i[0]) #if a city is not in visited list then append that city so that we won't have to revisit again

                    if cost == "distance":                        
                        heuristic = distance_so_far + distance(city_loc, curr_city, i[0])
                        route_taken_so_far = route_taken[:]
                        route_taken_so_far.append((i[0], i[3] + "  for " + i[1] + " miles"))
                        succ = (heuristic, (
                            i[0], distance_so_far + float(i[1]), time_so_far + (float(i[1]) / float(i[2])),
                            delivery + other_delivery(road_dict, curr_city, i[0], time_so_far), route_taken_so_far))
                    if cost == "time":
                        heuristic = time_so_far + time(road_dict, curr_city, i[0])
                        route_taken_so_far = route_taken[:]
                        route_taken_so_far.append((i[0], i[3] + "  for " + i[1] + " miles"))
                        succ = (heuristic, (
                            i[0], distance_so_far + float(i[1]), time_so_far + (float(i[1]) / float(i[2])),
                            delivery + other_delivery(road_dict, curr_city, i[0], time_so_far),
                            route_taken_so_far))
                    if cost == "segments":
                        heuristic = len(route_taken) + segments(road_dict, i[0], end)
                        route_taken_so_far = route_taken[:]
                        route_taken_so_far.append((i[0], i[3] + "  for " + i[1] + " miles"))
                        succ = (heuristic, (
                            i[0], distance_so_far + float(i[1]), time_so_far + (float(i[1]) / float(i[2])),
                            delivery + other_delivery(road_dict, curr_city, i[0], time_so_far), route_taken_so_far))
                    if cost == "delivery":
                        heuristic = delivery + heuristic_delivery(road_dict, curr_city, i[0], time_so_far)
                        route_taken_so_far = route_taken[:]
                        route_taken_so_far.append((i[0], i[3] + "  for " + i[1] + " miles"))
                        succ = (heuristic, (
                            i[0], distance_so_far + float(i[1]), time_so_far + (float(i[1]) / float(i[2])),
                            delivery + other_delivery(road_dict, curr_city, i[0], time_so_far), route_taken_so_far))
                    
                    #constructs a min heap through heapify() function and subsequently calls heappush() to add elements into the fringe--
                    #while maintaining the heap property.
                    heapq.heappush(fringe, succ)


# Please don't modify anything below this line
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function)=sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])







