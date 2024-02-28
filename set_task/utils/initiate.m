function opt = initiate()
%% Psychtoolbox initiate
screens = 2;% Screen('Screens'); % 2
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

opt.trNum = 1000;

% 도형 크기 설정
opt.radius = 5;

% 가능한 속성 목록 정의
opt.shapes = {'triangle', 'square', 'star'};
opt.colors = {'red', 'green', 'blue'};
opt.numbers = [1, 2, 3];
opt.shadows = {'outline', 'filled', 'stripe'};

end

