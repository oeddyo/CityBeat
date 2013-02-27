%{
@attribute AvgPhotoDis numeric
@attribute AvgPhotoDisbyCap numeric
@attribute Entropy numeric
@attribute diff_AvgPhotoDis numeric
@attribute diff_TopWordPopularity numeric
@attribute diff_Entropy numeric
@attribute NumberOfPhotsoContaingTopWord1 numeric
@attribute NumberOfPhotsoContaingTopWord2 numeric
@attribute NumberOfPhotsoContaingTopWord3 numeric
@attribute label {1,-1}
%}

A = load('reduced_balanced_unsparse_uniqueUser_allPhoto_historic.txt');

pos = A(1:131,:);
neg = A(132:end,:);

hist(pos(:,1));
hold on;
hist(neg(:,1));
 
h = findobj(gca,'Type','patch');
display(h)
set(h(1),'FaceColor','r','EdgeColor','k');
set(h(2),'FaceColor','g','EdgeColor','k');
