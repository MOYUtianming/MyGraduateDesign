% Close all;
clear; close all; clc;

% 1. LOAD dataset :
    % set datapath;
    datapath =  '../Dataset/Resnetdata';

    % load dataset;
    imds = imageDatastore(datapath, ...
        'IncludeSubfolders', true, ...
        'LabelSource',  'foldernames');

    % determine the split categories;
    total_split = countEachLabel(imds);

%2. VISUALIZE images:

    % count images;
    num_images = length(imds.Labels);

    % random permulation for imagelist including 6 unique numbers selected from num_aimds;
    % perm = randperm(num_images,6);
    % figure;
    % for idx = 1 : length(perm)
        % subplot(2,3,idx)
        % use prebuilt random matrix 'perm'
        % imshow(imread(imds.Files{perm(idx)}));
        % title(sprintf('%s',imds.Labels(perm(idx))));
    % end



%4. TRAIN Network & PREPROCESS images:
    %Number of folds
    num_folds=10;

    % create space for predicted_labels and posterior_t 
    predicted_labels = categorical(zeros(1,41));
    scores_t = single(zeros(41,2));
    %Loop for each fold
    for fold_idx=1:num_folds
        
    % fprintf
    % format the data and display them on the screen.

        fprintf('Processing %d among %d folds \n',fold_idx,num_folds);
        
    %TestIndicesfor current fold
        test_idx=fold_idx:num_folds:num_images;

        %Test cases for current fold
        imdsTest = subset(imds,test_idx);
        
    %Train indices for current fold
        train_idx=setdiff(1:length(imds.Files),test_idx);
        
    %Train cases for current fold
        imdsTrain = subset(imds,train_idx);
    
    %ResNetArchitecture
        net=resnet50;
        lgraph = layerGraph(net);
        clear net;
        
        %Number of categorie
        numClasses = numel(categories(imdsTrain.Labels));
        
        %Replacing the last layers withnew layers
        %NewLearnableLayer
        newLearnableLayer = fullyConnectedLayer(numClasses,...
            'Name','new_fc',...
            'WeightLearnRateFactor',10,...
            'BiasLearnRateFactor',10);
        lgraph = replaceLayer(lgraph,'fc1000',newLearnableLayer);
        newsoftmaxLayer = softmaxLayer('Name','new_softmax');
        lgraph = replaceLayer(lgraph,'fc1000_softmax',newsoftmaxLayer);
        newClassLayer = classificationLayer('Name','new_classoutput');
        lgraph = replaceLayer(lgraph,'ClassificationLayer_fc1000',newClassLayer);
        
        
    %PreprocessingTechnique
        imdsTrain.ReadFcn=@(filename)preprocess_Xray(filename);
        imdsTest.ReadFcn=@(filename)preprocess_Xray(filename);
        
    %TrainingOptions, we choose a small mini-batch size due to limited images
    % verbose：Log Display
        % verbose = 0 NOT display Log in stdout;
        % verbose = 1 display Log in stdout(default);
        % verbose = 2 display Log for each epoch;
    % use training-progress to plot the realtime training status
        options = trainingOptions('adam',...
            'MaxEpochs',30,'MiniBatchSize',8,...
            'Shuffle','every-epoch',...
            'InitialLearnRate',1e-4,...
            'Verbose',0,...
            'Plots','training-progress');
        
    %DataAugumentation
        % set augmentation options :
        % ROTATION TRANSFORMATION
        % set RandRotation as '[-5 5]' so the image will be randomly rotated an angle specified from the range [-5 5];
        % REFLECTION TRANSFORMATION
        % set RandXReflection as 'true' so the images will be randomly reflected with 50% probability;(if it is 'false',the images will not change)
        % set RandYReflection's requirement is similar to RandXReflection's.
        % SHEAR TRANSFORMATION
        % set RandXShear as '[-0.05 0.05]' so the images will be randomly sheared an angle specified from the range [-0.05 0.05]
        augmenter = imageDataAugmenter(...
            'RandRotation',[-5 5],'RandXReflection',true,...
            'RandYReflection',true,'RandXShear',[-0.05 0.05],'RandYShear',[-0.05 0.05]);
        
        %Resizing all training images to [224 224]forResNet architecture
        % ZOOM TRANSFORMATION for net adaption.
        % load option of augmentation.
        auimds = augmentedImageDatastore([224 224],imdsTrain,'DataAugmentation',augmenter);
        
    %Training
        netTransfer = trainNetwork(auimds,lgraph,options);
        
    %Resizing all testing images to [224224]forResNet architecture
        augtestimds = augmentedImageDatastore([224 224],imdsTest);
    
    %Testing and their corresponding Labels and Posterior for each Case
    % size of predicted_labels is 1height*41width
    % size of posterior is 41height*2width

        [predicted_labels(test_idx),scores_t(test_idx,:)]= classify(netTransfer,augtestimds);
        
        %Save the IndependentResNetArchitectures obtained for each Fold
        save(sprintf('ResNet50_%d_among_%d_folds',fold_idx,num_folds),'netTransfer','test_idx','train_idx');
        
    %Clearing unnecessary variables
        clearvars -except fold_idx num_folds num_images predicted_labels posterior imds netTransfer;
        
    end

%5. ConfusionMatrix
    %ActualLabels
    actual_labels=imds.Labels;

    figure;
    plotconfusion(actual_labels,predicted_labels)
    title('ConfusionMatrix:ResNet');