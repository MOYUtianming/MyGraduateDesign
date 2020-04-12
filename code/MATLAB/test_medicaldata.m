%MerchData.zip is a built-in dataset
unzip('.\dataset\medicaldata.zip');
%imageDatastore function is used to import an image dataset without paying
%attention to included elements' size ;
imds = imageDatastore('medicaldata', ...
    'IncludeSubfolders',true, ...
    'LabelSource','foldernames');
%splitEachLabel function is used to split a dataset in different size;
%'randomized' keyword means  randomly assigns the specified proportion of files from each label to the new datastores.
[imdsTrain,imdsTest] = splitEachLabel(imds,0.7,'randomized');
%numel function is used to get the length of an array
numImagesTrain = numel(imdsTrain.Labels);
%randperm function return a row vector that ramdom the purmulation of 1 --
%n(or output 'k' numbers within 1 to n,if input two parameters) intgers;
idx = randperm(numImagesTrain,14);

for i = 1:7
    I{i} = readimage(imdsTrain,idx(i));
end

 figure
 imshow(imtile(I))

net = alexnet;
net.Layers
inputSize = net.Layers(1).InputSize

augimdsTrain = augmentedImageDatastore(inputSize(1:2),imdsTrain);
augimdsTest = augmentedImageDatastore(inputSize(1:2),imdsTest);
% use the deeper layers' features to predict;('fc7' is a layer in this net)
layer = 'fc7';
featuresTrain = activations(net,augimdsTrain,layer,'OutputAs','rows');
featuresTest = activations(net,augimdsTest,layer,'OutputAs','rows');

YTrain = imdsTrain.Labels;
YTest = imdsTest.Labels;

mdl = fitcecoc(featuresTrain,YTrain);
% predict the test dataset based on the 'mdl' model ,featuresTest is the
% features extracted from test dataset;
YPred = predict(mdl,featuresTest);

idx = [1:20]
figure
for i = 1:numel(idx)
    subplot(4,5,i)
    I = readimage(imdsTest,idx(i));
    label = YPred(idx(i));
    
    imshow(I)
    title(label)
end

accuracy = mean(YPred == YTest)

