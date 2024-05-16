
import os
import numpy as np
import concurrent.futures
import random

from plot_assignment import display_assignment

def roulette_wheel_selection(P):
    r = random.random()
    C = [sum(P[:i + 1]) for i in range(len(P))]

    for j, c in enumerate(C):
        if r <= c:
            return j

def read_txt_file(filename):
    input_data = {}

    vertices = []
    list_demand = []
    num_depot = 0              # number of depot
    C = 0               # capacity

    coor_section = False
    demand_section = False
    depot_section = False


    current_path = os.path.dirname(__file__) 

    # Navigate up one level to the project root folder
    project_root = os.path.abspath(os.path.join(current_path, '..'))
    # Construct the path to the file you want to read
    file_path = os.path.join(project_root, 'test_instance', filename)

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('CAPACITY'):
                parts = line.split(':')
                C = int(parts[1].strip())
            if line.strip() == 'EOF':
                break
            if line.strip() == 'NODE_COORD_SECTION':
                coor_section = True
            if line.strip() == 'DEMAND_SECTION':
                coor_section = False
                demand_section = True
            if line.strip() == 'DEPOT_SECTION':
                demand_section = False
                depot_section = True
            if line[0].isalpha():
                continue
            parts = line.split()
            if coor_section:
                id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                vertices.append([id,x,y])
            if demand_section:
                id = int(parts[0])
                demand = int(parts[1])
                list_demand.append(demand)
            if depot_section:
                # print('Number of vertices = ', len(vertices))
                num_depot = int(parts[0])
                break

    input_data["vertices"] = vertices
    input_data["num_depot"] = num_depot
    input_data["demand"] = list_demand
    input_data["vehicle_capacity"] = C
    return input_data

def twoOpt(sub_tour,distance_matrix):
    new_tour = sub_tour
    del_cost = 0

    l = len(sub_tour)

    for i in range(l-2):
        for j in range(i+1,l-1):
            x1 = new_tour[i]
            x2 = new_tour[i+1]
            y1 = new_tour[j]
            y2 = new_tour[j+1]

            x1x2 = distance_matrix[x1,x2]
            y1y2 = distance_matrix[y1,y2]

            x1y1 = distance_matrix[x1,y1]
            x2y2 = distance_matrix[x2,y2]

            delta = x1y1 + x2y2 - x1x2 - y1y2

            if delta < 0:
                temp_tour = new_tour[:i+1]
                temp_tour.extend(new_tour[j:i:-1])
                temp_tour.extend(new_tour[j+1:])

                new_tour = temp_tour

                del_cost += delta

    # print('newtour found by twoOpt ',new_tour)
    return new_tour, del_cost

def construct_route(tau,eta,alpha,beta,tabu_set,data):
    tour = []
    
    # tour.append(data["depot"][0]) # the case of only one depot
    tour.append(0)                  # the case of only one depot

    current_idx = tour[0]

    C = data["vehicle_capacity"]

    dt = 0                          # total demand of the tour
    sub_cost = 0                    # length of subtour

    vertices_id = [i for i in range(len(data["demands"]))]

    ic = 0
    while(C-dt>0):
        if(len(tabu_set)<=0):
            break
        ic += 1
        if(ic>100):
            raise MemoryError("Error in while loop of construct_route function")
        
        # P is possibility value to chose next task
        # Calculate (tau[current_idx,i]**alpha)*(eta[current_idx,i]**beta) for the entire array
        # print('Check tau ', tau[current_idx,:])
        # print('Check eta ', eta[current_idx,:])
        P = (tau[current_idx,:] ** alpha) * (eta[current_idx,:] ** beta)
        # print('Check P ', P)
        P[current_idx] = 0

        # print('Check P ', P)

        # Set P to 0 where vertex_id is not in tabu_set
        not_in_tabu= [vertex_id for vertex_id in vertices_id if vertex_id not in tabu_set]
        P[not_in_tabu] = 0
        # Set P to 0 where demand exceeds capacity
        demand_exceeds_capacity = np.array([demand > (C - dt) for demand in data["demands"]])
        P[demand_exceeds_capacity] = 0
        
        if np.sum(P) == 0:
            break

        P /= np.sum(P)

        j = roulette_wheel_selection(P)

        dt += data["demands"][j]

        if dt > C:
            dt -= data["demands"][j]
            break

        sub_cost += data["distance_matrix"][current_idx,j]
        # tour.append(data["depot"][j])
        # tabu_set.remove(data["depot"][j])
        tour.append(j)
        tabu_set.remove(j)

        current_idx = j

    # after full the demand, robot come back to the depot   
    tour.append(tour[0])
    sub_cost = sub_cost+data["distance_matrix"][current_idx,tour[-1]]
    new_tour, del_c = twoOpt(tour,data["distance_matrix"])
    tour = new_tour
    sub_cost -= del_c

    # apply two-opt local search here

    return tour, tabu_set, dt, sub_cost

def construct_solution(tau,eta,alpha,beta,data):                   # construction solution based on tau matrix, input position
    tabu_set = []
    demand_list = []

    # print("Number of depot: ",len(data["depot"]))

    for i in range(len(data["depot"]),len(data["demands"])):
        tabu_set.append(i)      # Error here --> check more for consistency

    # print("Initial tabu set: ",tabu_set)

    v_count = 0         # number of route
    c_total = 0         # total cost
    R_list = []         # list of route

    i_check = 0
    while(len(tabu_set)>0):
        # construct route based on C
        subtour,tabu_set,sub_demand,sub_cost = construct_route(tau,eta,alpha,beta,tabu_set,data)
        # print("New subtour", subtour)
        R_list.append(subtour)
        v_count += 1
        c_total += sub_cost
        demand_list.append(sub_demand)

        i_check += 1
        if(i_check>100):
            print("Tabu set: ", tabu_set)
            print("Current best solution: ", R_list)
            raise MemoryError("Error in while loop of construct_solution function")
    
    return R_list,v_count,c_total,demand_list

