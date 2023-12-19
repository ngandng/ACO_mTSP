
clc;
clear;
close all;

%% Problem Definition

loadVar = true;

if loadVar
    load("modelTest3.mat");

    D = zeros(model.M,model.M);  % distance between two vertex

    for i=1:model.M-1
        for j=i+1:model.M
            delta_x = model.tasks(i).x-model.tasks(j).x;
            delta_y = model.tasks(i).y-model.tasks(j).y;
            delta_z = model.tasks(i).z-model.tasks(j).z;

            D(i,j)=sqrt((delta_x)^2+(delta_y)^2+(delta_z)^2);
            
            D(j,i)=D(i,j);
            
        end
    end

    model.D = D;

else
    model = CreateModel();
end


CostFunction = @(tour) TourCost(tour,model);

nVar = model.M;   % Searching dimension, number of tasks
nAgent = model.N;

%% ACO Parameters

MaxIt = 300;      % Maximum Number of Iterations

nAnt = 50;        % Number of Ants (Population Size)

Q = 1;

tau0 = 10*Q/(nVar*mean(model.D(:)));	% Initial Phromone

alpha = 1;        % Phromone Exponential Weight
beta = 1;         % Heuristic Exponential Weight

rho = 0.05;       % Evaporation Rate


%% Initialization

eta = 1./model.D;             % Heuristic Information Matrix, 1/distance

tau = tau0*ones(nVar,nVar);   % Phromone Matrix

BestCost = zeros(MaxIt,1);    % Array to Hold Best Cost Values

% Empty Ant
% empty_ant.agent = [];
empty_ant.Cost = [];

% Ant Colony Matrix
ant = repmat(empty_ant,nAnt,1);

% Best Ant
BestSol.Cost = inf;

%% need to revise part
% cost function
% 

%% ACO Main Loop

for it=1:MaxIt
    
    % Move Ants, find solutions
    for k=1:nAnt
        assigned = [];

        for agn = 1:nAgent
            ant(k).agent(agn).Tour = randi([1 nVar]); % get the random tasks for the first
            assigned = [assigned ant(k).agent(agn).Tour];
        % ant(k).Tour = 1;
        end

        for l=1:nVar    % finish assigning when all of task are assigned

            for ag = 1:nAgent
                i = ant(k).agent(ag).Tour(end); % get the final vertex
                
                P=tau(i,:).^alpha.*eta(i,:).^beta; % the probability of next point
                
                P(assigned)=0; % the visited vertex have prob 0
                
                P=P/sum(P);
                
                j=RouletteWheelSelection(P);
                
                assigned = [assigned j];

                ant(k).agent(ag).Tour=[ant(k).agent(ag).Tour j];
            end
            
        end 
        
        ant(k).Cost=CostFunction(ant(k));
        
        if ant(k).Cost<BestSol.Cost
            BestSol=ant(k);
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
    
    % Store Best Cost
    BestCost(it)=BestSol.Cost;
    
    % Show Iteration Information
    disp(['Iteration ' num2str(it) ': Best Cost = ' num2str(BestCost(it))]);
end

%% Results

% stl = ReadSTLModel1();
% PlotSTL(stl);
PlotAssignments(model,BestSol,1);
% hold off;
% 
figure;
plot(BestCost,'LineWidth',2);
xlabel('Iteration');
ylabel('Best Cost');
grid on;
