function WhiteOut(opt)
Screen('FillRect', opt.window, [255 255 255], [0, 0, opt.screenWidth, opt.screenHeight]);
Screen('Flip', opt.window);
startTime = GetSecs;
while GetSecs - startTime <= 0.5 + (0.7 - 0.5) * rand
end
end
