import numpy as np
import matplotlib.pyplot as plt
import copy

from CreateModel import Model
from CreateTask import Task
from InitAnt import Ant
from CostFunction import tour_cost as CostFunction
from RouletteWheelSelection import roulette_wheel_selection as RouletteWheelSelection
from PlotAssignment import plot_assignments as PlotAssignment
from Distance import cal_3Ddistance as distance

def main():

    # Problem Definition
    load_var = False

    if load_var:
        save_model = np.load("modelTest1.npy", allow_pickle=True).item()
        model = save_model

        for i in range(model.M):
            if model.tasks[i].tc != 0:
                model.tasks = model.tasks[:i]
                model.D = model.D[:i, :i]
                break
        model.M = len(model.tasks)

    else:
        model = Model(4, 30)

    # ACO Parameters
    MaxIt = 500  # Maximum Number of Iterations
    nAnt = 30  # Number of Ants (Population Size)
    Q = 100
    tau0 = 10 * Q / (model.M * np.mean(model.D))  # Initial Phromone
    alpha = 1  # Phromone Exponential Weight
    beta = 1  # Heuristic Exponential Weight
    rho = 0.05  # Evaporation Rate

    # Initialization
    eta = np.zeros((model.M,model.M))
    for i in range(0,model.M):
        eta[i][i] = np.inf
        for j in range(i+1,model.M):
            eta[i][j] = 1/model.D[i][j]
            eta[j][i] = eta[i][j]

    tau = tau0*np.ones((model.M, model.M))  # Phromone Matrix

    # Init ant colony
    ant = []
    empty_ant = Ant([],np.inf)
    empty_ant.Tour = [-1]*model.N
    for i in range(0,nAnt):
        ant.append(empty_ant)

    # ACO Main Loop
    BestSol = copy.deepcopy(empty_ant)

    for it in range(1, MaxIt + 1):

        # new task comes
        new_task = False

        if not load_var:

            nt = np.random.rand()
            # nt = 1
            if it > MaxIt - 150:
                nt = 1
            if nt < 0.02:
                print("Added new task")
                new_task = True

                n_id = len(model.tasks) + 1

                model.tasks.append(Task(n_id, it, model.WORLD))
                model.M = model.M + 1

        elif model.M != save_model.M:
            if it == save_model.tasks[model.M+1].tc:
                print("New task comes")
                new_task = True
                new_task = save_model.tasks[model.M]
                model.tasks.append(new_task)
                model.M = model.M + 1

        if new_task:
            mean_tau = np.mean(tau)
            var_tau = np.var(tau)
            model.D = np.append(model.D,np.zeros((1,model.M-1)),0)
            model.D = np.append(model.D,np.zeros((model.M,1)),1)

            eta = np.append(eta,np.zeros((1,model.M-1)),0)
            eta = np.append(eta,np.zeros((model.M,1)),1)

            tau = np.append(tau,np.zeros((1,model.M-1)),0)
            tau = np.append(tau,np.zeros((model.M,1)),1)

            for i in range(0,model.M-1):

                model.D[model.tasks[-1].id-1][i] = distance(model.tasks[i],model.tasks[-1])
                model.D[i][model.tasks[-1].id-1] = model.D[model.tasks[-1].id-1][i]

                eta[model.tasks[-1].id-1][i] = 1 / model.D[model.tasks[-1].id-1][i]
                eta[i][model.tasks[-1].id-1] = 1 / model.D[i][model.tasks[-1].id-1]

                tau[model.tasks[-1].id-1][i] = tau0 + np.random.randn() * var_tau
                tau[i][model.tasks[-1].id-1] = tau0 + np.random.randn() * var_tau

            BestSol.Cost = CostFunction(BestSol,model)

        # Move Ants, find solutions for each ant
        for k in range(nAnt):
            assigned = []
            ant[k].Tour = [-1]*model.N

            # Get a random tasks for the first        
            idx = 0
            while idx < len(ant[k].Tour):
                if ant[k].Tour[idx] == -1:
                    check_task = False
                    while not check_task:
                        rand_task = np.random.randint(1,model.M+1)
                        check_task = True
                        if rand_task in ant[k].Tour:
                            check_task = False
                    ant[k].Tour.insert(idx+1,rand_task)
                    assigned.append(rand_task)
                idx += 1

            # For in unassigned tasks
            while (model.M-len(assigned)) != 0:
                
                index = 0
                # for each ant
                while index < len(ant[k].Tour):

                    if (model.M-len(assigned)) == 0:
                        break

                    if (ant[k].Tour[index] == -1 and index != 0) or index==len(ant[k].Tour)-1:
                        P = np.zeros((model.M))

                        if index<len(ant[k].Tour)-1:
                            last_task = ant[k].Tour[index-1]  # get the final vertex
                        else:
                            last_task = ant[k].Tour[index]  # get the final vertex
                        if last_task == -1:
                            raise Exception("This agent is not assigned to any task")

                        for id in range(0,model.M):
                            if id+1 == last_task:
                                P[id] == 0
                            else:
                                P[id] = tau[last_task-1,id]**alpha*eta[last_task-1,id]**beta  # the probability of next point
                        
                        # the visited vertex have prob 0
                        for assigned_element in range(0,len(assigned)):
                            P[assigned[assigned_element]-1] = 0

                        P = P/np.sum(P)

                        j = RouletteWheelSelection(P)

                        assigned.append(j+1)    # j is the index of the task, j+1 is the task id

                        if index==len(ant[k].Tour)-1:
                            ant[k].Tour.append(j+1)
                        else:
                            ant[k].Tour.insert(index,j+1)
                        index += 1
                    index += 1                  

            ant[k].Cost = CostFunction(ant[k], model)
            
            if ant[k].Cost < BestSol.Cost:
                BestSol.Tour = np.copy(ant[k].Tour)
                BestSol.Cost = ant[k].Cost

        # Update Phromones
        for k in range(nAnt):
            tour = []

            for i in range(1, len(ant[k].Tour)):
                if ant[k].Tour[i] != -1:
                    tour.append(ant[k].Tour[i])

            for l in range(len(tour)-1):

                i = int(tour[l])
                j = int(tour[l+1])

                tau[i-1][j-1] = tau[i-1][j-1] + Q/ant[k].Cost

        # Evaporation
        tau = (1-rho)*tau

        # Show Iteration Information
        assigned_task = len(BestSol.Tour)-model.N

        print(f'Iteration {it}: Best Cost = {BestSol.Cost}, model.M {model.M}, assigned {assigned_task}')


    # Results
    # PlotAssignments(model, BestSol["agent"])
    # close(video)

    # plt.figure()
    PlotAssignment(model, BestSol)
    # plt.show()

    # plt.figure()
    # plt.plot([sol.Cost for sol in BestSol], linewidth=2)
    # plt.xlabel('Iteration')
    # plt.ylabel('Best Cost')
    # plt.grid(True)
    # plt.show()

if __name__=="__main__": 
    main() 
    