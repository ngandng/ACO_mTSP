import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.art3d import Line3D
import numpy as np

def display_assignment(input_data,solution):

    plt.figure()
    Cmap = plt.cm.get_cmap('tab20')

    lines = []  # List to store Line3D objects for legend

    vertices = input_data["vertices"]
    demands = input_data["demand"]

    # for i in range(0, len(vertices)):
    #     plt.scatter(vertices[i].x,vertices[i].y,c='g')

    for i in range(len(solution)):
        route = solution[i]

        plan_output = f"Route {i}:\n"
        route_distance = 0
        route_load = 0    

        for j in range(len(route)-1):
            a = route[j]
            b = route[j+1]
            
            route_load += demands[a]

            distance_ab = abs(vertices[a][1]-vertices[b][1]) + abs(vertices[a][2]-vertices[b][2])
            route_distance += distance_ab

            plt.scatter(vertices[a][1],vertices[a][2],color=Cmap(i%20))
            plt.scatter(vertices[b][1],vertices[b][2],color=Cmap(i%20))
            X = [vertices[a][1],vertices[b][1]]
            Y = [vertices[a][2],vertices[b][2]]
            
            line = plt.plot(X, Y, linestyle='-', color=Cmap(i%20), linewidth=2)

            plan_output += f" {vertices[a][0]} Load({demands[a]}) -> "

        plan_output += f" {vertices[route[-1]][0]} Load({demands[a]})\n"

        lines.extend(line)
        

    plt.title('ACO Paths')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Add legend
    labeled_lines = [line for line in lines if not line.get_label().startswith('_')]
    plt.legend(handles=labeled_lines, loc='upper left')

    plt.draw()
    plt.show()
    plt.pause(50)

# Example usage
# plot_assignments(your_model, your_solution)