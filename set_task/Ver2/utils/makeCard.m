function [opt, data] = makeCard(opt, data)

for i = 1:length(opt.features) + 1
    opt.i = i;
    if i < length(opt.features) + 1
        opt.feature = opt.features{i};
        
        opt.optionLeftCard = opt.playerCard;
        opt.optionRightCard =opt.playerCard;
        opt.optionUpCard = opt.playerCard;
        
        opt.optionLeftCard.(opt.feature) = opt.optionLeft.(opt.feature);
        opt.optionRightCard.(opt.feature) = opt.optionRight.(opt.feature);
        opt.optionUpCard.(opt.feature) = opt.optionUp.(opt.feature);
    else
        if randi([1,2]) == 1
            opt.optionLeftCard = opt.playerCard;
            opt.optionRightCard = selectRandomCard(opt);
            opt.optionUpCard = selectRandomCard(opt);
        else
            opt.optionLeftCard = selectRandomCard(opt);
            opt.optionRightCard = opt.playerCard;
            opt.optionUpCard = selectRandomCard(opt);
        end
    end
    opt.saveOption = 1;
    opt.phaseDone = 0;
    opt.phase = 1;
    opt.choice = 0;
    opt.phaseBgn = GetSecs;
    
    while ~opt.phaseDone
        [opt, data] = getUserSelect(opt, data);
        [opt, data] = updateScreen(opt, data);
    end
end

% feedback(opt);

end

