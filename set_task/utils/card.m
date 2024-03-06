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
        
        function tf = isequal(obj1, obj2)
            tf = isequal(obj1.shape, obj2.shape) && ...
                 isequal(obj1.color, obj2.color) && ...
                 isequal(obj1.number, obj2.number) && ...
                 isequal(obj1.shadow, obj2.shadow);
        end
    end
end
