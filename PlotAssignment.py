
import matplotlib.pyplot as plt
import numpy as np
# from mpl_toolkits.mplot3d import axes3d, Axes3D

def plot_assignments(model, sol):

    offset = (model.WORLD.XMAX - model.WORLD.XMIN) / 100
    Cmap = plt.cm.get_cmap('tab10')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for m_task in range(0,model.M):
        # ax.scatter(model.tasks[m_task].x, model.tasks[m_task].y, model.tasks[m_task].z, 'o-', color='g', markersize=7, markerfacecolor='g')
        ax.scatter(model.tasks[m_task].x, model.tasks[m_task].y, model.tasks[m_task].z, c='g')
        ax.text(model.tasks[m_task].x+offset, model.tasks[m_task].y+offset, model.tasks[m_task].z+offset, f'T{model.tasks[m_task].id}')

    n = 0       # the current agent
    icre = 0    # the current position in tour 

    while n <= model.N and icre < len(sol.Tour):
        # print('icre = ', icre, ', n = ', n)
        if sol.Tour[icre] == -1:

            if icre != 0:

                X = np.array([model.agents[n-1].x, model.tasks[sol.Tour[icre-1]-1].x])
                Y = np.array([model.agents[n-1].y, model.tasks[sol.Tour[icre-1]-1].y])
                # Z = np.zeros_like(X)
                Z = np.array([model.agents[n-1].z, model.tasks[sol.Tour[icre-1]-1].z])

                ax.plot3D(X, Y, Z, linestyle='-', color=Cmap(n), linewidth=2)
                # print('1. Plot the connection from agent ', n, ' to task ', sol.Tour[icre-1])

            n += 1

            # ax.plot3D(model.agents[n].x, model.agents[n].y, 0, 'o-', color=Cmap(n), markersize=10, markerfacecolor=Cmap(n))
            ax.scatter(model.agents[n-1].x, model.agents[n-1].y, model.agents[n-1].z, color=Cmap(n),s =40)
            ax.text(model.agents[n-1].x+offset, model.agents[n-1].y+offset, model.agents[n-1].z+offset, f'A{n}')

            # icre += 1

        else:   

            if sol.Tour[icre-1] == -1:  # if the prev position is -1, connect task with agent

                X = np.array([model.agents[n-1].x, model.tasks[sol.Tour[icre]-1].x])
                Y = np.array([model.agents[n-1].y, model.tasks[sol.Tour[icre]-1].y])
                # Z = np.zeros_like(X)
                Z = np.array([model.agents[n-1].z, model.tasks[sol.Tour[icre]-1].z])

                ax.plot3D(X, Y, Z, linestyle='-', color=Cmap(n), linewidth=2)
                # print('2. Plot the connection from agent ', n, ' to task ', sol.Tour[icre])

            else:                       # if the prev position is not -1, connect task with prev task

                X = np.array([model.tasks[sol.Tour[icre]-1].x, model.tasks[sol.Tour[icre-1]-1].x])
                Y = np.array([model.tasks[sol.Tour[icre]-1].y, model.tasks[sol.Tour[icre-1]-1].y])
                # Z = np.zeros_like(X)
                Z = np.array([model.tasks[sol.Tour[icre]-1].z, model.tasks[sol.Tour[icre-1]-1].z])

                ax.plot3D(X, Y, Z, linestyle='-', color=Cmap(n), linewidth=2)

                # print('3. Plot the connection from task ', sol.Tour[icre-1], ' to task ', sol.Tour[icre])

                if icre == len(sol.Tour)-1:

                    X = np.array([model.agents[n-1].x, model.tasks[sol.Tour[icre]-1].x])
                    Y = np.array([model.agents[n-1].y, model.tasks[sol.Tour[icre]-1].y])
                    # Z = np.zeros_like(X)
                    Z = np.array([model.agents[n-1].z, model.tasks[sol.Tour[icre]-1].z])

                    ax.plot3D(X, Y, Z, linestyle='-', color=Cmap(n), linewidth=2)
                    # print('3.5 Plot the connection from agent ', n, ' to task ', sol.Tour[icre])

        icre += 1

    ax.set_title('Agent Paths')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(True)
    plt.show()


def lookup_task(tasks, task_id):
    for task in tasks:
        if task.id == task_id:
            return task

    print(f'Task with index={task_id} not found')
    return None