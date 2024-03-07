function monkey_main()
addPath();

opt = initiate();

% select training feature {'shape', 'shadow', 'color', 'number'}
opt.features = {'color'};

% select training mode 'same', 'different', 'all'
mode = 'different';

% default
defaultShape = 'triangle'; % 'triangle', 'square', 'star'
defaultColor = 'black'; % 'black', 'red', 'green', 'blue'
defaultShadow = 'filled'; % 'outline', 'filled', 'stripe'
defaultNumber = '1';

for tr = 1:opt.trNum
    WhiteOut(opt); % 0.5~0.7초 백색 화면

    %% select card 1,2
    card1 = card(defaultShape, defaultColor, defaultNumber, defaultShadow);
    card2 = card(defaultShape, defaultColor, defaultNumber, defaultShadow);
    playerShape = card(defaultShape, defaultColor, defaultNumber, defaultShadow);

    for i = 1:length(opt.features)
        a = randi(3);
        switch mode
            case 'same'
                b = a;
            case 'different'
                b = a;
                while a == b
                    b = randi(3);
                end
            case 'all'
                b = randi(3);
        end

        feature = opt.features{i};
        switch feature
            case 'shape'
                card1.shape = opt.shapes{a};
                card2.shape = opt.shapes{b};
            case 'color'
                card1.color = opt.colors{a};
                card2.color = opt.colors{b};
            case 'shadow'
                card1.shadow = opt.shadows{a};
                card2.shadow = opt.shadows{b};
            case 'number'
                card1.number = opt.numbers{a};
                card2.number = opt.numbers{b};
        end
    end

    answerCard = CalculateAnswerCard(card1, card2, opt);

    %% select option
    for i = 1:length(opt.features)
        feature = opt.features{i};

        DisplayBackground(opt);
        DisplayCard(card1, opt.card1X, opt.card1Y, opt);
        DisplayCard(card2, opt.card2X, opt.card2Y, opt);

        options = ChooseOption(answerCard, feature, opt);
        DisplayOption(feature, options, opt, playerShape)

        Screen('Flip', opt.window);

        % playerSelection = GetMonkeySelection(opt); % monkey 선택(왼쪽 1, 오른쪽 2)
        playerSelection = GetUserSelection(opt);
        playerShape.(feature) = options{playerSelection};

        DisplayChoice(card1, card2, playerShape, playerSelection, opt);
    end
    
    Feedback(card1, card2, playerShape, answerCard, opt);
end
end

function addPath()
%% Add path for configuration, utilities, log
curr_dir = fileparts(mfilename('fullpath'));
parent_dir = fileparts(curr_dir);
addpath(genpath(parent_dir));
end
