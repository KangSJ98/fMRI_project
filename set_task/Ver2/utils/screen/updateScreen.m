function [opt, data] = updateScreen(opt, data)
%% 그림 그리는 부분
Screen('FillRect', opt.window, opt.backgroundColor,[0, 0, opt.screenWidth, opt.screenHeight]) % 회색 배경
Screen('FrameRect', opt.window, [0 0 0], opt.card1Area, opt.cardThick);                 % card 1 테두리
Screen('FrameRect', opt.window, [0 0 0], opt.card2Area, opt.cardThick);                 % card 2 테두리
Screen('FrameRect', opt.window, [0 0 0], opt.card3Area, opt.cardThick);                 % card 3 테두리

drawCard(opt.card1, opt.card1X, opt.card1Y, opt);
drawCard(opt.card2, opt.card2X, opt.card2Y, opt);
if opt.i > 1
    drawCard(opt.playerCard, opt.card3X, opt.card3Y, opt);
end

if opt.phase == 1
    Screen('FrameRect', opt.window, [0 0 0], opt.optionLeftArea, opt.cardThick);            % option left 테두리
    Screen('FrameRect', opt.window, [0 0 0], opt.optionRightArea, opt.cardThick);           % option right 테두리
    Screen('FrameRect', opt.window, [0 0 0], opt.optionUpArea, opt.cardThick);
    drawCard(opt.optionLeftCard, opt.optionLeftX, opt.optionLeftY, opt);
    drawCard(opt.optionRightCard, opt.optionRightX, opt.optionRightY, opt);
    drawCard(opt.optionUpCard, opt.optionUpX, opt.optionUpY, opt);
elseif opt.phase == 2
    if opt.choice == 1
        Screen('FrameRect', opt.window, [0 0 0], opt.optionLeftArea, opt.cardThick);
        drawCard(opt.optionLeftCard, opt.optionLeftX, opt.optionLeftY, opt);
    elseif opt.choice == 2
        Screen('FrameRect', opt.window, [0 0 0], opt.optionRightArea, opt.cardThick);
        drawCard(opt.optionRightCard, opt.optionRightX, opt.optionRightY, opt);
    elseif opt.choice == 3
        Screen('FrameRect', opt.window, [0 0 0], opt.optionUpArea, opt.cardThick);
        drawCard(opt.optionUpCard, opt.optionUpX, opt.optionUpY, opt);
    end
end

if (GetSecs-opt.frameBgn > opt.screenFlipTime),fprintf('frame no %d missing\n',opt.timeCounter); end
[~, opt.frameBgn] = Screen('Flip', opt.window);

%% data 저장
opt.timeCounter = opt.timeCounter + 1;
[opt, data] = collectData(opt, data);

end

