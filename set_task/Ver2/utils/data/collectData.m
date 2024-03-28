function [opt,data] = collectData(opt,data)

if opt.eyelinkPresent
    eyeData = Eyelink('NewestFloatSample');
    
    data.eyePos(opt.timeCounter,:) = [eyeData.gx(opt.eyeSide),eyeData.gy(opt.eyeSide)];
    data.eyeSz(opt.timeCounter,1) = [eyeData.pa(opt.eyeSide)];
    
end

if opt.saveOption
    data.option.left(opt.i,1) = opt.optionLeftCard;
    data.option.right(opt.i,2) = opt.optionRightCard;
end

data.choice.choice(opt.i, 1) = opt.choice;
if opt.phase == 1
    data.choice.time(opt.i, 1) = opt.timeCounter;
elseif opt.phase == 2
    data.choice.time(opt.i, 2) = opt.timeCounter;
end

data.phase(opt.timeCounter, 1) = opt.phase;

% data.reward = opt.rewarded;

if opt.timeCounter == 1
    data.info.subject = opt.subName;
    data.info.trial = opt.trial;
    data.info.date = date;
    
    data.info.card1 = opt.card1;
    data.info.card2 = opt.card2;
end

end

