function selectedCard = selectRandomCard(opt)
    % shape, color, number, shadow를 무작위로 선택
    random_shape_idx = randi(length(opt.shapes));
    random_shadow_idx = randi(length(opt.shadows));
    random_color_idx = randi(length(opt.colors));
    random_number_idx = randi(length(opt.numbers));
    
    % 무작위로 선택한 속성으로 card 생성
    selectedCard = card(opt.shapes{random_shape_idx}, opt.shadows{random_shadow_idx}, ...
                        opt.colors{random_color_idx}, opt.numbers{random_number_idx});
end
