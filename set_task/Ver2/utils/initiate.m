function opt = initiate()

opt = [];

opt.screenNumber = 1;

opt = basicConfig(opt);
opt = makeScreenComponents(opt);
end

function opt = basicConfig(opt)

rng('shuffle'); warning off;

% subject info
opt.subName = input('Subject Name : ','s');
opt.trainingMode = isempty(opt.subName);
opt.dataDir = fullfile(pwd, 'data', opt.subName);
opt.trial = max(length(dir(opt.dataDir))-2,1);

% initial variables
opt.expDone = 0;
opt.maxTrial = 100;


% eyelink
try,
    opt.useEyelink = ~opt.trainingMode;
    eyelinkPrep(opt)
    try,opt.eyelinkPresent = Eyelink('IsConnected'); catch, opt.eyelinkPresent = 0; end
    if opt.eyelinkPresent,
        opt.eyeSide = Eyelink('EyeAvailable')+1;
    end
catch,
    opt.useEyelink = 0;
    opt.eyelinkPresent = 0;
    opt.eyeSide = 1;
end
opt.eyePresent = 0;

% screen variables
Screen('Preference', 'SkipSyncTests', opt.screenNumber);
PsychDefaultSetup(2);
[opt.window, opt.windowRect] = Screen('OpenWindow',opt.screenNumber, [0,0,0]);
Screen('BlendFunction', opt.window, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
Screen('TextSize', opt.window, 50);

opt.screenWidth = opt.windowRect(3);
opt.screenHeight = opt.windowRect(4);
opt.centerX = opt.screenWidth / 2;
opt.centerY = opt.screenHeight / 2;
opt.screenFlipHz = 60;
opt.screenFlipTime = 1/opt.screenFlipHz;

opt.backgroundColor = [100 100 100];

% feature variables
opt.features = {'shape', 'shadow', 'color', 'number'};
opt.shapes = {'triangle', 'square', 'star'};
opt.colors = {'red', 'green', 'blue'};
opt.numbers = {'1', '2', '3'};
opt.shadows = {'outline', 'filled', 'stripe'};

% options

end

function opt = makeScreenComponents(opt)

% shape size
opt.radius = opt.screenHeight / 16;

% card position
opt.card1X = opt.screenWidth / 4;
opt.card1Y = opt.screenHeight / 4;
opt.card2X = opt.screenWidth / 2;
opt.card2Y = opt.screenHeight / 4;
opt.card3X = opt.screenWidth * 3 / 4;
opt.card3Y = opt.screenHeight / 4;

% card size
opt.cardThick = 3;
opt.cardSizeX = opt.radius * 6 + 2 * opt.cardThick;
opt.cardSizeY = opt.radius * 3 + 2 * opt.cardThick;

% card outline
opt.card1Area = [opt.card1X - opt.cardSizeX / 2, opt.card1Y - opt.cardSizeY / 2, opt.card1X + opt.cardSizeX / 2, opt.card1Y + opt.cardSizeY / 2];
opt.card2Area = [opt.card2X - opt.cardSizeX / 2, opt.card2Y - opt.cardSizeY / 2, opt.card2X + opt.cardSizeX / 2, opt.card2Y + opt.cardSizeY / 2];
opt.card3Area = [opt.card3X - opt.cardSizeX / 2, opt.card3Y - opt.cardSizeY / 2, opt.card3X + opt.cardSizeX / 2, opt.card3Y + opt.cardSizeY / 2];

% option position
opt.optionLeftX = opt.screenWidth / 3;
opt.optionLeftY = opt.screenHeight * 3 / 4;
opt.optionRightX = opt.screenWidth * 2 / 3;
opt.optionRightY = opt.screenHeight * 3 / 4;
opt.optionUpX = opt.screenWidth / 2;
opt.optionUpY = opt.screenHeight / 2;

% option outline
opt.optionLeftArea = [opt.optionLeftX - opt.cardSizeX / 2, opt.optionLeftY - opt.cardSizeY / 2, opt.optionLeftX + opt.cardSizeX / 2, opt.optionLeftY + opt.cardSizeY / 2];
opt.optionRightArea = [opt.optionRightX - opt.cardSizeX / 2, opt.optionRightY - opt.cardSizeY / 2, opt.optionRightX + opt.cardSizeX / 2, opt.optionRightY + opt.cardSizeY / 2];
opt.optionUpArea = [opt.optionUpX - opt.cardSizeX / 2, opt.optionUpY - opt.cardSizeY / 2, opt.optionUpX + opt.cardSizeX / 2, opt.optionUpY + opt.cardSizeY / 2];

end