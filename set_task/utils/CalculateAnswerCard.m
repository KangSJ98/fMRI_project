function answerCard = CalculateAnswerCard(card1, card2)
    answerCard = card(); % 정답 카드 객체 생성
    
    % 모양 결정
    if strcmp(card1.shape, card2.shape)
        answerCard.shape = card1.shape;
    else
        shape_candidates = setdiff(opt.shapes, {card1.shape, card2.shape});
        answerCard.shape = shape_candidates{randi(length(shape_candidates))};
    end
    
    % 색 결정
    if strcmp(card1.color, card2.color)
        answerCard.color = card1.color;
    else
        color_candidates = setdiff(opt.colors, {card1.color, card2.color});
        answerCard.color = color_candidates{randi(length(color_candidates))};
    end
    
    % 개수 결정
    if card1.number == card2.number
        answerCard.number = card1.number;
    else
        number_candidates = setdiff(opt.numbers, [card1.number, card2.number]);
        answerCard.number = number_candidates(randi(length(number_candidates)));
    end
    
    % Shadow 결정
    if strcmp(card1.shadow, card2.shadow)
        answerCard.shadow = card1.shadow;
    else
        shadow_candidates = setdiff(opt.shadows, {card1.shadow, card2.shadow});
        answerCard.shadow = shadow_candidates{randi(length(shadow_candidates))};
    end
end
