import math
import numpy as np
import sys
import random
import matplotlib.pyplot as plt

base_config = {
    'name': 'base_config',
    'alpha': 0.1,
    'initial_temp': 10000,
    'final_temp': 0.1,
    'max_stabilization_time': 100,
    'step_size': 0.0001,
    'initial_sol': [3,3],
    'temp_decrement_rule': 'linear'
}

class Question1():
    
    def __init__(self, is_debug=False):
        # Constructor params
        self.is_debug = is_debug
        
        # problem definition
        self.max_x = 100
        self.min_x = -100
        self.max_y = 100
        self.min_y = -100
        
        # annealing schedule
        self.alpha = 0.1                     # alpha parameter
        self.initial_temp = 10000             # initial temperature
        self.final_temp = 0.1                # final temperature
        self.max_stabilization_time =  1000       # number of iterations at each temperature
        self.step_size = 0.0001
        self.temp_decrement_rule = 'linear'
        
        # initial parameters
        self.initial_sol = [3,3]
        
        self.x_cache = []
        self.y_cache = []
        self.z_cache = []
    
    def set_params(self, params):
        self.alpha = params['alpha']                                        # alpha parameter
        self.initial_temp = params['initial_temp']                          # initial temperature
        self.final_temp = params['final_temp']                              # final temperature
        self.max_stabilization_time =  params['max_stabilization_time']     # number of iterations at each temperature
        self.step_size = params['step_size']                                # step size to take for neighbour generation
        self.initial_sol = params['initial_sol']
        self.temp_decrement_rule = params['temp_decrement_rule']
        self.name = params['name']
    
    def easom_function(self, x, y):
        return -math.cos(x) * math.cos(y) * math.exp(-(x-math.pi)**2 - (y-math.pi)**2)
    
    def cost_diff_function(self, z_old, z_new):
        # cost diff function is square error (negative -> trying to go uphill, positive -> trying to go downhill )
        return z_old - z_new
    
    def neighbourhood_generator(self, x, y, step):
        # generates neighbours based off current state and step amount
        neighbours = [[x+step,y], [x,y+step], [x-step,y], [x,y-step]]
        
        # filter states outside of define state space
        neighbours = list(filter(lambda state: state[0] <= self.max_x and state[0] >= self.min_x and state[1] <= self.max_y and state[1] >= self.min_y, neighbours))
        
        return neighbours
    
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
        
    
    def reset_caches(self):
        self.x_cache = []
        self.y_cache = []
        self.z_cache = []
    
    def run_solver(self):
        # set initial solution and temp
        self.curr_sol =  self.initial_sol
        self.curr_temp = self.initial_temp
        self.curr_stabilization = 0
        
        self.reset_caches()
        
        # continue process until final temp has been reached
        while(self.curr_temp > self.final_temp):

            # continue process until temperature has reached equilibrium in system
            while(self.curr_stabilization < self.max_stabilization_time):
                
                # generate neighbours
                neighbours = self.neighbourhood_generator(self.curr_sol[0], self.curr_sol[1], self.step_size)
                
                # pick a neighbour randomly
                candidate = neighbours[random.randint(0,len(neighbours)-1)]
                
                # calculate cost diff for new solution
                cost = self.cost_diff_function(self.easom_function(self.curr_sol[0], self.curr_sol[1]), self.easom_function(candidate[0], candidate[1]))
                
                # check if candidate is acceptable as new solution
                if(cost <= 0 or random.random() < self.random_decay(cost, self.curr_temp) ):
                    # cost diff is better with this candidate (z value is lower, meaning we are moving towards a minimum) 
                    # or random decay was successful
                    self.curr_sol = candidate
                    
                
                # increment stabilization time
                self.curr_stabilization +=1
                
            
            # decrease t using temp reduction function
            self.curr_temp =  self.temp_reduction_function(self.curr_temp)
            self.curr_stabilization = 0
            self.x_cache.append(self.curr_sol[0])
            self.y_cache.append(self.curr_sol[1])
            self.z_cache.append(self.easom_function(self.curr_sol[0], self.curr_sol[1]))
            
            # Print current state and temperature if requested
            if(self.is_debug):
                sys.stdout.write(f"Current Temperature: {self.curr_temp} | Current State: ({self.curr_sol[0]},{self.curr_sol[1]}) -> {self.easom_function(self.curr_sol[0], self.curr_sol[1])} \r")
                sys.stdout.flush()
                #print(f"Current Temperature: {self.curr_temp}")
                #print(f"Current State: ({self.curr_sol[0]},{self.curr_sol[1]}) -> {self.easom_function(self.curr_sol[0], self.curr_sol[1])}\n\n")
            
        
        print("\n\n\n---Solver Complete---")
        print(f"Final State: ({self.curr_sol[0]},{self.curr_sol[1]}) -> {self.easom_function(self.curr_sol[0], self.curr_sol[1])}")
        
        pass
    
    def save_plot(self):
        # Create a figure with two subplots (one above the other)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))  # 2 rows, 1 column

        # Top plot
        ax1.plot(self.x_cache, self.y_cache, marker='o', linestyle='-', color='blue')
        ax1.set_title(f'States explored starting at ({self.initial_sol[0]},{self.initial_sol[1]} with initial temp of {self.initial_temp})')
        ax1.set_xlabel('X State')
        ax1.set_ylabel('Y State')
        ax1.grid(True)
        
        # Bottom plot
        ax2.plot(self.z_cache, marker='o', linestyle='-', color='green')
        ax2.set_title('Objective Function over Time')
        ax2.set_xlabel('Iteration #')
        ax2.set_ylabel('Easom Function Value')
        ax2.grid(True)

        # Display the plots
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.savefig(f'{self.name}.png')
        if(self.is_debug):
            plt.show()


