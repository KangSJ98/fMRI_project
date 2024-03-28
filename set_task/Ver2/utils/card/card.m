classdef card
    properties
        shape
        shadow
        color
        number
    end
    
    methods
        function obj = card(shape, shadow, color, number)
            if nargin < 1
                shape = 'circle';
                shadow = 'filled';
                color = 'black';
                number = '1';
            end
            obj.shape = shape;
            obj.shadow = shadow;
            obj.color = color;
            obj.number = number;
        end
        
        function tf = isequal(obj1, obj2)
            tf = isequal(obj1.shape, obj2.shape) && ...
                 isequal(obj1.color, obj2.color) && ...
                 isequal(obj1.number, obj2.number) && ...
                 isequal(obj1.shadow, obj2.shadow);
        end
    end
end
