
function PlotModel(model)

% Set plotting parameters

offset = (model.WORLD.XMAX - model.WORLD.XMIN)/100; 

Cmap   = colormap(lines);

%% init time
m_tasks = [];

figure(1);
for i=1:length(model.tasks)
    m_tasks = [m_tasks, model.tasks(i)];
    if model.tasks(i).tc ~= 0
        break;
    end
end

% Plot tasks
cla;
hold on;

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
end

title('Initial time')
xlabel('X');
ylabel('Y');
zlabel('Z');
grid on;
hold off;

%% final time
m_tasks = [];

figure(2);
m_tasks = model.tasks;
% Plot tasks
cla;
hold on;

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
end

title('Final time')
xlabel('X');
ylabel('Y');
zlabel('Z');
grid on;
hold off;

end

    