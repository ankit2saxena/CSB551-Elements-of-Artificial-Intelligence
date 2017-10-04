# -*- coding: utf-8 -*-
"""
Please have a look at the README.md file in the parent directory for the answers to the below questions.
Created on Sun Sep 17 00:56:49 2017
1. Which search algorithm seems to work best for each routing options?
2. Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much, according to your experiments?
3. Which algorithm requires the least memory, and by how much, according to your experiments?
4. Which heuristic function(s) did you use, how good is it, and how might you make it/them better?
@author: Ankit
"""

import sys
import csv
import heapq
import math

#To represent the final Route
class Route:
    start_city = ''
    end_city = ''
    total_distance_in_miles = 0.0
    total_time_in_miles = 0.0
    path = ''
    
    def __init__(self, start_city, end_city, total_distance_in_miles, total_time_in_miles, path):
        self.start_city = start_city
        self.end_city = end_city
        self.total_distance_in_miles = total_distance_in_miles
        self.total_time_in_miles = total_time_in_miles
        self.path = path
        
    def showDetails(self, localMap):
        
        if len(self.path) > 1:
            temp_cities = self.path.split(' ')
            temp_cities.append(end_city)
            city1 = start_city
            for city2 in temp_cities:
                c1 = localMap.get_city(city1)
                details = c1.get_adj_details(city2)
                print details[0], "{:0.4f}".format(c1.get_adj_time(city2)) , city1, details[2], city2
                city1 = city2
        
            print "{:0.0f}".format(self.total_distance_in_miles), "{:0.4f}".format(self.total_time_in_miles) , start_city, self.path, self.end_city
        else:
            print "{:0.0f}".format(self.total_distance_in_miles), "{:0.4f}".format(self.total_time_in_miles) , start_city, self.end_city
            
