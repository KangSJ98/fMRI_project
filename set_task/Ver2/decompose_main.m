clear all; 
genDir = pwd;
cd(genDir); addpath(genpath(genDir))

opt = initiate();
while ~opt.expDone
    
    [opt,data] = trialReset(opt);
    [opt,data] = makeCard(opt, data);
    
    opt = saveData(opt,data);
    
end