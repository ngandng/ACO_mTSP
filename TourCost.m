
function L=TourCost(ant,model)

    n_agent = length(ant.agent);

%     tour=[tour tour(1)];
    
    L1=0; % Cost for length of path

    for i = 1:n_agent
        ntask = length(ant.agent(i).Tour); % number of tasks per agent

        startPos = model.agents(i);
        task1 = model.tasks(ant.agent(i).Tour(1));
        L1 = L1 + sqrt((startPos.x-task1.x)^2+(startPos.y-task1.y)^2+(startPos.z-task1.z)^2);

        for j = 2:ntask-1
            L1 = L1 + model.D(ant.agent(i).Tour(j),ant.agent(i).Tour(j+1));
        end
        
        task_end = model.tasks(ant.agent(i).Tour(end));
        L1 = L1 + sqrt((startPos.x-task_end.x)^2+(startPos.y-task_end.y)^2+(startPos.z-task_end.z)^2);
    end

    
    L = L1;
end