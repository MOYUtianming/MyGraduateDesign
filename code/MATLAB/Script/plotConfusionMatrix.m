%5. ConfusionMatrix
function plotConfusionMatrix(alabelset,plabelset)
%ActualLabels
    actual_labels=alabelset;
    predicted_labels=plabelset;
%show
    figure;
    plotconfusion(actual_labels,predicted_labels)
    title('ConfusionMatrix:ResNet');