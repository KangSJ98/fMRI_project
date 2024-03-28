function opt = saveData(opt, data)
if ~exist(opt.dataDir,'dir'), mkdir(opt.dataDir); end
fileName = sprintf('trial%d.mat', opt.trial);

save(fullfile(opt.dataDir, fileName), 'data')
opt.trial = opt.trial + 1;

if opt.trial > opt.maxTrial
    sca;
    Eyelink('StopRecording');
    opt.expDone = 1;
end

