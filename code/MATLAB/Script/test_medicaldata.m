%0. unzip dataset.
% unzip('.\dataset\medicaldata.zip');

%1. imageDatastore function is used to import an image dataset without paying
%attention to included elements' size ;
m_imds = imageDatastore('../Dataset/Resnetdata', ...
    'IncludeSubfolders',true, ...
    'LabelSource','foldernames');

%2. preprocess images
%splitEachLabel function is used to split a dataset in different size;
%'randomized' keyword means  randomly assigns the specified proportion of files from each label to the new datastores.
[TrainImds,TestImds] = splitEachLabel(m_imds,0.7,'randomized');

augTrainImds = augmentedImageDatastore([227,227],TrainImds,'ColorPreprocessing','gray2rgb');
augTestImds = augmentedImageDatastore([227,227],TestImds,'ColorPreprocessing','gray2rgb');

%3. numel function is used to get the length of an array
    numClasses = numel(categories(m_imds.Labels));
    idx = (1:numel(TestImds.Labels));
    U = TestImds.Labels;
    
%4. import network
    net = alexnet;
layers = layerGraph(net.Layers);
%5. set parameters and modify layers
    %inputSize = net.Layers(1).InputSize
    newLearnableLayer = fullyConnectedLayer(numClasses,'Name','new_fc');
    layers = replaceLayer(layers,'fc8',newLearnableLayer);

    newsoftmaxLayer = softmaxLayer('Name','new_softmax');
    layers = replaceLayer(layers,'prob',newsoftmaxLayer);
    
    newClassLayer = classificationLayer('Name','new_classoutput');
    layers = replaceLayer(layers,'output',newClassLayer);
    % set training gradient descent step length
    options = trainingOptions('sgdm',...
    'InitialLearnRate', 0.001,...
    'Plots','training-progress');
    
%6. train network
[mnet01,info] = trainNetwork(augTrainImds, layers, options);
%test
testpreds = classify(mnet01,augTestImds);

%7. plot

% figure
% for i = 1:numel(idx)
%     subplot(1,numel(idx),i)
%     I = readimage(TestImds,idx(i));
%     label = testpreds(idx(i));
%     
%     imshow(I)
%     title(label)
% end
    plotconfusion(U,testpreds)
    title('ConfusionMatrix:AlexNet');