solver = Question1(True)

test_config = {
    'name': 'test_config',
    'alpha': 0.1,
    'initial_temp': 10000,
    'final_temp': 20,
    'max_stabilization_time': 100,
    'step_size': 0.0001,
    'initial_sol': [3,3],
    'temp_decrement_rule': 'linear'
}


solver.set_params(base_config)
solver.run_solver()
solver.save_plot()


# Experiment 1
# for i in range(1,11):
#     new_config = dict(base_config)
    
#     new_config['name'] = f'exp1-{i}'
#     new_config['initial_sol'] = [random.randint(solver.min_x,solver.max_x), random.randint(solver.min_y,solver.max_y)]
    
#     solver.set_params(new_config)
#     solver.run_solver()
#     solver.save_plot()


# Experiment 2
# reasonable_initial_temps = [1000, 10000, 20000, 60000, 15000, 30000, 50000, 8000, 90000, 7000]
# for i in range(1,11):
#     new_config = dict(base_config)
    
#     new_config['name'] = f'exp2-{i}'
#     new_config['initial_temp'] = reasonable_initial_temps[i-1]
    
#     solver.set_params(new_config)
#     solver.run_solver()
#     solver.save_plot()
    
# Experiment 3
# annealing_schedules = [
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": base_config["max_stabilization_time"], "temp_decrement_rule":base_config["temp_decrement_rule"], "alpha": base_config["alpha"]}, # base config
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": base_config["max_stabilization_time"], "temp_decrement_rule":base_config["temp_decrement_rule"], "alpha": 0.3},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": 1000, "temp_decrement_rule":base_config["temp_decrement_rule"], "alpha": base_config["alpha"]},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": base_config["max_stabilization_time"], "temp_decrement_rule":"geometric", "alpha": base_config["alpha"]},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": base_config["max_stabilization_time"], "temp_decrement_rule":"geometric", "alpha": 0.96},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": base_config["max_stabilization_time"], "temp_decrement_rule":"geometric", "alpha": 0.85},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": 1000, "temp_decrement_rule":"geometric", "alpha": base_config["alpha"]},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": 1, "temp_decrement_rule":"slow_decrease", "alpha": base_config["alpha"]},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": 1, "temp_decrement_rule":"slow_decrease", "alpha":0.3},
#     {"final_temp": base_config["final_temp"], "max_stabilization_time": 1, "temp_decrement_rule":"slow_decrease", "alpha":0.6},
# ]

# for i in range(1, len(annealing_schedules)):
#     new_config = dict(base_config)
    
#     new_config['name'] = f'exp3-{i}'
#     new_config['final_temp'] = annealing_schedules[i-1]['final_temp']
#     new_config['max_stabilization_time'] = annealing_schedules[i-1]['max_stabilization_time']
#     new_config['temp_decrement_rule'] = annealing_schedules[i-1]['temp_decrement_rule']
#     new_config['alpha'] = annealing_schedules[i-1]['alpha']
    
#     solver.set_params(new_config)
#     solver.run_solver()
#     solver.save_plot()