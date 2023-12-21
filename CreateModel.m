% Create model

function model = CreateModel()
    %---------------------------------------------------------------------%
    % Initialize global variables
    %---------------------------------------------------------------------%
    
    WORLD.CLR  = rand(100,3);
    
    WORLD.XMIN = 0;
    WORLD.XMAX =  250;
    WORLD.YMIN = 0;
    WORLD.YMAX =  250;
    WORLD.ZMIN =  0.0;
    WORLD.ZMAX =  2.0;
    WORLD.MAX_DISTANCE = sqrt((WORLD.XMAX - WORLD.XMIN)^2 + ...
                              (WORLD.YMAX - WORLD.YMIN)^2 + ...
                              (WORLD.ZMAX - WORLD.ZMIN)^2);
     
    %---------------------------------------------------------------------%
    % Define agents and tasks
    %---------------------------------------------------------------------%
    % Grab agent and task types from CBBA Parameter definitions
    
    % Initialize possible agent fields
    agent_default.id    = 0;            % agent id    
    agent_default.x       = 0;          % agent position (meters)
    agent_default.y       = 0;          % agent position (meters)
    agent_default.z       = 0;          % agent position (meters)
    agent_default.nom_vel = 2;          % agent cruise velocity (m/s)    
    
    %---------------------------------------------------------------------%
    % Define sample scenario
    %---------------------------------------------------------------------%
    
    N = 3;      % number of agents
    M = 20;     % number of tasks
    % M2 = M-M1;  % tasks appear online

    %% Create random agents and define parameters for each agents
    for n=1:N

        agents(n) = agent_default;

        if n == 1
            agents(1).x    = WORLD.XMIN + 5;
            agents(1).y    = WORLD.YMIN + 5;   
        else
            % agents(n).x    = rand(1)*(WORLD.XMAX - WORLD.XMIN) + WORLD.XMIN;
            % agents(n).y    = rand(1)*(WORLD.YMAX - WORLD.YMIN) + WORLD.YMIN;
            agents(n).x    = agents(n-1).x;
            agents(n).y    = agents(n-1).y + 5;
        end
    
        % Init remaining agent parameters
        agents(n).id   = n;

    end
    
    %% Create random tasks
    for m=1:M

        tasks(m) = CreateTask(m,0,WORLD);

    end

    %% Calculate distance matrix
    D = zeros(M,M);  % distance between two vertex

    for i=1:M-1
        for j=i+1:M
            delta_x = tasks(i).x-tasks(j).x;
            delta_y = tasks(i).y-tasks(j).y;
            delta_z = tasks(i).z-tasks(j).z;

            D(i,j)=sqrt((delta_x)^2+(delta_y)^2+(delta_z)^2);
            
            D(j,i)=D(i,j);
            
        end
    end

    model.WORLD = WORLD;
    model.tasks = tasks;
    model.agents = agents;
    model.N = N; % number of agents
    model.M = M; % number of tasks
    model.D = D;
end