#To add a City node in the graph
class City:
    name = ''
    latitude = 0.0
    longitude = 0.0
    state = ''
    
    def __init__(self, name, latitude, longtitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longtitude
        self.adj_city = {}
        state = name.split(',')[1]
        self.state = state[1:]
        
    def set_adj_city(self, adj_city_name, distance, speed_limit, highway):
        self.adj_city[adj_city_name] = [distance, speed_limit, highway]
        
    def get_adj_city(self):
        return self.adj_city.keys()
        
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
        
    def get_adj_details(self, adj_city_name):
        return self.adj_city[adj_city_name]

    def get_adj_distance(self, adj_city_name):
        distance = float(self.get_adj_details(adj_city_name)[0])
        return distance
        
    def get_adj_time(self, adj_city_name):
        details = self.get_adj_details(adj_city_name)
        time = float(details[0])/float(details[1])
        return time
        
    def get_state_name(self):
        return self.state

#To create a Map of cities, as a Graph
class Map:
    
    def __init__(self):
        self.cities = {}
        self.states = []
        self.no_cities = 0
        
    def set_city(self, city_name, latitude, longtitude):
        city = City(city_name, latitude, longtitude)
        self.cities[city_name] = city
        
        state = city_name.split(',')[1]
        state = state[1:]
        if state not in self.states:
            self.states.append(state)
        self.no_cities = self.no_cities + 1
        return city
        
    def get_city(self, city_name):
        if city_name in self.cities:
            return self.cities.get(city_name)
        else:
            return None
            
    def set_edge(self, localMap, start_city, end_city, distance, speed_limit, highway):
        #to handle cities that not in 'city-gps.txt'
        if start_city not in self.cities:
            self.cities[start_city] = City(start_city, 0.0, 0.0)
        
        if end_city not in self.cities:
            self.cities[end_city] = City(end_city, 0.0, 0.0)
            
        if float(distance) == 0.0:
            distance = heuristic_calc_Haversine(localMap, start_city, end_city)
            if float(distance) == 0.0:
                distance = sys.maxint    
            
        self.cities.get(start_city).set_adj_city(end_city, distance, speed_limit, highway)
        self.cities.get(end_city).set_adj_city(start_city, distance, speed_limit, highway)
        
    #to get a list of all cities in the map
    def get_cities(self):
        return self.cities.keys()
        
    #to get a list of US states in the map
    def get_states(self):
        return self.states
        
    #to remove non-US states or regions
    def remove_extra_states(self):
        not_US_states = ['Tamaulipas', 'Prince_Edward_Island', 'Saskatchewan', 'British_Columbia', 
                         'New_Brunswick', 'Yukon_Territory', 'Manitoba', 'Baja_California_Norte', 
                         'Tamaulipas', 'Coahuila', 'Labrador', 'Sonora', 'St._Pierre_and_Miquelon',
                         'Newfoundland', 'Alberta', 'Ontario', 'Nova_Scotia', 'District_of_Columbia', 'Alaska']
        for x in not_US_states:
            if x in self.states:
                self.states.remove(x)
        self.states.sort()
            
        pass


#To find the optimal route based on the query        
class Locate_Me:
    start_city = ''
    end_city = ''    
    routes = {}
    final_routes = []
    
    def __init__(self, start_city, end_city):
        self.start_city = start_city
        self.end_city = end_city
        
    def loadFiles(self, localMap):
        #create a dictionary of cities and (latitude, longitude)
        with open('city-gps.txt', 'rt') as f:
            reader = csv.reader(f, delimiter = ' ')
                
            for num, rows in enumerate(reader):
                
                #to correct the spelling of Mississippi
                if rows[0] == 'Morton,_Mississppi':
                    rows[0] = 'Morton,_Mississippi'
                
                localMap.set_city(rows[0], rows[1], rows[2])
                pass
            
        #create a mapping of road-segments
        with open('road-segments.txt', 'rt') as f:
            reader = csv.reader(f, delimiter = ' ')
            for num, rows in enumerate(reader):
                
                #to correct the spelling of Mississippi
                if rows[0] == 'Morton,_Mississppi':
                    rows[0] = 'Morton,_Mississippi'
                    
                if rows[1] == 'Morton,_Mississppi':
                    rows[1] = 'Morton,_Mississippi'
                    
                #rows[2] is distance, rows[3] is speed limit, rows[4] is route
                if rows[2] != '' and rows[3] != '' and rows[2] != '0' and rows[3] != '0':
                    localMap.set_edge(localMap, rows[0], rows[1], rows[2], rows[3], rows[4])
                    pass
                #in case the value of distance is 0 or blank, insert the distance from Haversine value
                if rows[2] == '0' or rows[2] == '':
                    localMap.set_edge(localMap, rows[0], rows[1], 0.0, rows[3], rows[4])
                    pass   
                #in case the value of time is 0 or blank, insert the maxint value
                if rows[3] == '0' or rows[3] == '':
                    localMap.set_edge(localMap, rows[0], rows[1], rows[2], sys.maxint, rows[4])
                    pass
                    
        pass
    
    def routing_bfs_dfs(self, routing_algorithm, localMap, start_city, end_city):
        total_distance_in_miles = 0.0
        total_time_in_miles = 0.0
        p = ''
        visited = []
        
        stack = [(start_city, [total_distance_in_miles, total_time_in_miles, p, visited])]
        
        while stack:
            if routing_algorithm == 'bfs':
                city1, details = stack.pop(0)
            else:
                city1, details = stack.pop()
                
            total_distance_in_miles, total_time_in_miles, p = details[0], details[1], details[2]
            visited = details[3]

            for city2 in localMap.cities.get(city1).get_adj_city():
                if city2 != start_city and city2 not in visited:
                    distance, time, p_string = total_distance_in_miles, total_time_in_miles, p
                    
                    imported = localMap.get_city(city1).get_adj_details(city2)
                    distance = distance + float(imported[0])
                    time = time + (float(imported[0])/float(imported[1]))
                    
                    if city2 != end_city:
                        if p_string != '':
                            p_string = p_string + ' '
                        p_string = p_string + city2
            
                    if city2 == end_city:
                        route = Route(start_city, end_city, distance, time, p_string)
                        route.showDetails(localMap)
                        return
                    
                    visited.append(city2)
                    stack.append((city2, [distance, time, p_string, visited]))
        print ''
        pass
    
    def routing_uniform(self, cost_function, localMap, start_city, end_city, longtour = False):
        total_distance_in_miles = 0.0
        total_time_in_miles = 0.0
        p = ''
        visited = []
        c = 0
        
        stack = [(c, [total_distance_in_miles, total_time_in_miles, p, start_city])]
    
        while stack:
            cost, details = heapq.heappop(stack)
            total_distance_in_miles, total_time_in_miles, p, city1 = details[0], details[1], details[2], details[3]
            
            if city1 not in visited:
                visited.append(city1)
                
                for city2 in localMap.cities.get(city1).get_adj_city():
                    if city2 != start_city and city2 not in visited:
                        distance, time, p_string = total_distance_in_miles, total_time_in_miles, p
                        c = cost
                        
                        if longtour:
                            distance = distance - localMap.get_city(city1).get_adj_distance(city2)
                            time = time - localMap.get_city(city1).get_adj_time(city2)
                            c = distance
                        else:
                            distance = distance + localMap.get_city(city1).get_adj_distance(city2)
                            time = time + localMap.get_city(city1).get_adj_time(city2)
                            c = c + 1
                            
                            if cost_function == 'distance':
                                c = distance
                            elif cost_function == 'time':
                                c = time
                        
                        if city2 != end_city:
                            if p_string != '':
                                p_string = p_string + ' '
                            p_string = p_string + city2
                            
                        if city2 == end_city:
                            if longtour:
                                distance = -distance
                                time = -time
                        
                            route = Route(start_city, end_city, distance, time, p_string)
                            route.showDetails(localMap)
                            return
                        
                        heapq.heappush(stack, (c, [distance, time, p_string, city2]))
        print ''                
        pass
    
    def routing_astar(self, cost_function, localMap, start_city, end_city, stateTour = False):
        total_distance_in_miles = 0.0
        total_time_in_miles = 0.0
        p = ''
        visited = []
        c = 0
        
        global_states = []

        if stateTour:
            global_states = localMap.get_states()
            
        stack = [(c, [total_distance_in_miles, total_time_in_miles, p, start_city])]
    
        while stack:
            cost, details = heapq.heappop(stack)
            total_distance_in_miles, total_time_in_miles, p, city1 = details[0], details[1], details[2], details[3]
            
            if city1 not in visited:
                visited.append(city1)
                
                for city2 in localMap.cities.get(city1).get_adj_city():
                    if city2 != start_city:
                        distance, time, p_string = total_distance_in_miles, total_time_in_miles, p
                        c = cost
                        
                        distance = distance + localMap.get_city(city1).get_adj_distance(city2)
                        time = time + localMap.get_city(city1).get_adj_time(city2)
                        c = c + 1
                        
                        if city2 != end_city:
                            if p_string != '':
                                p_string = p_string + ' '
                            p_string = p_string + city2
                            
                            if not stateTour:
                                if cost_function == 'distance':
                                    c = math.pow(heuristic_calc_Haversine(localMap, city2, end_city), float(1/3)) + distance
                                elif cost_function == 'time':
                                    c = (float((heuristic_calc_Haversine(localMap, city2, end_city))) / 65) - 1 + time
                            
                        if city2 == end_city:
                            if stateTour:
                                temp_cities = p_string.split(' ')
                                local_states = []
                                for cit in temp_cities:
                                    state = cit.split(',')[1]
                                    state = state[1:]
                                    if state not in local_states:
                                        local_states.append(state)
                                    
                                if len(local_states) >= 48:
                                    if set(local_states) & set(global_states) == set(global_states):
                                        route = Route(start_city, end_city, distance, time, p_string)
                                        route.showDetails(localMap)
                                        return
                            else:
                                route = Route(start_city, end_city, distance, time, p_string)
                                route.showDetails(localMap)
                                return
                        
                        heapq.heappush(stack, (c, [distance, time, p_string, city2]))
        print ''                
        pass
            
    def longtour(self, localMap, start_city, end_city):
        self.routing_uniform('distance', localMap, start_city, end_city, True)
        pass
    
    def statetour(self, localMap, start_city, end_city):
        self.routing_astar('distance', localMap, start_city, end_city, True)
        pass
    
def heuristic_calc(localMap, start_city, end_city):
    city1 = localMap.cities.get(start_city)
    city2 = localMap.cities.get(end_city)
    
    lat1, long1 = float(city1.latitude), float(city1.longitude)
    lat2, long2 = float(city2.latitude), float(city2.longitude)
    
    sum = pow((lat1 - lat2), 2) + pow((long1 - long2), 2)
    return pow(sum, 0.5)
    
def heuristic_calc_Haversine(localMap, start_city, end_city):
    city1 = localMap.cities.get(start_city)
    city2 = localMap.cities.get(end_city)
    
    lat1, long1 = math.radians(float(city1.latitude)), math.radians(float(city1.longitude))
    lat2, long2 = math.radians(float(city2.latitude)), math.radians(float(city2.longitude))
    
    if lat1 == 0.0 or lat2 == 0.0 or long1 == 0.0 or long2 == 0.0:
        return 0.0
    
    dlong = long1 - long2
    dlat = lat1 - lat2
    
    R = 3950
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d
    

start_city = sys.argv[1]
end_city = sys.argv[2]
routing_algorithm = sys.argv[3]
cost_function = sys.argv[4]

if routing_algorithm not in ['bfs', 'uniform', 'dfs', 'astar', 'longtour', 'statetour']:
    print 'Please enter a valid value of Routing Algorithm.'
    sys.exit(0)
    
if cost_function not in ['segments', 'distance', 'time']:
    print 'Please enter a valid value of Cost Function.'
    sys.exit(0)

if start_city == end_city:
    sys.exit(0)
    
localMap = Map()
instance = Locate_Me(start_city, end_city)
instance.loadFiles(localMap)
localMap.remove_extra_states()

if routing_algorithm == 'bfs':
    instance.routing_bfs_dfs(routing_algorithm, localMap, start_city, end_city)
elif routing_algorithm == 'uniform':
    instance.routing_uniform(cost_function, localMap, start_city, end_city)
elif routing_algorithm == 'dfs':
    instance.routing_bfs_dfs(routing_algorithm, localMap, start_city, end_city)
elif routing_algorithm == 'astar':
    instance.routing_astar(cost_function, localMap, start_city, end_city)
elif routing_algorithm == 'longtour':
    instance.longtour(localMap, start_city, end_city)
elif routing_algorithm == 'statetour':
    instance.statetour(localMap, start_city, end_city)
