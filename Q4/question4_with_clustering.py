import matplotlib.pyplot as plt
import numpy as np
import random
import math
import sys
import statistics

class Question4():
    
    def __init__(self, is_debug=False):
        # Constructor params
        self.is_debug = is_debug
        
        # annealing schedule
        self.alpha = 0.1                     # alpha parameter
        self.initial_temp = 10000             # initial temperature
        self.final_temp = 0.1                # final temperature
        self.max_stabilization_time =  1000       # number of iterations at each temperature
        self.step_size = 0.0001
        self.temp_decrement_rule = 'linear'
        
        # initialize fixed parameters of problem
        self.max_width = 100
        self.max_height = 100
        self.base_value = -1
        self.num_of_cities = 39
        self.num_of_trucks = 6 #6
        
        # initialize a euclidean map of the cities and depot -> index using [x,y] and get the city idx (or empty space default value of -1)
        self.vrp_map = np.full((self.max_width, self.max_height), self.base_value)
        
        # intialize city table -> index using the city idx and get [x,y] coordinate of the city
        self.city_table = [None] * self.num_of_cities
        
        # initialize demand array -> index using the city idx and get the demand value for that city
        self.demand = [None] * self.num_of_cities
        
        self.filename = 'A-n39-k6.vrp'
    
    def set_params(self, params):
        self.alpha = params['alpha']                                        # alpha parameter
        self.initial_temp = params['initial_temp']                          # initial temperature
        self.final_temp = params['final_temp']                              # final temperature
        self.max_stabilization_time =  params['max_stabilization_time']     # number of iterations at each temperature
        self.step_size = params['step_size']                                # step size to take for neighbour generation
        self.temp_decrement_rule = params['temp_decrement_rule']
        self.name = params['name']
    
    def extract_vrp_data(self, filename, vrp_map, city_table, demand_list):
        # extract city locations from file
        # open the file for reading
        with open(filename, 'r') as file:
            # initialize flag to indicate if we are within NODE_COORD_SECTION
            in_node_section = False
            in_demand_section = False
            
            # read file line by line
            for line in file:
                stripped_line = line.strip()
                
                # check if reached the NODE_COORD_SECTION
                if stripped_line == "NODE_COORD_SECTION":
                    in_node_section = True
                    continue

                # check if reached the DEMAND_SECTION (END of NODE_COORD_SECTION)
                if stripped_line == "DEMAND_SECTION":
                    in_node_section = False
                    in_demand_section = True
                    continue
                    
                if stripped_line == "DEPOT_SECTION":
                    in_node_section = False
                    in_demand_section = False
                    # all data has been extracted, exit the extraction routine
                    break

                # if we are within NODE_COORD_SECTION, extract city location
                if in_node_section:
                    # split the line into components
                    parts = stripped_line.split()
                    if len(parts) == 3:
                        vrp_map[int(parts[1])][int(parts[2])] =  parts[int(0)]
                        city_table[int(parts[0])-1] = [int(parts[1]), int(parts[2])]

                # if we are within DEMAND_SECTION, extract demand value
                if in_demand_section:
                    # split the line into components
                    parts = stripped_line.split()
                    if len(parts) == 2:
                        demand_list[int(parts[0])-1] = int(parts[1])
    
    def plot_map(self, map):
        # get location of cities
        rows, cols = np.where(map > -1)
        values = map[rows, cols]

        # Create the scatter plot
        plt.scatter(cols, rows, c=values, cmap='viridis', s=50, edgecolors='k')
        plt.colorbar(label='Matrix Values')
        plt.title('Scatter plot of matrix values > -1')
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.gca().invert_yaxis()  # Invert y-axis to match the matrix indexing
        #plt.grid(True)
        plt.show()
        
    def euclidean_distance(self, a, b):
        # calculate euclidean distance between two points
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def calculate_centroid(self, cluster):
        # cluster should be a list of integers, corresponding to the identifier of the city
        centroid = None
        
        avg_x = 0
        avg_y = 0
        
        # loop through each city in the cluster and calculate the average x and y coord
        for b in range(0,len(cluster)-1):
            avg_x += self.city_table[cluster[b]][0]
            avg_y += self.city_table[cluster[b]][1]
        
        avg_x = avg_x/(len(cluster)-1)
        avg_y = avg_y/(len(cluster)-1)
        
        # loop through each city and compare with avg (x,y) and find lowest eucledian
        # distance city to theoretical centroid
        shortest_distance = 9999
        for b in range(0,len(cluster)-1):
            dist = self.euclidean_distance(self.city_table[cluster[b]], [avg_x, avg_y])
            
            # current point distance is less than previous point distance
            if(dist < shortest_distance):
                centroid = cluster[b]
                shortest_distance = dist
        
        return centroid
        
        
    def cluster_algo(self, k):
        
        # init centroids (list of idx of cities that will be the centroids)
        centroids = []
        
        # init cluster list (list of k lists, for each cluster)
        clusters = [[] for _ in range(k)]
        
        # intialize k centroids randomly (store the city ID number)
        for b in range(0,k):
            new_centroid = random.randint(0, self.num_of_cities-1)
            
            # keep generating centroid until one is found that is not already in the centroids
            while(new_centroid in centroids):
                new_centroid = random.randint(0, self.num_of_cities-1)
        
            # add new centroid if it does not already appear
            centroids.append(new_centroid)
        
        print("intial centroids:", centroids)
        
        convergence = False
        
        while (not convergence):
            # clear the old clusters
            clusters = [[] for _ in range(k)]
            
            # loop through each city and assign it to the "closest centroid"
            for city_index in range(self.num_of_cities-1):
                current_city = self.city_table[city_index]
                
                distances_to_each_centroid = [self.euclidean_distance(current_city, self.city_table[centroid]) for centroid in centroids]
                cluster_assignment = distances_to_each_centroid.index(min(distances_to_each_centroid)) 
                clusters[cluster_assignment].append(city_index)
        
            new_centroids = [self.calculate_centroid(cluster) for cluster in clusters]
        
            convergence = (new_centroids == centroids)
            centroids = new_centroids
        
            if convergence:
                return clusters
            
    def random_decay(self, cost, t):
        return math.exp(-cost / t)
    
    def temp_reduction_function(self, temp):
        # linear temperature decrement
        if self.temp_decrement_rule == 'geometric':
            return temp*self.alpha
        elif self.temp_decrement_rule == 'slow_decrease':
            return temp / (1+temp*self.alpha)
        else:
            # default to linear temperature decrement
            return temp - self.alpha
    
    def generate_initial_state(self, num_of_trucks, num_of_cities):
        # generate initial set of cities for truck list
        cities = num_of_cities
        truck_routes = [[] for _ in range(num_of_trucks)]
        
        # skip city 1 (which corresponds to idx = 0) as this is the DEPOT
        self.depot = 1
        
        # round robin assign cities to each vehicle route
        while(cities >= 0):
            for i in range(num_of_trucks):
                # if cities have ran out, exit
                if(cities < 0):
                    break
                
                # skip depot
                if(cities == self.depot):
                    cities = cities -1
                    continue
                
                if self.is_debug:
                    print(f"City {cities} is assigned to truck/route {i}")
                    
                truck_routes[i].append(cities)
                cities = cities -1
        return truck_routes
        
    
    def neighbourhood_generator(self, truck_routes):
        
        # generate neighbour to swap
        start_truck_idx = random.randint(0,len(truck_routes)-1)
        end_truck_idx = random.randint(0,len(truck_routes)-1)
        
        start_city_idx = random.randint(0,len(truck_routes[start_truck_idx]))
        end_city_idx = random.randint(0,len(truck_routes[end_truck_idx]))
        
        # conduct swap                
        temp = truck_routes[start_truck_idx][start_city_idx]
        truck_routes[start_truck_idx][start_city_idx] = truck_routes[end_truck_idx][end_city_idx]
        truck_routes[end_truck_idx][end_city_idx] = temp
        
        return truck_routes
    
    def single_route_cost(self, truck_route):
        
        # calculate cost from depot to the first city on the route
        final_cost = self.euclidean_distance(self.city_table[truck_route[0]], self.city_table[0])
        final_cost += self.demand[self.city_table[truck_route[0]]]
        
        # calculate cost for the rest of the route till the last city
        # for each iteration i, the final cost will be the cost to get to city at truck_route[i] including service time
        for i in range(1, len(truck_route)):
            final_cost += self.euclidean_distance(self.city_table[truck_route[i]], self.city_table[truck_route[i-1]])   # travel time to get to city i from previous city
            final_cost += self.demand[self.city_table[truck_route[i]]]                                                  # service time at city @ i
        
        # calculate the cost from the last city back to the depot
        final_cost += self.euclidean_distance(self.city_table[0], self.city_table[truck_route[-1]])
        
        return final_cost
        
    
    def cost_function(self, truck_routes, control_params):
        
        # get control params
        alpha = control_params['alpha']
        beta = control_params['beta']
        gamma = control_params['gamma']
        
        # generate a list of the individual vehicle route costs
        truck_routes_costs = map(self.single_route_cost, truck_routes)
        
        # calculate mean of truck_routes_costs
        mean = statistics.mean(truck_routes_costs)
        
        # calculate median of truck_routes_costs
        median = statistics.median(truck_routes_costs)
        
        # calculate mode of truck_routes_costs
        mode = statistics.mode(truck_routes_costs)      #TODO: check that this functions as expected? 
        
        # calculate final cost function output
        return alpha * (mean - mode) + beta * (mean - median) + gamma * mean

    def run_sa(self):
        # generate initial state
        self.current_state =  self.generate_initial_state(self.num_of_trucks, self.num_of_cities)
        

        # set temp and stabilization values
        self.curr_temp = self.initial_temp
        self.curr_stabilization = 0
        
        #TODO: Move this outside somewhere?
        cost_function_control_params = {'alpha': 0.4, 'beta': 0.4, 'gamma': 1.0}
        
        # continue process until final temp has been reached
        while(self.curr_temp > self.final_temp):

            # continue process until temperature has reached equilibrium in system
            while(self.curr_stabilization < self.max_stabilization_time):
                
                # generate neighbour
                candidate = self.neighbourhood_generator(self.current_state)
                
                # TODO: calculate cost diff for new solution
                cost = self.cost_function(candidate, cost_function_control_params) - self.cost_function(self.current_state, cost_function_control_params)
                
                # check if candidate is acceptable as new solution
                if(cost <= 0 or random.random() < self.random_decay(cost, self.curr_temp) ):
                    # cost diff is better with this candidate (z value is lower, meaning we are moving towards a minimum) 
                    # or random decay was successful
                    self.current_state = candidate
                    
                
                # increment stabilization time
                self.curr_stabilization +=1
                
            
            # decrease t using temp reduction function
            self.curr_temp =  self.temp_reduction_function(self.curr_temp)
            self.curr_stabilization = 0
            
            # Print current state and temperature if requested
            if(self.is_debug):
                sys.stdout.write(f"Current Temperature: {self.curr_temp} | Current State: {self.current_state} -> INSERT_COST \r")
                sys.stdout.flush()
            
        
        print("\n\n\n---Solver Complete---")
        print(f"Final State: {self.current_state}")
        
        return self.current_state     


solver = Question4(True)

solver.extract_vrp_data(solver.filename, solver.vrp_map, solver.city_table, solver.demand)
#solver.plot_map(solver.vrp_map)
routes = solver.run_sa()
#print(routes)

# clusters = solver.cluster_algo(3)
# cluster_map = np.full((solver.max_width, solver.max_height), solver.base_value)
# i = 10
# for cluster in clusters:
#     for city in cluster:
#         cluster_map[solver.city_table[city][0]][solver.city_table[city][1]] = i
#     i+=1
# solver.plot_map(cluster_map)

