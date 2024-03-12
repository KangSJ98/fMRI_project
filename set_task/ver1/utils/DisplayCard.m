function DisplayCard(card, center_x, center_y, opt)
%% 색상 설정
switch card.color
    case 'red'
        color = [255 0 0]; % 빨간색
    case 'blue'
        color = [0 0 255]; % 파란색
    case 'green'
        color = [0 255 0]; % 초록색
    case 'black'
        color = [0 0 0]; % 검정색
    otherwise
        color = [255 255 255]; % 기본값은 흰색
end

%% 도형 개수 설정
switch card.number
    case '1'
        DrawShape(center_x, center_y, color, card, opt)
    case '2'
        DrawShape(center_x - opt.radius, center_y, color, card, opt);
        DrawShape(center_x + opt.radius, center_y, color, card, opt);
    case '3'
        DrawShape(center_x - 2 * opt.radius, center_y, color, card, opt);
        DrawShape(center_x, center_y, color, card, opt);
        DrawShape(center_x + 2 * opt.radius, center_y, color, card, opt);
end

end

% 도형 그리는 함수
function DrawShape(center_x, center_y, color, card, opt)
%% 도형 모양
switch card.shape
    % 삼각형
    case 'triangle'
        % 정삼각형의 세 꼭지점 좌표 계산
        angles = [60, 180, 300];
        points_x = center_x + opt.radius * sind(angles);
        points_y = center_y + opt.radius * cosd(angles);
        % 삼각형 그리기
        Screen('FillPoly', opt.window, color, [points_x; points_y]', 1);
        if strcmp('outline', card.shadow)
            outline_x = center_x + opt.radius * sind(angles) * 0.9;
            outline_y = center_y + opt.radius * cosd(angles) * 0.9;
            Screen('FillPoly', opt.window, [255 255 255], [outline_x; outline_y]', 1);
        end
    % 사각형
    case 'square'
        % 정사각형의 세 꼭지점 좌표 계산
        angles = [45, 135, 225, 315];
        points_x = center_x + opt.radius * sind(angles);
        points_y = center_y + opt.radius * cosd(angles);
        % 삼각형 그리기
        Screen('FillPoly', opt.window, color, [points_x; points_y]', 1);
        if strcmp('outline', card.shadow)
            outline_x = center_x + opt.radius * sind(angles) * 0.9;
            outline_y = center_y + opt.radius * cosd(angles) * 0.9;
            Screen('FillPoly', opt.window, [255 255 255], [outline_x; outline_y]', 1);
        end
    % 별
    case 'star'
        % 정삼각형의 세 꼭지점 좌표 계산
        angles = [60, 180, 300];
        points_x = center_x + opt.radius * sind(angles);
        points_y = center_y + opt.radius * cosd(angles);
        % 삼각형 그리기
        Screen('FillPoly', opt.window, color, [points_x; points_y]', 1);
        % 뒤집은 정삼각형의 세 꼭지점 좌표 계산
        angles = [0, 120, 240];
        points_x = center_x + opt.radius * sind(angles);
        points_y = center_y + opt.radius * cosd(angles);
        % 뒤집은 삼각형 그리기
        Screen('FillPoly', opt.window, color, [points_x; points_y]', 1);
        if strcmp('outline', card.shadow)
            outline_x = center_x + opt.radius * sind(angles) * 0.9;
            outline_y = center_y + opt.radius * cosd(angles) * 0.9;
            Screen('FillPoly', opt.window, [255 255 255], [outline_x; outline_y]', 1);
            angles = [60, 180, 300];
            outline_x = center_x + opt.radius * sind(angles) * 0.9;
            outline_y = center_y + opt.radius * cosd(angles) * 0.9;
            Screen('FillPoly', opt.window, [255 255 255], [outline_x; outline_y]', 1);
        end
    % 원
    case 'circle'
        Screen('FillOval', opt.window, color, [center_x - opt.radius, center_y - opt.radius, center_x + opt.radius, center_y + opt.radius]);
        if strcmp('outline', card.shadow)
            Screen('FillOval', opt.window, [255 255 255], [center_x - opt.radius * 0.9, center_y - opt.radius * 0.9, center_x + opt.radius * 0.9, center_y + opt.radius * 0.9]);
        end
end

%% stripe인 경우 가로 줄무늬 추가
if strcmp(card.shadow, 'stripe')
    % 좌상단 좌표와 우하단 좌표 계산
    rect_left = center_x - opt.radius;
    rect_top = center_y - opt.radius;
    rect_right = center_x + opt.radius;
    rect_bottom = center_y + opt.radius;
    
    % 영역의 높이 계산
    rect_height = rect_bottom - rect_top;
    
    % 영역의 너비 계산
    rect_width = rect_right - rect_left;
    
    % 영역을 20등분하여 각 영역의 높이 계산
    stripe_height = rect_height / 21;
    
    % 홀수 번째 영역만 흰색으로 채우기
    for i = 2:2:20
        % 홀수 번째 영역의 상단, 하단 좌표 계산
        stripe_top = rect_top + (i - 1) * stripe_height;
        stripe_bottom = stripe_top + stripe_height;
        
        % 영역 채우기
        Screen('FillRect', opt.window, [255 255 255], [rect_left, stripe_top, rect_right, stripe_bottom]);
    end
end

end