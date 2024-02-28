function main()

opt = initiate();

for tr = 1:opt.trNum
    
    card1 = SelectRandomCard(opt); % 무작위 카드 1 선택
    card2 = SelectRandomCard(opt); % 무작위 카드 2 선택
    answerCard = CalculateAnswerCard(card1, card2, opt); % 정답 카드 계산
   
    playerShape = card(); % 플레이어 옵션 초기화
    shuffledFeatures = opt.features(randperm(length(opt.features))); % feature 선택 순서 랜덤으로 섞음
    
    for i = 1:length(shuffledFeatures)
        feature = shuffledFeatures{i};
        disp(feature);
        
        % card 1, 2, 3 화면에 표시
        DisplayCard(card1, opt.card1X, opt.card1Y, opt);
        DisplayCard(card2, opt.card2X, opt.card2Y, opt);
        DisplayCard(playerShape, opt.card3X, opt.card3Y, opt);
        
        
        options = ChooseOption(answerCard, feature, opt); % options = {'정답', '오답'}
        disp(options);
        DisplayOption(feature, options, opt); % 선택 옵션 제시
        
        % 화면 업데이트
        Screen('Flip', opt.window);
        
        playerSelection = GetUserSelection(); % 플레이어 선택(왼쪽 1, 오른쪽 2)
        playerShape.(feature) = options{playerSelection}; % 선택 옵션 저장
        if playerSelection == 3
            break;
        end
        
    end
    if playerSelection == 3
        break;
    end
    % card 1, 2, 3 화면에 표시
    DisplayCard(card1, opt.card1X, opt.card1Y, opt);
    DisplayCard(card2, opt.card2X, opt.card2Y, opt);
    DisplayCard(playerShape, opt.card3X, opt.card3Y, opt);
    Screen('Flip', opt.window);
    
    startTime = GetSecs; % 현재 시간 기록
    while GetSecs - startTime <= 2
    end
    
    if CheckAnswer(playerShape, answerCard)
        disp('정답');
    else
        disp('오답');
    end
    
    
end
end

% function main()
%     opt = initiate();
%     % 카드 생성
%     myCard1 = card('circle', 'red', 1, 'outline');
%     myCard2 = card('star', 'blue', 2, 'stripe');
%     myCard3 = card('triangle', 'green', 3, 'filled');
%     myCard3.shape = 'star';
%     % 카드 표시
%     DisplayCard(myCard1, opt.screenWidth/2, opt.screenHeight/4, opt);
%     DisplayCard(myCard2, opt.screenWidth/2, opt.screenHeight/2, opt);
%     DisplayCard(myCard3, opt.screenWidth/2, opt.screenHeight*3/4, opt);
%     Screen('Flip', opt.window)
%     % 키보드 입력 대기
%     KbWait;
%
%     % 화면 닫기
%     sca;
% end

