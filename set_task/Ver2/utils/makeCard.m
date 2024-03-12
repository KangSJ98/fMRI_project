function [opt, data] = makeCard(opt, data)

for i = 1:length(opt.features)
    opt.feature = opt.features{i};

    opt.optionLeftCard = opt.playerCard;
    opt.optionRightCard =opt.playerCard;

    if randi([1,2]) == 1
        opt.optionLeftCard.(opt.feature) = opt.answerCard.(opt.feature);
        opt.optionRightCard.(opt.feature) = opt.wrongCard.(opt.feature);
    else
        opt.optionLeftCard.(opt.feature) = opt.wrongCard.(opt.feature);
        opt.optionRightCard.(opt.feature) = opt.answerCard.(opt.feature);
    end

    opt.phaseDone = 0;
    opt.phase = 1;
    opt.choice = 0;
    opt.phaseBgn = GetSecs;

    while ~opt.phaseDone
        [opt, data] = getUserSelect(opt, data);
        [opt, data] = updateScreen(opt, data);
    end
end

end

