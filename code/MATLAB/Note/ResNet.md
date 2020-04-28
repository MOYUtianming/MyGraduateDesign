# ResNet 学习笔记

## 论文主要内容

1. 工具及工具的使用环境配置
2. 学科背景
3. 语言(相关学习途径)
4. 引用/致谢

## 小数据集应对过拟合的方法

1. 每个 _fold_ (折,即对整个图像集的一轮训练) 开始训练之前
   有概率进行AffineTransformation(即仿射变换,允许图像任意倾斜,任意伸缩)中的两种变换
   ( 排除了
   必须要进行的 ZoomTransformation (缩放变换) <为了适应网络入口> 和
   无扰动意义的TranslationTransformation (平移变换) ):

    * 有概率进行 RotationTransformation (旋转变换) , 旋转的角度在预设的范围内 (备选集范围为(-90,90)) 随机选取;

    * 有概率进行 ShearTransformation (剪切变换) , 剪切的角度在预设的范围内 (备选集范围为(-90,90)) 随机选取;

2. 每个 _fold_ 开始训练之前
   有概率进行 ReflectionTransformation (反射变换) , 当参数设置为 ‘true’ 时 每次预处理对每一张图都有 50% 的概率进行反射变换, 即图像转变为其中心对称图形;

## 附录1: 各类函数、关键字及其参数简介

1. _function_ imageDatastore
   [Placeholder]
2. _function_ countEachLabel
   [Placeholder]
3. _function_ length
   [Placeholder]
4. _function_ randperm
   [Placeholder]
5. _function_ zeros
   [Placeholder]
6. _keyword_ categorical / single
   使用类似categorical(< matrixName >) 的结构可以将matrix由原有类型强制转换为如categorical这样的另一类型,在本程序中我用该语法和zeros函数来为scores_t 和 predicted_labels 两个变量提供预缓存区;
7. _keyword_ for 
   for indexName=values
      statements;
   end
   其中:
   indexName 是实时的循环序号;
   values 用于指定index的范围和变化算法,其形式可以是各种形式的矩阵(包括普通行向量,等差序列,n阶单位矩阵等);
      e.g:  1:3;
            1:-0.1:0;
            [1 5 8 2];(指定循环中需要操作的时刻)
            eye(1,2);单位阵
            ...
   statements 指每次循环中需要执行的语句;
8. _function_ fopen
   fileID = fopen(filename);
9. _function_ fprintf([ fileID ],'strings and dataFormats',dataname1,dataname2,...);
   format output function.
   不指定fileID 时,用于将格式化的带数据字符串输出到stdout中(类似C语言中的printf)。
   指定fileID 时,用于将格式化的带数据字符串输出到fileID指向的文件中;
10. _keyword_ **:**
   **:** 一共有以下几种常见用法;
      * 创建向量(序列)
         * 创建序列 J:K <=> J,J+1,J+2,...K-1,K

         * 创建等差序列 J:I:K

      * 数组(矩阵)下标(选取用)
         * A(:,n),选取A 的第n列;

         * A(m,:),选取A的第m行;

         * A([ j:k ],[ a:b ]),选取A的j~k行中对应A中a~b列的内容;

         * for loop 中的循环次数指定;(参见for的介绍)
11. _function_ subset
      用于从大数据集中提取指定序列的数据元素;
      mininset01 = subset(originsetName,seriesNumberMatrixName);
12. _function_ setdiff
      用于求两个数组的元素种类差异;
      miniset02 = setdiff(A,B);
      在本次程序设计中用于求出总数据集中除了测试集之外的所有图像的序号(与subset搭配使用来组建训练集)
13. _net_ resnet50
      用于导入resnet50网络(要求已经配置好该网络)
      net01 = resnet50;
14. _function_ layerGraph
      用于提取输入的DAG ( Directed acyclic graph ) [ 有向无环图 ]型网络本身或者顺序网络的 Layers 参数 对应的的网络构型;
      当无输入参数时,会创建一个空的网络构型对象容器;
      对于DAGNetwork,直接使用 lgraphName = layerGraph(netName);
      对于SeriesNetwork,需要使用 lgraphName = layerGraph(netName.Layers);
15. _keyword_ clear
      用于清理变量;
      clear variableName01,vN02,...//清理指定
      clear all;// 清理所有;

