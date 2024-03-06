function selection = GetUserSelection(opt)
selection = randi([1, 2]); % 랜덤 선택

startTime = GetSecs; % 현재 시간 기록
while GetSecs - startTime <= 1
end
while GetSecs - startTime <= opt.trTime
    [keyIsDown, ~, keyCode] = KbCheck;
    if keyIsDown == true
        if keyCode(KbName('LeftArrow'))
            selection = 1;
            break;
        elseif keyCode(KbName('RightArrow'))
            selection = 2;
            break;
        end
    end
end
