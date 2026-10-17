function fig = fig1_admission_architecture()
%FIG1_ADMISSION_ARCHITECTURE Draw the task-admission and execution schematic.

cfg = common_formatting();
root = fileparts(fileparts(mfilename('fullpath')));
pdfPath = fullfile(root, 'figures', 'pdf', 'fig1_admission_architecture.pdf');
pngPath = fullfile(root, 'figures', 'png', 'fig1_admission_architecture.png');

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 3.45 6.15], ...
    'PaperPositionMode', 'auto', 'Renderer', 'painters');
ax = axes(fig, 'Position', [0.02 0.02 0.96 0.96]);
hold(ax, 'on');
axis(ax, [0 1 0 1]);
axis(ax, 'off');

boxX = 0.06;
boxW = 0.62;
boxH = 0.072;
y = [0.91 0.795 0.68 0.565 0.45 0.335 0.22 0.105];
labels = {
    'Task release'
    'Pending queue'
    'Eager / Count / Bounded admission rule'
    'Reliable task-admission announcement'
    'Robot-local known-task pool'
    'Decentralized allocator transaction'
    'Retained goal and path state'
    'Physical or simulated execution'
};

fills = repmat([0.96 0.96 0.96], 8, 1);
fills(3,:) = [0.90 0.94 0.98];
fills(4,:) = [0.91 0.96 0.93];
fills(6,:) = [0.98 0.93 0.85];
fills(7,:) = [0.94 0.92 0.97];

for k = 1:numel(y)
    rectangle(ax, 'Position', [boxX y(k) boxW boxH], 'Curvature', 0.06, ...
        'FaceColor', fills(k,:), 'EdgeColor', [0.2 0.2 0.2], 'LineWidth', 0.75);
    text(ax, boxX + boxW/2, y(k) + boxH/2, labels{k}, ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
        'FontName', cfg.fontName, 'FontSize', 7.1, 'Color', cfg.axisColor, ...
        'Interpreter', 'none');
    if k < numel(y)
        drawArrow(ax, boxX + boxW/2, y(k) - 0.004, ...
            boxX + boxW/2, y(k+1) + boxH + 0.004, [0.25 0.25 0.25]);
    end
end

% Make release and admission visibly distinct.
text(ax, 0.695, 0.735, {'Release is not', 'admission'}, ...
    'FontName', cfg.fontName, 'FontSize', 6.6, 'FontAngle', 'italic', ...
    'Color', [0.25 0.25 0.25], 'VerticalAlignment', 'middle');

% Feedback entering later allocator transactions.
sideX = 0.76;
sideW = 0.20;
sideH = 0.073;
rectangle(ax, 'Position', [sideX 0.445 sideW sideH], 'Curvature', 0.06, ...
    'FaceColor', [0.95 0.95 0.95], 'EdgeColor', [0.35 0.35 0.35], 'LineWidth', 0.7);
text(ax, sideX + sideW/2, 0.445 + sideH/2, {'Allocator peer', 'communication'}, ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
    'FontName', cfg.fontName, 'FontSize', 6.6, 'Interpreter', 'none');
drawArrow(ax, sideX, 0.465, boxX + boxW + 0.005, y(6) + 0.052, [0.35 0.35 0.35]);

rectangle(ax, 'Position', [sideX 0.205 sideW sideH], 'Curvature', 0.06, ...
    'FaceColor', [0.95 0.95 0.95], 'EdgeColor', [0.35 0.35 0.35], 'LineWidth', 0.7);
text(ax, sideX + sideW/2, 0.205 + sideH/2, {'Task-completion', 'information'}, ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
    'FontName', cfg.fontName, 'FontSize', 6.6, 'Interpreter', 'none');
plot(ax, [sideX + sideW/2 sideX + sideW/2], [0.278 0.322], '-', ...
    'Color', [0.35 0.35 0.35], 'LineWidth', 0.75);
drawArrow(ax, sideX + sideW/2, 0.322, boxX + boxW + 0.005, y(6) + 0.020, [0.35 0.35 0.35]);

% Causal timing boundary and HIL scope notes.
rectangle(ax, 'Position', [0.015 y(6)-0.018 0.705 boxH+0.036], ...
    'EdgeColor', [0.70 0.46 0.08], 'LineStyle', '--', 'LineWidth', 0.75);
text(ax, 0.725, y(6)+boxH/2, {'Only the calling robot''s', 'virtual processor is busy'}, ...
    'FontName', cfg.fontName, 'FontSize', 6.4, 'Color', [0.45 0.29 0.04], ...
    'VerticalAlignment', 'middle');

text(ax, 0.50, 0.015, ...
    {'RP2040 HIL measures allocator transactions.', ...
     'World state, communication, routing, and motion remain simulated.'}, ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
    'FontName', cfg.fontName, 'FontSize', 6.4, 'Color', [0.25 0.25 0.25]);

exportgraphics(fig, pdfPath, 'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, pngPath, 'Resolution', 400, 'BackgroundColor', 'white');
end

function drawArrow(ax, x1, y1, x2, y2, color)
dx = x2 - x1;
dy = y2 - y1;
quiver(ax, x1, y1, dx, dy, 0, 'Color', color, 'LineWidth', 0.75, ...
    'MaxHeadSize', 0.32, 'AutoScale', 'off');
end

