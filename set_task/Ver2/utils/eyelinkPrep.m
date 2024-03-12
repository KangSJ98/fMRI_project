function eyelinkPrep(opt)

if opt.useEyelink,
    % screen open
    Screen('Preference', 'SkipSyncTests' , 1);
    [window] = Screen('openWindow', opt.screenNumber, 0, [], 32, 2);
    [winWidth, winHeight] = WindowSize(window);
    
    % set eyelink
    el = EyelinkInitDefaults(window);
    
    el.backgroundcolour = GrayIndex(el.window);
    el.mshfontcolur = WhiteIndex(el.window);
    el.imgtititlecolour = WhiteIndex(el.window);
    el.targetbeep = 1;
    el.calibrationtargetcolour = WhiteIndex(el.window);
    el.calibrationtargetsize= 2.5;
    el.calibrationtargetwidth= 1;
    
    EyelinkUpdateDefaults(el);
    EyelinkInit(0);
    
    % open edf file
    %edfFile = 'Demo';
    %isnotopen = Eyelink('Openfile', edfFile);
    %if ~isnotopen, cleanup;return; end
    
    % eyelink config
    Eyelink('command' , 'add_file_preamble_text ''Recorded by Eyelink Trial game experiment''');
    Eyelink('command','screen_pixel_coords = %ld %ld %ld %ld', 0, 0, winWidth-1, winHeight-1);
    Eyelink('message', 'DISPLAY_COORDS %ld %ld %ld %ld', 0, 0, winWidth-1, winHeight-1);
    Eyelink('command', 'calibration_type = HV9');
    Eyelink('command', 'generate_default_targets = YES');
    Eyelink('command', 'saccade_velocity_threshold = 35');
    Eyelink('command', 'saccade_acceleration_threshold = 9500');
    [v,vs] = Eyelink('GetTrackerVersion');
    vsn = regexp(vs,'\d','match');
    Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT');
    Eyelink('command', 'link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,FIXUPDATE,INPUT');
    Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT');
    Eyelink('command', 'link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT');
    if (v ==3) && str2double(vsn{1}) == 4 % if EL 1000 and tracker version 4.xx
        Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT,HTARGET');
        Eyelink('command', 'link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT,HTARGET');
    end
    Eyelink('command', 'button_function 5 "accept_target_fixation"');
    
    % start calibrate
    EyelinkDoTrackerSetup(el);
    opt.el = el;
    
    Screen('Close',window)
    Eyelink( 'StartRecording' );
end
end



