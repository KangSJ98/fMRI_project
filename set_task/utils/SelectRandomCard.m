function selectedCard = SelectRandomCard()
    % shape, color, number, shadow를 무작위로 선택
    random_shape_idx = randi(length(opt.shapes));
    random_color_idx = randi(length(opt.colors));
    random_number_idx = randi(length(opt.numbers));
    random_shadow_idx = randi(length(opt.shadows));
    
    % 무작위로 선택한 속성으로 card 생성
    selectedCard = card(opt.shapes{random_shape_idx}, opt.colors{random_color_idx}, ...
                        opt.numbers(random_number_idx), opt.shadows{random_shadow_idx});
end
