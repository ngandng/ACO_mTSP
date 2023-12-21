function task_default = CreateTask(id, tc, WORLD)

    % Initialize possible task fields
    task_default.id = id;          % task id
    task_default.tc = tc;
    % task_default.duration = 0;          % task default duration (sec)
    
    task_default.x = rand(1)*(WORLD.XMAX - WORLD.XMIN) + WORLD.XMIN; % task position (meters)
    task_default.y = rand(1)*(WORLD.YMAX - WORLD.YMIN) + WORLD.YMIN; % task position (meters)
    task_default.z = rand(1)*(WORLD.ZMAX - WORLD.ZMIN) + WORLD.ZMIN; % task position (meters)
end