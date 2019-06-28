function MATToPNGDirectory(dd)

if nargin < 1
    dd = pwd();
end

list_f = dir([dd '\*DataSet*.mat']);

for i = [1:size(list_f,1)]
    fprintf('%s\n',list_f(i).name);
    load(list_f(i).name);
    new_fn = list_f(i).name;
    new_fn = [new_fn(1:end-4) '.png'];
    MATToPNG(data, new_fn);
end