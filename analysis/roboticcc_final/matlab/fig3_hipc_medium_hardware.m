function fig = fig3_hipc_medium_hardware()
%FIG3_HIPC_MEDIUM_HARDWARE Show individual matched AGX/RP2040 policy pairs.

cfg = common_formatting();
root = fileparts(fileparts(mfilename('fullpath')));
csvPath = fullfile(root, 'figures', 'source', 'fig3_hipc_medium_hardware.csv');
pdfPath = fullfile(root, 'figures', 'pdf', 'fig3_hipc_medium_hardware.pdf');
pngPath = fullfile(root, 'figures', 'png', 'fig3_hipc_medium_hardware.png');

T = readtable(csvPath, 'TextType', 'string', 'VariableNamingRule', 'preserve');
platforms = ["AGX", "RP2040"];
platformLabels = ["AGX Orin", "RP2040"];
traceIds = ["trace_0000", "trace_0001", "trace_0002", "trace_0003"];

% Keep this figure's publication styling local so Figure 1 is unchanged.
fontName = 'Times New Roman';
axisFontSize = 6.5;
labelFontSize = 7.5;
legendFontSize = 6.8;
traceColors = [
    0.1216 0.4667 0.7059
    1.0000 0.4980 0.0549
    0.1725 0.6275 0.1725
    0.8392 0.1529 0.1569
];
traceMarkers = {'o', 's', '^', 'd'};

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 3.52 3.57], ...
    'PaperPositionMode', 'auto', 'Renderer', 'painters');
tl = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
legendHandles = gobjects(1,4);

latencyValues = [T.eager_mean_release_to_completion_latency_s; ...
    T.count4_mean_release_to_completion_latency_s];
latPad = max(3, 0.08*range(latencyValues));
latLim = [0, 25*ceil((max(latencyValues)+latPad)/25)];

for col = 1:2
    D = T(T.platform == platforms(col),:);
    if height(D) ~= 4
        error('Expected four %s HIPC/medium trace pairs.', platforms(col));
    end

    axWork = nexttile(tl, col);
    hold(axWork, 'on');
    title(axWork, platformLabels(col), 'FontName', fontName, ...
        'FontSize', labelFontSize, 'FontWeight', 'bold');
    axLat = nexttile(tl, 2 + col);
    hold(axLat, 'on');

    for k = 1:4
        r = D(D.trace_id == traceIds(k),:);
        if height(r) ~= 1
            error('Missing or duplicate Figure 3 row: %s/%s', ...
                platforms(col), traceIds(k));
        end
        color = traceColors(k,:);
        h = plot(axWork, [1 2], [r.eager_work_s r.count4_work_s], '-', ...
            'Color', color, 'LineWidth', 0.9, 'Marker', traceMarkers{k}, ...
            'MarkerSize', 4.4, 'MarkerFaceColor', color, ...
            'MarkerEdgeColor', color);
        if col == 1
            legendHandles(k) = h;
        else
            h.HandleVisibility = 'off';
        end
        plot(axLat, [1 2], ...
            [r.eager_mean_release_to_completion_latency_s ...
             r.count4_mean_release_to_completion_latency_s], '-', ...
            'Color', color, 'LineWidth', 0.9, 'Marker', traceMarkers{k}, ...
            'MarkerSize', 4.4, 'MarkerFaceColor', color, ...
            'MarkerEdgeColor', color, 'HandleVisibility', 'off');
    end

    workValues = [D.eager_work_s; D.count4_work_s];
    pad = max(0.03*max(workValues), 0.08*range(workValues));
    workUpper = niceUpperLimit(max(workValues)+pad);
    ylim(axWork, [0, workUpper]);
    yticks(axWork, 0:niceTickStep(workUpper):workUpper);
    ylim(axLat, latLim);
    yticks(axLat, 0:25:latLim(2));
    formatPairAxis(axWork, cfg, fontName, axisFontSize, labelFontSize, ...
        col == 1, 'Work (processor-s)');
    formatPairAxis(axLat, cfg, fontName, axisFontSize, labelFontSize, ...
        col == 1, 'Mean task latency (s)');
end

lg = legend(legendHandles, ["0000", "0001", "0002", "0003"], ...
    'Orientation', 'horizontal', 'NumColumns', 4, 'Box', 'off', ...
    'FontName', fontName, 'FontSize', legendFontSize);
lg.Layout.Tile = 'south';

exportgraphics(fig, pdfPath, 'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, pngPath, 'Resolution', 400, 'BackgroundColor', 'white');
end

function formatPairAxis(ax, cfg, fontName, axisFontSize, labelFontSize, showYLabel, yText)
xlim(ax, [0.75 2.25]);
xticks(ax, [1 2]);
xticklabels(ax, {'Eager', 'Count b = 4'});
box(ax, 'off');
grid(ax, 'off');
set(ax, 'FontName', fontName, 'FontSize', axisFontSize, ...
    'LineWidth', 0.5, 'TickDir', 'out', 'XColor', cfg.axisColor, ...
    'YColor', cfg.axisColor, 'Layer', 'top');
if showYLabel
    ylabel(ax, yText, 'FontName', fontName, 'FontSize', labelFontSize);
end
end

function upper = niceUpperLimit(value)
step = 5 * 10^(floor(log10(value))-1);
upper = ceil(value/step) * step;
end

function step = niceTickStep(upper)
rawStep = upper/4;
scale = 10^floor(log10(rawStep));
normalized = rawStep/scale;
if normalized <= 1
    factor = 1;
elseif normalized <= 2
    factor = 2;
elseif normalized <= 5
    factor = 5;
else
    factor = 10;
end
step = factor*scale;
end
