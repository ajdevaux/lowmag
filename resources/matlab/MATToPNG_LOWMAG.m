function MATToPNG_LOWMAG(data, fn)

if nargin < 2
    fn = 'capture.png';
end



for i = 1:4
    max_t = max(max(data(i,:,:)));
    if (max_t) > 1
        div_v = max_t;
    else
        div_v = 1.0;
    end
    data_t(:,:,1) = data(i,:,:)/div_v;
    data_t(:,:,2) = data(i,:,:)/div_v;
    data_t(:,:,3) = data(i,:,:)/div_v;

    IMG = uint16(fix(2^16 * data_t));
    imwrite(IMG, [fn num2str(i) '.png'],'png');
end