function DisplayOption(feature, option, opt, playerShape)
% optionLeft = card();
% optionRight = card();
optionLeft = playerShape;
optionRight = playerShape;

optionLeft.(feature) = option{1};
optionRight.(feature) = option{2};

DisplayCard(optionLeft, opt.optionLeftX, opt.optionLeftY, opt);
DisplayCard(optionRight, opt.optionRightX, opt.optionRightY, opt);

end

