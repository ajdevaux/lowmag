function StackToPNG(fn)

if nargin < 2
    fn = 'zstack21DataSet';
end


load(fn)
frames = size(zStack.slice,2);

for i = 1:frames
    im = zStack.slice(i).image;
    fn_png = [fn '_' num2str(i) '.png'];
    MATToPNG(im, fn_png);
end