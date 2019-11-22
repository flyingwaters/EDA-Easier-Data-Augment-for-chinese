# EDA_用近义词替换句子中的词
 chinese EDA from<a href="https://arxiv.org/abs/1901.11196" target="_blank">《EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks》</a>的代码实现
 参考https://github.com/zhanlaoban/EDA_NLP_for_Chinese
 针对自己需求做如下修改，
 + 1.加入中文检测，之前发现替换结果中有非中文存在,
 + 2.改为替换近似最高和次高的词。
## 使用方法
```
修改if __name__ = "__main__": 下的open()路径，作为输入路径
修改其他的文件输出路径以及文件名字　修改synonyms[2] , 该模块为近义词查询模块，返回值为一个list = [ ],第一个为本身，近似度依次降低“２”选择近似度第二高的单词
作为替换词
```
# **命令行使用例子**
```
$ python EDA,py --alpha 0.1 --num_aug 9
分别为每句话替换单词的比例(--alpha)，以及生成增强的句子个数(--num_aug)
```
