环境配置
------------------
pytorch 1.8.0 
torchvision 0.9.0
torchaudio 0.8.0
（其他的文件库适配即可）


文件结构
-------------------
model
	-resnet50_3_64_751.pt：模型为resnet50，输入大小为3*64*751的tensor
	-Gmv3_3_64_751.pt：模型为Gmv3，输入大小为3*64*751的tensor

main.py 主函数 ： 使用BSR函数测试鸟鸣音频文件，得到结果

predata.py ：加载音频文件，处理为3*64*751的梅尔频谱图

utils.py：音频处理的工具函数包

class_indices.json: 类别id转换文件
--------------------
以上文件即可完成整体预测鸟鸣功能，以下文件函模型定义
model.py：含有具体模型定义，resnet50为pytorch内置，可达66%准确率
Gmv3是论文《Design_of_Bird_Sound_Recognition_Model_Based_on_Lightweight》的模型复现