def cal_searching_data(input_data):
    data = {}

    N = len(input_data["vertices"])

    # matrix of distance
    D = np.zeros((N,N))
    for i in range(N-1):
        for j in range(i+1,N):
            dx = input_data["vertices"][i][1]-input_data["vertices"][j][1]
            dy = input_data["vertices"][i][2]-input_data["vertices"][j][2]
            D[i,j] = np.sqrt(dx**2+dy**2)
            D[j,i] = D[i,j]
            # print(f'Distance between two vertices {i} and {j} = {D[i,j]}')

    # demands for each node
    data["demands"] = input_data["demand"]
    # vehicle capacity
    data["vehicle_capacity"] = input_data["vehicle_capacity"]
    # id of depot
    data["depot"] = [input_data["vertices"][i][0] for i in range(input_data["num_depot"])]

    data["distance_matrix"] = D

    return data

def print_bestsol(sol,best_num_vehicle,best_dmlist,best_cost,data):
    routes = []
    for i in range(len(sol)):
        tempt = []
        for j in range(len(sol[i])):
            tempt.append(data["vertices"][sol[i][j]][0])
        routes.append(tempt)

    print(f'Best solution with {best_num_vehicle} routes')
    for i in range(len(routes)):
        print(f'route {i}: ',routes[i],'\n')
    print('Demand list: ',best_dmlist)
    print('Best cost = ',best_cost)


def aco_search(searching_data, maxIt):  

    # ACO parameters
    nAnt = 10
    Q = 1           # pheromone quantity parameter

    # tau0 = Q/(N*np.mean(D))
    tau0 = Q/(np.mean(searching_data["distance_matrix"]))
    alpha = 1
    beta = 1
    rho = 0.05      # evaporation rate

    eta = np.zeros((N,N))
    for i in range(N):
        eta[i,i] = np.inf
        for j in range(i+1,N):
            eta[i,j] = 1/searching_data["distance_matrix"][i,j]
            eta[j,i] = eta[i,j]
    
    tau = tau0*np.ones((N,N))

    # aco main loop
    best_sol = []
    best_num_vehicle = 0
    best_cost = np.inf
    best_dmlist = []

    for iter in range(maxIt):
        ############ sequential version ################
        # for _ in range(nAnt):
        #     sol, v_count, cost, demand_list = construct_solution(tau,eta,alpha,beta,vertices,num_depot,C)

        #     if cost < best_cost:
        #         print(f'Found a better solution by ants with cost {cost}')
        #         best_sol = sol
        #         best_num_vehicle = v_count
        #         best_cost = cost
        #         best_dmlist = demand_list

        ############# coarse-grain master slave parallel version ###################
        with concurrent.futures.ProcessPoolExecutor() as executor:
            ants = [executor.submit(construct_solution,tau,eta,alpha,beta,searching_data) for _ in range(nAnt)]

            for f in concurrent.futures.as_completed(ants):
                sol, v_count, cost, demand_list = f.result()

                # print(f'new solution found with cost {cost}')

                if cost < best_cost:
                    print(f'Found a better solution by ants with cost {cost}')
                    best_sol = sol
                    best_num_vehicle = v_count
                    best_cost = cost
                    best_dmlist = demand_list
        # apply local search
        
        # update pheromone matrix as bestsol
        for i in range(len(best_sol)):
            for j in range(len(best_sol[i])-1):
                # if(best_sol[i][j] < num_depot):
                #     continue
                node_a = int(best_sol[i][j])
                node_b = int(best_sol[i][j+1])

                tau[node_a][node_b] = tau[node_a][node_b] + Q/best_cost
        # evaporation
        tau = (1-rho)*tau
        # print iteration performance
        print('Iteration ',iter,' best cost ',best_cost)

    # Print
    print_bestsol(best_sol,best_num_vehicle,best_dmlist,best_cost,input_data)

    # plot
    display_assignment(input_data,best_sol)
        
    return best_sol, best_num_vehicle, best_cost
        
if __name__=="__main__":

    files = ['P-n22-k8.txt','P-n23-k8.txt','P-n45-k5.txt','P-n50-k8.txt','P-n55-k8.txt','P-n60-k15.txt','P-n65-k10.txt',
             'X-n115-k10.txt', 'X-n200-k36.txt', 'X-n351-k40.txt', 'X-n480-k70.txt', 'X-n701-k44.txt']
    filename = files[7]

    maxIt = 500

    # process the information of input file, generate the problem input
    input_data = read_txt_file(filename)

    print('Number of depot = ',input_data["num_depot"])
    print('Tasks size ',len(input_data["vertices"])-input_data["num_depot"])

    N = len(input_data["vertices"])

    print('N = ',N)

    for i in range(N):
        print(f'Vertice: {input_data["vertices"][i][0]}, coordination: x = {input_data["vertices"][i][1]}, y = {input_data["vertices"][i][2]}, demand = {input_data["demand"][i]}')

    searching_data = cal_searching_data(input_data)

    sol,num_veh,cost = aco_search(searching_data,maxIt)