## 人工神经网络的蓝本_人类视觉原理
* 1981年诺贝尔医学奖 , 颁发给了David Hubel(出生于加拿大的美国神经生物学家) 和TorstenWiesel，以及 Roger Sperry。
* 前述三人中前两位的主要贡献，是“发现了视觉系统的信息处理”，可视皮层是分级的 如下图所示。

![卷积神经网络原理](Pictures/theory%20of%20human's%20vision.jpg)

* 从图中可以看到 , 人类的视觉原理如下：
  从原始信号摄入开始(瞳孔摄入像素 Pixels) ,
  接着做初步处理(大脑皮层某些细胞发现边缘和方向) ,
  然后抽象(大脑判定，眼前的物体的局部特征) ,
  然后进一步抽象(依据前述特征 , 大脑进一步判定该物体到底是什么)
  
  更多的例子如下 :
  ![更多的例子](Pictures/more_examples.jpg)
  
  基本原理就是若干低级特征组成更高一级的特征 , 层层迭代 , 最后归纳为一个具体概念 .
  仿照人眼的这种识别流程 , 人们提出了人工神经网络这一仿生学设计概念 , 即构造多层的神经网络 , 低层的识别简单的样本特征 , 若干次级特征归纳出更高一级特征 , 层层迭代 , 最终在顶层作出分类 .
## CNN
1.  什么是CNN ?
    CNN = Convolutional Neural Network , 卷积神经网络
    在图像处理方面极具优势 , 特别是大图像的处理问题.
    最早由 *Yann LeCun* 提出并被用于手写字体识别上(也就是经典的MNIST训练集中的那些图片的识别) , 其提出的初代CNN被称之为LeNet(下图为其结构示意)
    ![LeNet](Pictures/LeNet_structure.jpg)
2.  卷积神经网络的结构
    卷积神经网络由 输入层 , 卷积层 , 激活函数 , 池化层 , 全连接层 组成 .
    *   卷积层  
        **用途 :** 卷积层用于进行特征提取
        ![卷积层特征提取示例](Pictures/convolution_layer.png)
        上图中 , 二维卷积中用的卷积层范围称为感受野(也就是图中标的filter<过滤器>) , 图中感受野大小为*5 * 5 * 3* , 原图大小为*32 * 32 * 3*;  
        **Note : 感受野的深度和图像的深度要相同**  
        **如本例中 , 原图是RGB三通道图像那么原图的矩阵深度就是3 , 那么感受野的最后一个大小参数也应该是3**   
        在卷积(convolute)之后 , 采样(sample)得到的图像(称feature map)大小为*28 * 28 * 1* ;
        而之后再对feature map 进行二次采样(subsample) , 之后如需要则继续卷积 , 循环往复至流程结束;  
        一般会设计多层卷积来获得高层次图像特征
        示例图如下
        ![多层卷积实例示例](Pictures/sample_multiConv.png)
        其原理如下图(*图中ReLU为一类激活函数 全称为 Rectified Linear Unit , 译名为线性整流函数*) :
        ![多层卷积原理示例](Pictures/theory_moticonv_1.png)


3.  使用CNN的原因
## 附录1 : 关于MNIST
MNIST = Mini National Institute of Standards and Technology 
NIST 是美国国家标准与技术研究所的简称 , MNIST 是该研究所提供的训练集的子集 , 其中训练集 (training set) 由 250 个不同人手写的数字构成, 其中 50% 是高中学生, 50% 来自人口普查局 (the Census Bureau) 的工作人员. 测试集(test set) 也是同样比例的手写数字数据.
关于如何得到该数据 , 可在如下链接查找.
[MNIST_download](http://yann.lecun.com/exdb/mnist/)
## 附录2 : 关于Fashion MNIST

## 附录3 : 关于二维卷积
将filter和输入图重合之后 , 对应位置相乘之后求加和 , 之后filter中心向右移动一定的步长(stride) , 重复上述流程 , 方向为左至右 , 上至下 , 直至图像右下角最后一组像素 , 就是二维卷积;
![二维卷积示例1](Pictures/theory_multiconv_2.png)
![二维卷积示例2](Pictures/theory_multiconv_3.png)
Note1 : 图中的卷积结果加上了偏移量(Bias);
Note2 : 图中的原图周围灰色部分是补充的边框(zero pad) , 是一个经验值 , 不一定是1 , 使用它是为了使得输入图像和输出图像具有相同的维度 , 如输入为5 * 5 * 3 , filter是3 * 3 * 3 , zero pad 为1 , 则输出图像为5 * 5 * 1 , 与输入图像具有相同的二维大小;
具体的运算方法如下 :
![zero_pad的使用方法](Pictures/zero_pad_method_of_application.png)
Note3 : 图2中的stride是2不是1;
## 参考资料
1.  [深度学习简介(一)——卷积神经网络](https://www.cnblogs.com/alexcai/p/5506806.html)
2.  [卷积神经网络_（1）卷积层和池化层学习](https://www.cnblogs.com/zf-blog/p/6075286.html)
3.  [详解 MNIST 数据集](https://blog.csdn.net/simple_the_best/article/details/75267863)
4.  [如何使用 Fashion MNIST 数据集](https://www.jianshu.com/p/2ed1707c610d)


