function make_all_figures()
%MAKE_ALL_FIGURES Reproduce all final RoboticCC paper figures.
%
% Run from this directory:
%   make_all_figures

here = fileparts(mfilename('fullpath'));
addpath(here);
close all force;

fig1_admission_architecture();
fig2_coalescing_regimes();
fig3_hipc_medium_hardware();

fprintf('RoboticCC figures written to ../figures/pdf and ../figures/png.\n');
end
