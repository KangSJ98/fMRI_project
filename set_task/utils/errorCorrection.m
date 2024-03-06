function playerShape = errorCorrection(card1, card2, playerShape, answerCard, opt)
optionLeft = playerShape;

if isequal(playerShape, answerCard)
    optionRight = SelectRandomCard(opt);
else
    optionRight = answerCard;
end

DisplayBackground(opt)
DisplayCard(card1, opt.card1X, opt.card1Y, opt);
DisplayCard(card2, opt.card2X, opt.card2Y, opt);
DisplayCard(optionLeft, opt.optionLeftX, opt.optionLeftY, opt);
DisplayCard(optionRight, opt.optionRightX, opt.optionRightY, opt);

Screen('Flip', opt.window);

playerSelection = GetUserSelection(opt);
if playerSelection == 1
    playerShape = optionLeft;
else
    playerShape = optionRight;
end

