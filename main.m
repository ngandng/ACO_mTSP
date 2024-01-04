
clc;
clear;
close all;

%% Problem Definition

loadVar = false;
currentTasks = [];

if loadVar
    load("scenario1.mat");
    
    for i = 1:model.M
        if model.tasks(i).tc ~= 0
            break;
        end
        currentTasks = [currentTasks model.tasks(i)];
    end

else
    model = CreateModel();
    currentTasks = model.tasks;
end


CostFunction = @(tour,env) TourCost(tour,env);

nVar = model.M;   % Searching dimension, number of tasks
nAgent = model.N;

%% ACO Parameters

MaxIt = 700;      % Maximum Number of Iterations

nAnt = 50;        % Number of Ants (Population Size)

Q = 1;

tau0 = 10*Q/(nVar*mean(model.D(:)));	% Initial Phromone

alpha = 1;        % Phromone Exponential Weight
beta = 1;         % Heuristic Exponential Weight

rho = 0.05;       % Evaporation Rate


%% Initialization

eta = 1./model.D;             % Heuristic Information Matrix, 1/distance

tau = tau0*ones(nVar,nVar);   % Phromone Matrix

% BestCost = zeros(MaxIt,1);    % Array to Hold Best Cost Values

% Empty Ant
% empty_ant.agent = [];
empty_ant.Cost = [];

% Ant Colony Matrix
ant = repmat(empty_ant,nAnt,1);

myFig = figure(3);
video = VideoWriter('result2.avi','Motion JPEG AVI');
video.FrameRate = 20;  % (frames per second) this number depends on the sampling time and the number of frames you have
open(video);

%% ACO Main Loop

for it=1:MaxIt
    
    if it == 1
        BestSol(it).Cost = Inf;
    else
        BestSol(it).agent = BestSol(it-1).agent;
        BestSol(it).Cost = CostFunction(BestSol(it),model);
    end

    % new task comes
    newtask = false;
    
    % % ======This is for random new task======
    nt = rand();
    if it > MaxIt-150
        nt = 1;
    end
    if nt < 0.02
        % add new task
        disp("Added new task");
        newtask = true;

        n_id = length(model.tasks)+1;
        new_task = CreateTask(n_id,it,model.WORLD);

        model.tasks = [model.tasks new_task];
        model.M = model.M+1;

    end

    % % ========This is for new task from data=======
    % %  write code here
    
    
    % %  ======Update something when new tasks come======
    if newtask 

        mean_tau = mean(tau, 'all');
        var_tau = var(tau, 0, 'all');

        for i=1:model.M
            delta_x = model.tasks(i).x-new_task.x;
            delta_y = model.tasks(i).y-new_task.y;
            delta_z = model.tasks(i).z-new_task.z;

            model.D(n_id,i) = sqrt(delta_x^2+delta_y^2+delta_z^2);
            model.D(i,n_id) = model.D(n_id,i);

            eta(n_id,i) = 1/model.D(n_id,i);
            eta(i,n_id) = 1/model.D(i,n_id);

            tau(n_id,i) = tau0+randn()*var_tau;
            tau(i,n_id) = tau0+randn()*var_tau;
        end
        % Update nVar
        nVar = model.M;
    end


    % Move Ants, find solutions
    for k=1:nAnt
        assigned = [];

        % get a random tasks for the first
        for agn = 1:nAgent  
            check = false;
            while ~check
                ant(k).agent(agn).Tour = randi([1 nVar]); 
                dupl = intersect(ant(k).agent(agn).Tour,assigned);
                if isempty(dupl)
                    check = true;
                end
            end
            assigned = [assigned, ant(k).agent(agn).Tour];
        end

        for l=1:nVar    % finish assigning when all of task are assigned

            for ag = 1:nAgent
                i = ant(k).agent(ag).Tour(end); % get the final vertex
                
                P=tau(i,:).^alpha.*eta(i,:).^beta; % the probability of next point
                
                P(assigned)=0; % the visited vertex have prob 0
                
                P=P/sum(P);
                
                j=RouletteWheelSelection(P);
                
                assigned = [assigned, j];

                ant(k).agent(ag).Tour=[ant(k).agent(ag).Tour j];
            end
            
        end 
        
        ant(k).Cost=CostFunction(ant(k),model);
        
        if ant(k).Cost<BestSol(it).Cost
            BestSol(it).agent = ant(k).agent;
            BestSol(it).Cost = ant(k).Cost;
        end
        
    end
    
    % Update Phromones
    for k=1:nAnt
        tour = [];

        for p = 1:nAgent
            tour = [tour ant(k).agent(p).Tour];
        end
        
        % tour=[tour tour(1)]; %#ok
        
        for l=1:length(tour)-1
            
            i=tour(l);
            j=tour(l+1);
            
            tau(i,j)=tau(i,j)+Q/ant(k).Cost;
            
        end
        
    end
    
    % Evaporation
    tau=(1-rho)*tau;
    
    % % Store Best Cost
    % BestCost(it)=BestSol.Cost;
    
    assignedTask = 0;
    for ag = 1:model.N
        assignedTask = assignedTask + length(BestSol(it).agent(ag).Tour);
    end

    % Show Iteration Information
    disp(['Iteration ' num2str(it) ': Best Cost = ' num2str(BestSol(it).Cost) ', model.M ' num2str(model.M), ', assigned ' num2str(assignedTask)]);

    % plot
    PlotAssignments(model,BestSol(it));
    Frame = getframe(myFig);
    writeVideo(video,Frame);

end

% Results
figure();
PlotAssignments(model,BestSol(end));
close(video);


figure;
plot(BestSol(:).Cost,'LineWidth',2);
xlabel('Iteration');
ylabel('Best Cost');
grid on;
