function options = ChooseOption(answerCard, feature, opt)
% option{1}, option{2}에 정답 feature와 오답 feature가 랜덤하게 선택
    options = cell(1, 2);
    
    % 정답 카드의 해당 feature 값
    correctValue = answerCard.(feature);
    
    % 오답 생성을 위해 랜덤하게 다른 값을 선택
    incorrectValue = correctValue;
    while strcmp(incorrectValue, correctValue) % 정답과 중복되지 않는 값을 선택할 때까지 반복
        switch feature
            case 'shape'
                incorrectValue = opt.shapes{randi(length(opt.shapes))};
            case 'color'
                incorrectValue = opt.colors{randi(length(opt.colors))};
            case 'shadow'
                incorrectValue = opt.shadows{randi(length(opt.shadows))};
            case 'number'
                incorrectValue = opt.numbers{randi(length(opt.numbers))};
        end
    end
    
    % options 배열에 값을 저장
    if randi(2) == 1
        options{1} = correctValue;
        options{2} = incorrectValue;
    else
        options{1} = incorrectValue;
        options{2} = correctValue;
    end
end
