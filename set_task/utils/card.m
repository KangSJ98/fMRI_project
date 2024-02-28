classdef card
    properties
        shape
        color
        number
        shadow
    end
    methods
        function obj = card(shape, color, number, shadow)
            if nargin < 1
                shape = 'circle';
                color = 'black';
                number = '1';
                shadow = 'filled';
            end
            obj.shape = shape;
            obj.color = color;
            obj.number = number;
            obj.shadow = shadow;
        end
    end
end