## 附录2: resnet-50 层说明

  177x1 Layer array with layers:

     1   'input_1'                      Image Input             224x224x3 images with 'zerocenter' normalization
     2   'conv1'                        Convolution             64 7x7x3 convolutions with stride [2  2] and padding [3  3  3  3]
     3   'bn_conv1'                     Batch Normalization     Batch normalization with 64 channels
     4   'activation_1_relu'            ReLU                    ReLU
     5   'max_pooling2d_1'              Max Pooling             3x3 max pooling with stride [2  2] and padding [0  0  0  0]
     6   'res2a_branch2a'               Convolution             64 1x1x64 convolutions with stride [1  1] and padding [0  0  0  0]
     7   'bn2a_branch2a'                Batch Normalization     Batch normalization with 64 channels
     8   'activation_2_relu'            ReLU                    ReLU
     9   'res2a_branch2b'               Convolution             64 3x3x64 convolutions with stride [1  1] and padding 'same'
    10   'bn2a_branch2b'                Batch Normalization     Batch normalization with 64 channels
    11   'activation_3_relu'            ReLU                    ReLU
    12   'res2a_branch2c'               Convolution             256 1x1x64 convolutions with stride [1  1] and padding [0  0  0  0]
    13   'res2a_branch1'                Convolution             256 1x1x64 convolutions with stride [1  1] and padding [0  0  0  0]
    14   'bn2a_branch2c'                Batch Normalization     Batch normalization with 256 channels
    15   'bn2a_branch1'                 Batch Normalization     Batch normalization with 256 channels
    16   'add_1'                        Addition                Element-wise addition of 2 inputs
    17   'activation_4_relu'            ReLU                    ReLU
    18   'res2b_branch2a'               Convolution             64 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    19   'bn2b_branch2a'                Batch Normalization     Batch normalization with 64 channels
    20   'activation_5_relu'            ReLU                    ReLU
    21   'res2b_branch2b'               Convolution             64 3x3x64 convolutions with stride [1  1] and padding 'same'
    22   'bn2b_branch2b'                Batch Normalization     Batch normalization with 64 channels
    23   'activation_6_relu'            ReLU                    ReLU
    24   'res2b_branch2c'               Convolution             256 1x1x64 convolutions with stride [1  1] and padding [0  0  0  0]
    25   'bn2b_branch2c'                Batch Normalization     Batch normalization with 256 channels
    26   'add_2'                        Addition                Element-wise addition of 2 inputs
    27   'activation_7_relu'            ReLU                    ReLU
    28   'res2c_branch2a'               Convolution             64 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    29   'bn2c_branch2a'                Batch Normalization     Batch normalization with 64 channels
    30   'activation_8_relu'            ReLU                    ReLU
    31   'res2c_branch2b'               Convolution             64 3x3x64 convolutions with stride [1  1] and padding 'same'
    32   'bn2c_branch2b'                Batch Normalization     Batch normalization with 64 channels
    33   'activation_9_relu'            ReLU                    ReLU
    34   'res2c_branch2c'               Convolution             256 1x1x64 convolutions with stride [1  1] and padding [0  0  0  0]
    35   'bn2c_branch2c'                Batch Normalization     Batch normalization with 256 channels
    36   'add_3'                        Addition                Element-wise addition of 2 inputs
    37   'activation_10_relu'           ReLU                    ReLU
    38   'res3a_branch2a'               Convolution             128 1x1x256 convolutions with stride [2  2] and padding [0  0  0  0]
    39   'bn3a_branch2a'                Batch Normalization     Batch normalization with 128 channels
    40   'activation_11_relu'           ReLU                    ReLU
    41   'res3a_branch2b'               Convolution             128 3x3x128 convolutions with stride [1  1] and padding 'same'
    42   'bn3a_branch2b'                Batch Normalization     Batch normalization with 128 channels
    43   'activation_12_relu'           ReLU                    ReLU
    44   'res3a_branch2c'               Convolution             512 1x1x128 convolutions with stride [1  1] and padding [0  0  0  0]
    45   'res3a_branch1'                Convolution             512 1x1x256 convolutions with stride [2  2] and padding [0  0  0  0]
    46   'bn3a_branch2c'                Batch Normalization     Batch normalization with 512 channels
    47   'bn3a_branch1'                 Batch Normalization     Batch normalization with 512 channels
    48   'add_4'                        Addition                Element-wise addition of 2 inputs
    49   'activation_13_relu'           ReLU                    ReLU
    50   'res3b_branch2a'               Convolution             128 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    51   'bn3b_branch2a'                Batch Normalization     Batch normalization with 128 channels
    52   'activation_14_relu'           ReLU                    ReLU
    53   'res3b_branch2b'               Convolution             128 3x3x128 convolutions with stride [1  1] and padding 'same'
    54   'bn3b_branch2b'                Batch Normalization     Batch normalization with 128 channels
    55   'activation_15_relu'           ReLU                    ReLU
    56   'res3b_branch2c'               Convolution             512 1x1x128 convolutions with stride [1  1] and padding [0  0  0  0]
    57   'bn3b_branch2c'                Batch Normalization     Batch normalization with 512 channels
    58   'add_5'                        Addition                Element-wise addition of 2 inputs
    59   'activation_16_relu'           ReLU                    ReLU
    60   'res3c_branch2a'               Convolution             128 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    61   'bn3c_branch2a'                Batch Normalization     Batch normalization with 128 channels
    62   'activation_17_relu'           ReLU                    ReLU
    63   'res3c_branch2b'               Convolution             128 3x3x128 convolutions with stride [1  1] and padding 'same'
    64   'bn3c_branch2b'                Batch Normalization     Batch normalization with 128 channels
    65   'activation_18_relu'           ReLU                    ReLU
    66   'res3c_branch2c'               Convolution             512 1x1x128 convolutions with stride [1  1] and padding [0  0  0  0]
    67   'bn3c_branch2c'                Batch Normalization     Batch normalization with 512 channels
    68   'add_6'                        Addition                Element-wise addition of 2 inputs
    69   'activation_19_relu'           ReLU                    ReLU
    70   'res3d_branch2a'               Convolution             128 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    71   'bn3d_branch2a'                Batch Normalization     Batch normalization with 128 channels
    72   'activation_20_relu'           ReLU                    ReLU
    73   'res3d_branch2b'               Convolution             128 3x3x128 convolutions with stride [1  1] and padding 'same'
    74   'bn3d_branch2b'                Batch Normalization     Batch normalization with 128 channels
    75   'activation_21_relu'           ReLU                    ReLU
    76   'res3d_branch2c'               Convolution             512 1x1x128 convolutions with stride [1  1] and padding [0  0  0  0]
    77   'bn3d_branch2c'                Batch Normalization     Batch normalization with 512 channels
    78   'add_7'                        Addition                Element-wise addition of 2 inputs
    79   'activation_22_relu'           ReLU                    ReLU
    80   'res4a_branch2a'               Convolution             256 1x1x512 convolutions with stride [2  2] and padding [0  0  0  0]
    81   'bn4a_branch2a'                Batch Normalization     Batch normalization with 256 channels
    82   'activation_23_relu'           ReLU                    ReLU
    83   'res4a_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    84   'bn4a_branch2b'                Batch Normalization     Batch normalization with 256 channels
    85   'activation_24_relu'           ReLU                    ReLU
    86   'res4a_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    87   'res4a_branch1'                Convolution             1024 1x1x512 convolutions with stride [2  2] and padding [0  0  0  0]
    88   'bn4a_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    89   'bn4a_branch1'                 Batch Normalization     Batch normalization with 1024 channels
    90   'add_8'                        Addition                Element-wise addition of 2 inputs
    91   'activation_25_relu'           ReLU                    ReLU
    92   'res4b_branch2a'               Convolution             256 1x1x1024 convolutions with stride [1  1] and padding [0  0  0  0]
    93   'bn4b_branch2a'                Batch Normalization     Batch normalization with 256 channels
    94   'activation_26_relu'           ReLU                    ReLU
    95   'res4b_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    96   'bn4b_branch2b'                Batch Normalization     Batch normalization with 256 channels
    97   'activation_27_relu'           ReLU                    ReLU
    98   'res4b_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    99   'bn4b_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    100   'add_9'                        Addition                Element-wise addition of 2 inputs
    101   'activation_28_relu'           ReLU                    ReLU
    102   'res4c_branch2a'               Convolution             256 1x1x1024 convolutions with stride [1  1] and padding [0  0  0  0]
    103   'bn4c_branch2a'                Batch Normalization     Batch normalization with 256 channels
    104   'activation_29_relu'           ReLU                    ReLU
    105   'res4c_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    106   'bn4c_branch2b'                Batch Normalization     Batch normalization with 256 channels
    107   'activation_30_relu'           ReLU                    ReLU
    108   'res4c_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    109   'bn4c_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    110   'add_10'                       Addition                Element-wise addition of 2 inputs
    111   'activation_31_relu'           ReLU                    ReLU
    112   'res4d_branch2a'               Convolution             256 1x1x1024 convolutions with stride [1  1] and padding [0  0  0  0]
    113   'bn4d_branch2a'                Batch Normalization     Batch normalization with 256 channels
    114   'activation_32_relu'           ReLU                    ReLU
    115   'res4d_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    116   'bn4d_branch2b'                Batch Normalization     Batch normalization with 256 channels
    117   'activation_33_relu'           ReLU                    ReLU
    118   'res4d_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    119   'bn4d_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    120   'add_11'                       Addition                Element-wise addition of 2 inputs
    121   'activation_34_relu'           ReLU                    ReLU
    122   'res4e_branch2a'               Convolution             256 1x1x1024 convolutions with stride [1  1] and padding [0  0  0  0]
    123   'bn4e_branch2a'                Batch Normalization     Batch normalization with 256 channels
    124   'activation_35_relu'           ReLU                    ReLU
    125   'res4e_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    126   'bn4e_branch2b'                Batch Normalization     Batch normalization with 256 channels
    127   'activation_36_relu'           ReLU                    ReLU
    128   'res4e_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    129   'bn4e_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    130   'add_12'                       Addition                Element-wise addition of 2 inputs
    131   'activation_37_relu'           ReLU                    ReLU
    132   'res4f_branch2a'               Convolution             256 1x1x1024 convolutions with stride [1  1] and padding [0  0  0  0]
    133   'bn4f_branch2a'                Batch Normalization     Batch normalization with 256 channels
    134   'activation_38_relu'           ReLU                    ReLU
    135   'res4f_branch2b'               Convolution             256 3x3x256 convolutions with stride [1  1] and padding 'same'
    136   'bn4f_branch2b'                Batch Normalization     Batch normalization with 256 channels
    137   'activation_39_relu'           ReLU                    ReLU
    138   'res4f_branch2c'               Convolution             1024 1x1x256 convolutions with stride [1  1] and padding [0  0  0  0]
    139   'bn4f_branch2c'                Batch Normalization     Batch normalization with 1024 channels
    140   'add_13'                       Addition                Element-wise addition of 2 inputs
    141   'activation_40_relu'           ReLU                    ReLU
    142   'res5a_branch2a'               Convolution             512 1x1x1024 convolutions with stride [2  2] and padding [0  0  0  0]
    143   'bn5a_branch2a'                Batch Normalization     Batch normalization with 512 channels
    144   'activation_41_relu'           ReLU                    ReLU
    145   'res5a_branch2b'               Convolution             512 3x3x512 convolutions with stride [1  1] and padding 'same'
    146   'bn5a_branch2b'                Batch Normalization     Batch normalization with 512 channels
    147   'activation_42_relu'           ReLU                    ReLU
    148   'res5a_branch2c'               Convolution             2048 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    149   'res5a_branch1'                Convolution             2048 1x1x1024 convolutions with stride [2  2] and padding [0  0  0  0]
    150   'bn5a_branch2c'                Batch Normalization     Batch normalization with 2048 channels
    151   'bn5a_branch1'                 Batch Normalization     Batch normalization with 2048 channels
    152   'add_14'                       Addition                Element-wise addition of 2 inputs
    153   'activation_43_relu'           ReLU                    ReLU
    154   'res5b_branch2a'               Convolution             512 1x1x2048 convolutions with stride [1  1] and padding [0  0  0  0]
    155   'bn5b_branch2a'                Batch Normalization     Batch normalization with 512 channels
    156   'activation_44_relu'           ReLU                    ReLU
    157   'res5b_branch2b'               Convolution             512 3x3x512 convolutions with stride [1  1] and padding 'same'
    158   'bn5b_branch2b'                Batch Normalization     Batch normalization with 512 channels
    159   'activation_45_relu'           ReLU                    ReLU
    160   'res5b_branch2c'               Convolution             2048 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    161   'bn5b_branch2c'                Batch Normalization     Batch normalization with 2048 channels
    162   'add_15'                       Addition                Element-wise addition of 2 inputs
    163   'activation_46_relu'           ReLU                    ReLU
    164   'res5c_branch2a'               Convolution             512 1x1x2048 convolutions with stride [1  1] and padding [0  0  0  0]
    165   'bn5c_branch2a'                Batch Normalization     Batch normalization with 512 channels
    166   'activation_47_relu'           ReLU                    ReLU
    167   'res5c_branch2b'               Convolution             512 3x3x512 convolutions with stride [1  1] and padding 'same'
    168   'bn5c_branch2b'                Batch Normalization     Batch normalization with 512 channels
    169   'activation_48_relu'           ReLU                    ReLU
    170   'res5c_branch2c'               Convolution             2048 1x1x512 convolutions with stride [1  1] and padding [0  0  0  0]
    171   'bn5c_branch2c'                Batch Normalization     Batch normalization with 2048 channels
    172   'add_16'                       Addition                Element-wise addition of 2 inputs
    173   'activation_49_relu'           ReLU                    ReLU
    174   'avg_pool'                     Average Pooling         7x7 average pooling with stride [7  7] and padding [0  0  0  0]
    175   'fc1000'                       Fully Connected         1000 fully connected layer
    176   'fc1000_softmax'               Softmax                 softmax
    177   'ClassificationLayer_fc1000'   Classification Output   crossentropyex with 'tench' and 999 other classes
