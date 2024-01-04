
function L=TourCost(ant,model)

    n_agent = length(ant.agent);

%     tour=[tour tour(1)];
    %% Cost for length of path and longest tour
    L1 = 0; 
    L3 = 0;
    for i = 1:n_agent
        a_tour = 0; %length of agent tour

        ntask = length(ant.agent(i).Tour); % number of tasks per agent

        startPos = model.agents(i);
        task1 = model.tasks(ant.agent(i).Tour(1));
        a_tour = a_tour + sqrt((startPos.x-task1.x)^2+(startPos.y-task1.y)^2+(startPos.z-task1.z)^2);

        for j = 2:ntask-1
            a_tour = a_tour + model.D(ant.agent(i).Tour(j),ant.agent(i).Tour(j+1));
        end
        
        task_end = model.tasks(ant.agent(i).Tour(end));
        a_tour = a_tour + sqrt((startPos.x-task_end.x)^2+(startPos.y-task_end.y)^2+(startPos.z-task_end.z)^2);

        L1 = L1+a_tour;

        if a_tour > L3
            L3 = a_tour;
        end
    end

    %% Cost for number of task assigned
    
    ntask = 0; % total number of assigned tasks
    for i = 1:n_agent
        na = length(ant.agent(i).Tour); % number of tasks per agent

        ntask = ntask+na;
    end
    L2 = model.M - ntask;
    % disp(['model.m: ' num2str(model.M) 'ntask' num2str(ntask)])
  
    L = L1 + 150*L2 + 3*L3;
end