function c_data = eliminate_outlier(data,sigma_level)

sz = length(data);
dt = zeros(24,1);
ct = zeros(24,1);
i = 1;
cnt = 1;
bins = zeros(15,24);
day = 1;
while i<=sz
    dt(cnt) = data(i,2);
    ct(cnt) = ct(cnt) + 1;
    if cnt<24
        cnt = cnt+1;
    else
        cnt = 1;
        bins(day,:) = dt;
        day = day+1;
    end
    i= i + 1; 
end

outlier = (std(bins)*sigma_level + mean(bins));

%[I J V] ;
W = (bins<repmat(outlier, 15,1));
A = reshape(W',size(W,1)*size(W,2),1);

sz = length(data);

data(A(1:sz)==0,2) = -1;

c_data = data;

end
