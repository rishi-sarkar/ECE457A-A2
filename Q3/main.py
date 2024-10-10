import csv
import random
import heapq
from collections import deque

#read flow distance data into matrix
with open('asignment-2-Distance.csv', newline ='') as csvfile:
    csvreader = csv.reader(csvfile)  # Create a reader object
    dist = list(csvreader)  # Convert to a list of lists

with open('assignment-2-Flow.csv', newline ='') as csvfile:
    csvreader = csv.reader(csvfile)  # Create a reader object
    flow = list(csvreader)  # Convert to a list of lists

#retrieve cost of a given permutation (represented as a list)
def cost(solution) -> int:
    cost = 0
    for i in range(20):
        for j in range(20):
            cost+= int(dist[i][j])*int(flow[solution[i]][solution[j]])

    return cost
            
class Swap:
    def __init__(self, swap, sol) -> None:
        
        self.swap = swap
        self.sol = sol.copy()
        index1 = self.sol.index(swap[0])
        index2 = self.sol.index(swap[1])

        self.sol[index1] = swap[1]
        self.sol[index2] = swap[0]

        self.cost = cost(self.sol)

    def __lt__(self, other) -> bool:
        return self.cost < other.cost

def tabu_search():

    swaps_made = []
    aspiration = False
    frequency = False

    #creates a list from 0 to 19 in random order
    curr_sol = random.sample(range(20), 20)
    curr_cost = cost(curr_sol)

    best_sol = curr_sol
    best_cost = curr_cost

    print(f"starting solution: {curr_sol}")
    print(f"starting cost: {cost(curr_sol)}")
     
    #matrix with values for swaps and their tenure 
    tabu_list = deque()
    frequency_list = {}
    tabu_size = 3
    max_freq = 5
    dynamic_tabu_sizes = range(1,20)
    iterations = 0

    while(iterations < 100):

        #create a new neighborhood of potential swaps
        neighborhood = []
        for i in range(19):
            for j in range(i+1,20):
                neighborhood.append(Swap((i, j), curr_sol))

        #random selection of only 50 out of the 190 neighborhoods
        sample_size = 20
        random_sample = random.sample(range(len(neighborhood)), sample_size)
        for n, k in enumerate(random_sample):
            neighborhood[n] = neighborhood[k]
        neighborhood = neighborhood[:sample_size]

        #find the swap that results in the lowest cost
        heapq.heapify(neighborhood)
        prospect = heapq.heappop(neighborhood)

        #if aspiration is true, continue under the condition the best prospect is better than the best cost yet
        if aspiration and prospect.cost < best_cost:
            pass

        #if frequency is true, find the best swap that has a frequency less than 5 and is also not on tabu list
        elif frequency:
            while(prospect is not None and (frequency_list.get(prospect.swap,0) > max_freq or prospect.swap in tabu_list)):
                prospect = heapq.heappop(neighborhood) if neighborhood else None

        #normal condition: find best swap that is not on tabu list
        else:
            while (prospect is not None and prospect.swap in tabu_list):
                prospect = heapq.heappop(neighborhood) if neighborhood else None
        
        #if nothing can be found from the neighborhood, one of the 2 stopping criterion are hit
        if prospect is None:
            break
        
        #update current and all times solutions/costs
        curr_cost = prospect.cost
        curr_sol = prospect.sol
        if curr_cost < best_cost:
            best_cost = curr_cost
            best_sol = curr_sol

        #add the current candidate to the tabu list and make pop from list if necessary
        while(len(tabu_list) >= tabu_size):
            tabu_list.popleft()
        tabu_list.append(prospect.swap)

        #increment frequency list values
        frequency_list[prospect.swap] = frequency_list.get(prospect.swap,0) + 1
        
        #dynamic tabu list every 10 iterations
        # if iterations % 10 ==0:
        #     tabu_size= random.choice(dynamic_tabu_sizes)
        #     while(len(tabu_list) > tabu_size):
        #         tabu_list.popleft()

        iterations +=1
        #swaps_made.append(f"iteration:{iterations} swap1:{prospect.swap[0]} swap2:{prospect.swap[1]} new cost:{curr_cost}")

        
    print(f"final solution: {best_sol}")
    print(f"final cost: {best_cost}")
    #print(f"Frequency list:{frequency_list}")
    for swaps in swaps_made:
        print(swaps)

if __name__ == "__main__":
    tabu_search()


