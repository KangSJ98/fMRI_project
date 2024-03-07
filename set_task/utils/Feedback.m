function Feedback(card1, card2, playerShape, answerCard, opt)
%% 조합된 도형을 세 번째 위치에 2초간 표시
DisplayBackground(opt)
DisplayCard(card1, opt.card1X, opt.card1Y, opt);
DisplayCard(card2, opt.card2X, opt.card2Y, opt);
DisplayCard(playerShape, opt.card3X, opt.card3Y, opt);

Screen('Flip', opt.window);

startTime = GetSecs;
while GetSecs - startTime <= opt.trTime
end

%% 정답, 오답 2초간 표시
DisplayBackground(opt)
DisplayCard(card1, opt.card1X, opt.card1Y, opt);
DisplayCard(card2, opt.card2X, opt.card2Y, opt);

if CheckAnswer(playerShape, answerCard)
    disp('정답');
    Screen('FillRect', opt.window, [0 255 0], opt.card3Area);
else
    disp('오답');
    Screen('FillRect', opt.window, [255 0 0], opt.card3Area);
end

Screen('Flip', opt.window);

startTime = GetSecs;
while GetSecs - startTime <= opt.trTime
end

end
