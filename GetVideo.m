
myFig = figure(3);
% set(gcf, 'Position', get(0, 'Screensize')); 

% Set plotting parameters
offset = (model.WORLD.XMAX - model.WORLD.XMIN)/100; 

Cmap   = colormap(lines);

linS = {'-','-.','--',':'};

m_tasks = model.tasks;

for iter=1:100

    % Plot tasks
    cla;
    hold on;

    sol = BestSol(iter);
    disp(['Plotting iteration ' num2str(iter)]);
    
    for m = 1:length(m_tasks)
        % plot3(m_tasks(m).x + [0 0], m_tasks(m).y + [0 0], [0 1],'square','color',Cmap(m_tasks(m).id,:),'LineWidth',10);
        plot3(m_tasks(m).x + [0 0], m_tasks(m).y + [0 0], m_tasks(m).z + [0 0] ,'o','color','g','MarkerSize',7,'MarkerFaceColor','g');
        text(m_tasks(m).x+offset, m_tasks(m).y+offset, 0.1, ['T' num2str(m)]);
        % num_req = m_tasks(m).req;
        % text(m_tasks(m).x-offset, m_tasks(m).y-offset, 0.1, ['(' num2str(num_req) ')']);
    end
    
    % Plot agents
    for n=1:length(model.agents)
    
        plot3(model.agents(n).x, model.agents(n).y, 0,'o','color',Cmap(model.agents(n).id,:),'MarkerSize',10,'MarkerFaceColor',Cmap(model.agents(n).id,:));
    
        text(model.agents(n).x+offset, model.agents(n).y+offset, 0.1, ['A' num2str(n)]);
    
        % Check if path has something in it
        if(~isempty(sol.agent(n).Tour))
    
            taskPrev = lookupTask(model.tasks, sol.agent(n).Tour(1)); % get the task information
    
            X = [model.agents(n).x, taskPrev.x];
            Y = [model.agents(n).y, taskPrev.y];
            Z = zeros(length(X));
    
            plot3(X,Y,Z,'linestyle',linS(n),'color',Cmap(model.agents(n).id,:),'LineWidth',2);
    
            % plot3(X(end)+[0 0], Y(end)+[0 0], Z(end)+[0 0], '^','color',Cmap(model.agents(n).id,:),'MarkerSize',10,'MarkerFaceColor',Cmap(model.tasks(n).id+5,:));
            text(model.agents(n).x+offset, model.agents(n).y+offset, 0.1, ['A' num2str(n)]);
    
            for m = 2:length(sol.agent(n).Tour)
                if( ~isempty(sol.agent(n).Tour(m)) && m > 1 )
    
                    taskNext = lookupTask(model.tasks, sol.agent(n).Tour(m));
                    X = [taskPrev.x, taskNext.x];
                    Y = [taskPrev.y, taskNext.y];
                    Z = zeros(length(X));
    
                    plot3(X,Y,Z,'linestyle',linS(n),'color',Cmap(model.agents(n).id,:),'LineWidth',2);
    
                    % plot3(X(end)+[0 0], Y(end)+[0 0], Z(end)+[0 0], '^','color',Cmap(model.agents(n).id,:),'MarkerSize',10,'MarkerFaceColor',Cmap(model.tasks(n).id+5,:));
    
                    taskPrev = taskNext;
    
                else
                    break;
                end
            end
    
            X = [taskPrev.x, model.agents(n).x];
            Y = [taskPrev.y, model.agents(n).y];
            Z = zeros(length(X));
    
            plot3(X,Y,Z,'linestyle',linS(n),'color',Cmap(model.agents(n).id,:),'LineWidth',2);
        end
    end
    
    % legend([agent_quad, agent_car, tasks_track, tasks_rescue], {'Quadrotors', 'Cars', 'Tracking tasks', 'Rescue tasks'}, 'Location', 'southwest');
    title('Agent Paths')
    xlabel('X');
    ylabel('Y');
    zlabel('Time');
    grid on;
    hold off;
    Frame(iter) = getframe(myFig);
end

video = VideoWriter('result.avi','Motion JPEG AVI');
video.FrameRate = 20;  % (frames per second) this number depends on the sampling time and the number of frames you have
open(video);
writeVideo(video,Frame);
close(video);

%% function
function task = lookupTask(tasks, taskID)

    for mi=1:length(tasks)
        if(tasks(mi).id == taskID)
            task = tasks(mi);
            return;
        end
    end
    
    task = [];
    disp(['Task with index=' num2str(taskID) ' not found']);

return

end