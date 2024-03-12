function wrongCard = calculateWrongCard(answerCard, opt)
wrongCard = card();

shape_candidates = opt.shapes(~ismember(opt.shapes, {answerCard.shape}));
wrongCard.shape = shape_candidates{randi(length(shape_candidates))};

color_candidates = opt.shapes(~ismember(opt.shapes, {answerCard.shape}));
wrongCard.color = color_candidates{randi(length(color_candidates))};

number_candidates = opt.shapes(~ismember(opt.shapes, {answerCard.shape}));
wrongCard.number = number_candidates{randi(length(number_candidates))};

shadow_candidates = opt.shapes(~ismember(opt.shapes, {answerCard.shape}));
wrongCard.shadow = shadow_candidates{randi(length(shadow_candidates))};

end

