function [ training, testing ] = data_split( data, ratio )
%split the data into training and test.
%   ratio% of training, and 1-ratio of testing

data_length = length(data);
train_length = round(ratio*data_length);
training = data(1:train_length, :);
testing = data(train_length+1:data_length, :);


end

