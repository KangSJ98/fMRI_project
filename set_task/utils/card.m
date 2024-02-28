classdef card
    properties
        shape
        color
        number
        shadow
    end
    methods
        function obj = main(shape, color, number, shadow)
            obj.shape = shape;
            obj.color = color;
            obj.number = number;
            obj.shadow = shadow;
        end
    end
end