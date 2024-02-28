function result = CheckAnswer(playerShape, answerCard)
    % 모든 속성이 일치하는지 확인
    if isequal(playerShape.shape, answerCard.shape) && ...
       isequal(playerShape.color, answerCard.color) && ...
       isequal(playerShape.number, answerCard.number) && ...
       isequal(playerShape.shadow, answerCard.shadow)
        result = true;
    else
        result = false;
    end
end
