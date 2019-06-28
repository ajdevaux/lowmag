function MATToPNG(data, fn)

if nargin < 2
    fn = 'capture.png';
end

max_t = max(max(data));
if (max_t) > 1
    div_v = max_t;
else
    div_v = 1.0;
end

data_t(:,:,1) = data/div_v;
data_t(:,:,2) = data/div_v;
data_t(:,:,3) = data/div_v;

IMG = uint16(fix(2^16 * data_t));
imwrite(IMG, fn,'png');