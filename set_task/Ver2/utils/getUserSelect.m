function [opt, data] = getUserSelect(opt, data)
if opt.phase == 1
    [keyIsDown, ~, keyCode] = KbCheck;
    if GetSecs - opt.phaseBgn > 2
        opt.phase = 2;
        opt.phaseBgn = GetSecs;
        switch randi([1,3])
            case 1
            opt.playerCard = opt.optionLeftCard;
            opt.choice = 1;
            case 2
            opt.playerCard = opt.optionRightCard;
            opt.choice = 2;
            case 3
            opt.playerCard = opt.optionUpCard;
            opt.choice = 3;
        end
    end
    
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
        elseif keyCode(KbName('UpArrow'))
            opt.playerCard = opt.optionUpCard;
            opt.phase = 2;
            opt.choice = 3;
            opt.phaseBgn = GetSecs;
        elseif keyCode(KbName('Escape'))
            opt.phaseDone = 1;
            sca;
            Eyelink('StopRecording');
            opt.expDone = 1;
        end
    end
elseif opt.phase == 2
    if GetSecs - opt.phaseBgn > 0.5
        opt.phaseDone = 1;
    end
end


end

