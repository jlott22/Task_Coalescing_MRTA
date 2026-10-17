function cfg = common_formatting()
%COMMON_FORMATTING Shared IEEE-oriented figure settings.

cfg.fontName = 'Arial';
cfg.axisFontSize = 7;
cfg.labelFontSize = 8;
cfg.legendFontSize = 7;
cfg.lineWidth = 0.9;
cfg.errorLineWidth = 0.65;
cfg.markerSize = 5.2;
cfg.axisColor = [0.15 0.15 0.15];
cfg.guideColor = [0.76 0.76 0.76];

% Okabe-Ito-derived colors, paired with unique marker shapes and line styles.
cfg.policyIds = ["count_b2", "count_b4", "count_b8", "bounded_b4_w10"];
cfg.policyLabels = ["Count b=2", "Count b=4", "Count b=8", "Bounded b=4, W=10 s"];
cfg.policyColors = [
    0.0000 0.4470 0.6980
    0.9020 0.6240 0.0000
    0.0000 0.6196 0.4510
    0.8000 0.4745 0.6549
];
cfg.policyMarkers = {'o', 's', '^', 'd'};

cfg.traceLabels = ["trace 0000", "trace 0001", "trace 0002", "trace 0003"];
cfg.traceColors = [
    0.0000 0.4470 0.6980
    0.8350 0.3690 0.0000
    0.0000 0.6196 0.4510
    0.5000 0.5000 0.5000
];
cfg.traceMarkers = {'o', 's', '^', 'd'};
cfg.traceLineStyles = {'-', '--', '-.', ':'};
end

