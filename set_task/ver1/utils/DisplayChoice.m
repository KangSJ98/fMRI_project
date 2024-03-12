function DisplayChoice(card1, card2, playerShape, playerSelection, opt)
DisplayBackground(opt)
DisplayCard(card1, opt.card1X, opt.card1Y, opt);
DisplayCard(card2, opt.card2X, opt.card2Y, opt);

if playerSelection == 1
    DisplayCard(playerShape, opt.optionLeftX, opt.optionLeftY, opt);
    Screen('FrameRect', opt.window, [0 255 0], opt.optionLeftArea, opt.cardThick);
else
    DisplayCard(playerShape, opt.optionRightX, opt.optionRightY, opt);
    Screen('FrameRect', opt.window, [0 255 0], opt.optionRightArea, opt.cardThick);
end

Screen('Flip', opt.window);

startTime = GetSecs;
while GetSecs - startTime <= 0.5
end

end

