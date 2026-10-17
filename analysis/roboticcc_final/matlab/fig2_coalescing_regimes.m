function fig = fig2_coalescing_regimes()
%FIG2_COALESCING_REGIMES Plot AGX work/latency changes relative to Eager.

cfg = common_formatting();
root = fileparts(fileparts(mfilename('fullpath')));
csvPath = fullfile(root, 'figures', 'source', 'fig2_coalescing_regimes.csv');
pdfPath = fullfile(root, 'figures', 'pdf', 'fig2_coalescing_regimes.pdf');
pngPath = fullfile(root, 'figures', 'png', 'fig2_coalescing_regimes.png');

T = readtable(csvPath, 'TextType', 'string', 'VariableNamingRule', 'preserve');
algorithms = ["CBAA", "ACBBA", "PI", "HIPC"];
loads = ["low", "medium", "high"];
loadLabels = ["Low arrivals (0.075 tasks/s)", ...
    "Medium arrivals (0.30 tasks/s)", "High arrivals (0.60 tasks/s)"];

% Keep this figure's publication styling local so Figure 1 is unchanged.
fontName = 'Times New Roman';
axisFontSize = 6.5;
labelFontSize = 7.5;
legendFontSize = 6.8;
policyColors = [
    0.1216 0.4667 0.7059
    1.0000 0.4980 0.0549
    0.1725 0.6275 0.1725
    0.8392 0.1529 0.1569
];

fig = figure('Color', 'w', 'Units', 'inches', 'Position', [1 1 7.16 5.36], ...
    'PaperPositionMode', 'auto', 'Renderer', 'painters');
tl = tiledlayout(fig, 4, 3, 'TileSpacing', 'compact', 'Padding', 'compact');

allX = [T.y_work_pct_ci_low; T.y_work_pct_ci_high; 0];
xPad = max(4, 0.06 * range(allX));
xLim = [10*floor((min(allX)-xPad)/10), 10*ceil((max(allX)+xPad)/10)];

yLims = zeros(3,2);
for col = 1:3
    q = T.arrival_load == loads(col);
    vals = [T.x_latency_pct_ci_low(q); T.x_latency_pct_ci_high(q); 0];
    pad = max(3, 0.06 * range(vals));
    yLims(col,:) = [10*floor((min(vals)-pad)/10), 10*ceil((max(vals)+pad)/10)];
end

legendHandles = gobjects(1,4);
for row = 1:4
    for col = 1:3
        ax = nexttile(tl, (row-1)*3 + col);
        hold(ax, 'on');
        q = T.algorithm == algorithms(row) & T.arrival_load == loads(col);
        D = T(q,:);

        xline(ax, 0, ':', 'Color', cfg.guideColor, 'LineWidth', 0.55, ...
            'HandleVisibility', 'off');
        yline(ax, 0, ':', 'Color', cfg.guideColor, 'LineWidth', 0.55, ...
            'HandleVisibility', 'off');

        policyNUsed = zeros(1, numel(cfg.policyIds));
        policyNPlanned = zeros(1, numel(cfg.policyIds));
        for p = 1:numel(cfg.policyIds)
            r = D(D.policy_id == cfg.policyIds(p),:);
            if height(r) ~= 1
                error('Missing or duplicate Figure 2 row: %s/%s/%s', ...
                    algorithms(row), loads(col), cfg.policyIds(p));
            end
            x = r.y_work_pct;
            y = r.x_latency_pct;
            policyNUsed(p) = r.n_used;
            policyNPlanned(p) = r.n_planned;
            color = policyColors(p,:);
            errorbar(ax, x, y, x-r.y_work_pct_ci_low, ...
                r.y_work_pct_ci_high-x, 'horizontal', 'LineStyle', 'none', ...
                'Color', color, 'LineWidth', 0.55, 'CapSize', 3, ...
                'HandleVisibility', 'off');
            errorbar(ax, x, y, y-r.x_latency_pct_ci_low, ...
                r.x_latency_pct_ci_high-y, 'LineStyle', 'none', ...
                'Color', color, 'LineWidth', 0.55, 'CapSize', 3, ...
                'HandleVisibility', 'off');
            h = plot(ax, x, y, cfg.policyMarkers{p}, 'MarkerSize', 4.6, ...
                'MarkerFaceColor', color, 'MarkerEdgeColor', color, ...
                'Color', color, 'LineWidth', 0.7);
            if row == 1 && col == 1
                legendHandles(p) = h;
            else
                h.HandleVisibility = 'off';
            end
        end

        plot(ax, 0, 0, 'k+', 'MarkerSize', 5.8, 'LineWidth', 0.9, ...
            'HandleVisibility', 'off');

        incomplete = policyNUsed < policyNPlanned;
        if any(incomplete)
            if nnz(incomplete) == 1
                policyIndex = find(incomplete, 1);
                threshold = extractAfter(cfg.policyIds(policyIndex), "count_b");
                note = sprintf('b = %s: n = %d', threshold, policyNUsed(policyIndex));
            else
                note = "n = " + strjoin(string(policyNUsed(incomplete)), " / ");
            end
            text(ax, 0.035, 0.955, note, 'Units', 'normalized', ...
                'HorizontalAlignment', 'left', 'VerticalAlignment', 'top', ...
                'FontName', fontName, 'FontSize', 5.8, ...
                'Color', [0.18 0.18 0.18], 'BackgroundColor', 'w', ...
                'Margin', 0.5, 'Clipping', 'on');
        end

        xlim(ax, xLim);
        ylim(ax, yLims(col,:));
        box(ax, 'off');
        grid(ax, 'off');
        set(ax, 'FontName', fontName, 'FontSize', axisFontSize, ...
            'LineWidth', 0.5, 'TickDir', 'out', 'XColor', cfg.axisColor, ...
            'YColor', cfg.axisColor, 'Layer', 'top');
        if row == 1
            title(ax, loadLabels(col), 'FontName', fontName, ...
                'FontSize', labelFontSize, 'FontWeight', 'normal');
        end
        if col == 1
            ylabel(ax, algorithms(row), 'FontName', fontName, ...
                'FontSize', labelFontSize, 'FontWeight', 'bold');
        end
        if row ~= 4
            ax.XTickLabel = [];
        end
    end
end

xlabel(tl, 'Allocator work change relative to Eager (%)', ...
    'FontName', fontName, 'FontSize', labelFontSize);
ylabel(tl, 'Mean task-latency change relative to Eager (%)', ...
    'FontName', fontName, 'FontSize', labelFontSize);

policyLabels = ["Count b = 2", "Count b = 4", "Count b = 8", ...
    "Bounded b = 4, W = 10 s"];
lg = legend(legendHandles, policyLabels, 'Orientation', 'horizontal', ...
    'NumColumns', 4, 'Box', 'off', 'FontName', fontName, ...
    'FontSize', legendFontSize);
lg.Layout.Tile = 'south';

exportgraphics(fig, pdfPath, 'ContentType', 'vector', 'BackgroundColor', 'white');
exportgraphics(fig, pngPath, 'Resolution', 400, 'BackgroundColor', 'white');
end
