function [opt, data] = getUserSelect(opt, data)
if opt.phase == 1
    [keyIsDown, ~, keyCode] = KbCheck;
    if keyIsDown
        if keyCode(KbName('LeftArrow'))
            opt.playerCard = opt.optionLeftCard;
            opt.phase = 2;
            opt.choice = 1;
            opt.phaseBgn = GetSecs;
        elseif keyCode(KbName('RightArrow'))
            opt.playerCard = opt.optionRightCard;
            opt.phase = 2;
            opt.choice = 2;
            opt.phaseBgn = GetSecs;
        elseif keyCode(KbName('Escape'))
            opt.phaseDone = 1;
            opt.expDone = 1;
        end
    end
end


end

