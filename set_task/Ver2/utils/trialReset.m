function [opt, data] = trialReset(opt)
opt.card1 = selectRandomCard(opt);
while true
    opt.card2 = selectRandomCard(opt);
    if ~isequal(opt.card1, opt.card2)
        break
    end
end

opt.answerCard = calculateAnswerCard(opt.card1, opt.card2, opt);
opt.wrongCard = calculateWrongCard(opt.answerCard, opt);

opt.playerCard = card();
opt.optionLeftCard = card();
opt.optionRightCard = card();
opt.optionUpCard = card();

opt.optionLeft = card('triangle', 'outline', 'red', '1');
opt.optionRight = card('square', 'filled', 'green', '2');
opt.optionUp = card('star', 'stripe', 'blue', '3');

opt.trialDone = 0;

data = [];

opt.trialBgn = GetSecs;
opt.frameBgn = GetSecs;

opt.timeCounter = 0;

end

