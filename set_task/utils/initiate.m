function opt = initiate()
%% Psychtoolbox initiate
screens = 1;% Screen('Screens'); % 2
Screen('Preference', 'SkipSyncTests', screens);
PsychDefaultSetup(2);
InitializePsychSound(1);
screenNumber = max(screens);
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
[opt.window, opt.windowRect] = PsychImaging('OpenWindow', screenNumber, white);

%% parameter
% Calculate screen size and center
opt.screenWidth = opt.windowRect(3);
opt.screenHeight = opt.windowRect(4);
opt.centerX = opt.screenWidth / 2;
opt.centerY = opt.screenHeight / 2;

% card1, 2, 3 (x,y) position
opt.card1X = opt.screenWidth / 4;
opt.card1Y = opt.screenHeight / 4;
opt.card2X = opt.screenWidth / 2;
opt.card2Y = opt.screenHeight / 4;
opt.card3X = opt.screenWidth * 3 / 4;
opt.card3Y = opt.screenHeight / 4;

% option (x,y) position
opt.optionLeftX = opt.screenWidth / 3;
opt.optionLeftY = opt.screenHeight * 3 / 4;
opt.optionRightX = opt.screenWidth * 2 / 3;
opt.optionRightY = opt.screenHeight * 3 / 4;

opt.trNum = 100;

% 도형 크기 설정
opt.radius = opt.screenHeight / 16;

% 가능한 속성 목록 정의
opt.features = {'shape', 'color', 'number', 'shadow'};
opt.shapes = {'triangle', 'square', 'star'};
opt.colors = {'red', 'green', 'blue'};
opt.numbers = {'1', '2', '3'};
opt.shadows = {'outline', 'filled', 'stripe'};

end

