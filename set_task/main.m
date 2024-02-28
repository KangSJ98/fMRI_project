function main()

opt = initiate();

for tr = 1:opt.trNum
    card1 = SelectRandomCard();
    card2 = SelectRandomCard();
    answerCard = CalculateAnswerCard(card1, card2);

    
end
end
