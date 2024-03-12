function [opt,data] = collectData(opt,data)

if opt.eyelinkPresent
    eyeData = Eyelink('NewestFloatSample');
    
    data.eyePos(opt.timeCounter,:) = [eyeData.gx(opt.eyeSide),eyeData.gy(opt.eyeSide)];
    data.eyeSz(opt.timeCounter,1) = [eyeData.pa(opt.eyeSide)];
    
end

if opt.timeCounter == 1
    data.info.subject = opt.subName;
    data.info.trial = opt.trial;
    data.info.date = date;
end

end

