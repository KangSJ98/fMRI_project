function [opt, data] = trialReset(opt)
opt.card1 = selectRandomCard(opt);
while true
    opt.card2 = selectRandomCard(opt);
    if ~isequal(opt.card1, opt.card2)
        break
    end
end

opt.answerCard = calculateAnswerCard(card1, card2, opt);
opt.wrongCard = calculateWrongCard(opt.answerCard, opt);

opt.playerCard = card();
opt.optionLeftCard = card();
opt.optionRightCard = card();

opt.trialDone = 0;

data = [];

opt.trialBgn = GetSecs;

opt.timeCounter = 0;

end

