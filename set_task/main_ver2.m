function main_ver2()
addPath();

opt = initiate();

for tr = 1:opt.trNum
    WhiteOut(opt); % 0.5~0.7초 백색 화면
    
    card1 = SelectRandomCard(opt); % 무작위 카드 1 선택
    while true
        card2 = SelectRandomCard(opt); % 무작위 카드 2 선택
        if ~isequal(card1, card2)
            break
        end
    end
    answerCard = CalculateAnswerCard(card1, card2, opt); % 정답 카드 계산
   
    playerShape = card(); % 플레이어 옵션 초기화
    
    for i = 1:length(opt.features)
        feature = opt.features{i};
        
        % card 1, 2, 3 화면에 표시
        DisplayBackground(opt)
        DisplayCard(card1, opt.card1X, opt.card1Y, opt);
        DisplayCard(card2, opt.card2X, opt.card2Y, opt);
        % DisplayCard(playerShape, opt.card3X, opt.card3Y, opt);
        
        options = ChooseOption(answerCard, feature, opt); % options = {'정답', '오답'}
        DisplayOption(feature, options, opt, playerShape); % 선택 옵션 제시
        
        % 화면 업데이트
        Screen('Flip', opt.window);
        
        playerSelection = GetUserSelection(opt); % 플레이어 선택(왼쪽 1, 오른쪽 2)
        playerShape.(feature) = options{playerSelection}; % 선택 옵션 저장
        
        DisplayChoice(card1, card2, playerShape, playerSelection, opt); % 선택한 옵션 표시

    end
    if tr == 21
    disp('Error Correction trial start');
    if tr > 20
        playerShape = ErrorCorrection(card1, card2, playerShape, answerCard, opt);
    end

    Feedback(card1, card2, playerShape, answerCard, opt)

end
end

function addPath()
%% Add path for configuration, utilities, log
curr_dir = fileparts(mfilename('fullpath'));
parent_dir = fileparts(curr_dir);
addpath(genpath(parent_dir));
end
