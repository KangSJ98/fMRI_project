function DisplayCard(card, x, y)
% 중심점 좌표
center_x = x;
center_y = y;

switch card.color
    case 'red'
        color = 'r';
    case 'blue'
        color = 'b';
    case 'green'
        color = 'g';
end

switch card.shape
    case 'triangle'
        % 정삼각형의 세 꼭지점 좌표 계산
        points_x = [center_x, center_x + opt.radius * cosd(0), center_x + opt.radius * cosd(120)];
        points_y = [center_y, center_y + opt.radius * sind(0), center_y + opt.radius * sind(120)];
    case 'rectangle'
        % 사각형의 네 꼭지점 좌표 계산
        half_side = side_length / 2;
        points_x = [center_x - half_side, center_x + half_side, center_x + half_side, center_x - half_side];
        points_y = [center_y - half_side, center_y - half_side, center_y + half_side, center_y + half_side];
    case 'star'
        % 별의 다섯 개 꼭지점 좌표 계산
        angles = linspace(0, 2*pi, 5);
        points_x = center_x + opt.radius * cos(angles);
        points_y = center_y + opt.radius * sin(angles);
    case 'circle'
        % 원의 좌표 계산
        theta = linspace(0, 2*pi, 100); % 원을 그리기 위한 각도 범위
        circle_x = opt.radius * cos(theta) + center_x; % x 좌표
        circle_y = opt.radius * sin(theta) + center_y; % y 좌표
        points_x = circle_x;
        points_y = circle_y;
end

switch card.number
    case 1
        DrawShape(points_x, points_y, color, card.shadow)
    case 2
        DrawShape(x - opt.radius, y, color);
        DrawShape(x + opt.radius, y, color);
    case 3
        DrawShape(x - 2 * opt.radius, y, color);
        DrawShape(x, y, color);
        DrawShape(x + 2 * opt.radius, y, color);
end
end

function DrawShape(points_x, points_y, color, shadow)
switch shadow
    case 'outline'
        fill(points_x, points_y, 'w', 'EdgeColor', color);
    case 'filled'
        fill(points_x, points_y, color);
    case 'stripe'
        fill(points_x, points_y, color); % 도형 내부를 채우기
        hold on;
        axis tight;
        axis equal;
        x_range = [min(points_x), max(points_x)]; % x 좌표 범위
        y_range = [min(points_y), max(points_y)]; % y 좌표 범위
        for y = y_range(1):0.1:y_range(2) % y 좌표 범위에 따라 루프
            plot(x_range, [y, y], 'Color', 'w', 'LineWidth', 1); % 줄무늬 그리기
        end
        hold off;
end
end
