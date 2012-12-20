function [ validate_res ] = validate( prediction, ground_truth, evaluate_method )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

data_length = length(prediction);

if length(prediction) ~= length(ground_truth)
    fprintf('Error: length of prediction and ground truth are not the same');
end

if evaluate_method==1
    validate_res = sum(abs( prediction-ground_truth))/(1.0*data_length);
else
    validate_res = sum( (prediction-ground_truth).^2)/(1.0*data_length);
end


end

