precision =[0.658, 0.636, 0.604, 0.569, 0.537, 0.5, 0.5, 0.492, 0.484, 0.469];
recall= [0.735, 0.824, 0.853, 0.853, 0.853, 0.853, 0.882, 0.882, 0.882, 0.882];


plot(recall, precision, '--'); hold on
plot(recall, precision, 'r*')
xlabel('recall')
ylabel('precision')
title('Logistic Regression on Next Week Data');