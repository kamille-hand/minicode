# coding : utf-8
import os
import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms, models


class myGradCAM:
    # 加载vgg19模型
    model = models.vgg19()
    # 加载预训练模型数据
    model.load_state_dict(torch.load("DL/models/vgg19.pth"))
    # 测试模式，禁用dropout，保证每次输出为定值
    model.eval()
    # CNN模型输入归一化
    preprocess = transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
    
    # layerNames:目标特征层的名字
    def __init__(self, layerNames=["36"], cudaDevice=0):
        # 设定gpu_id
        self.device = torch.device(cudaDevice)
        # 模型移至gpu
        self.model.cuda(self.device)
        # 存放目标层的输出
        self.targetFeature = []
        # 存放目标层的梯度
        self.targetGradient = []
        # 存放目标层的类激活图结果
        self.classActivationMap = []
        # 获取目标层对象
        self.targetLayers = [ 
            layer for index, layer in self.model.features._modules.items() 
            if index in layerNames
        ]
        # 设置前向、后向hook函数，分别获取目标层输出和梯度
        for targetLayer in self.targetLayers:
            targetLayer.register_forward_hook(self.saveFeature)
            targetLayer.register_backward_hook(self.saveGradient) 

    # imgTensor为载入的图像张量
    def __call__(self, imgTensor):
        # 前向传播，触发前向hook
        res = self.model(self.preprocess(imgTensor).unsqueeze(dim=0).cuda(self.device))
        # 获取预测值和类别
        val, idx = torch.max(res,dim=1,keepdim=True)
        # 清除梯度
        self.model.zero_grad()
        # 反向传播，触发后向hook
        val.backward()
        # 生成类激活图
        self.generateActivationMap()

    def saveFeature(self, model, ins, outs):
        self.targetFeature.append(outs)

    def saveGradient(self, model, ins, outs):
        self.targetGradient.append(outs[0])

    def generateActivationMap(self):
        # 禁用自动求导
        with torch.no_grad():
            for i in range(len(self.targetFeature)):
                # Global Average Pooling
                alpha = self.targetGradient[-1-i].mean(dim=(2,3), keepdim=True)
                '''
                print(self.targetFeature[i].size(), 
                      self.targetGradient[i].size(), 
                      alpha.size())
                '''
                # 按位置加权和
                linearCombination = (alpha * self.targetFeature[i]).sum(dim=1)
                # ReLU
                linearCombination = (linearCombination > 0) * linearCombination
                # 以numpy数组形式存放类激活图
                self.classActivationMap.append(linearCombination.cpu().squeeze().numpy())

    # 加载图片函数
    @staticmethod
    def loadImg(imgPath):
        tf = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop((224,224)),
            transforms.ToTensor(),
        ])
        img = Image.open(imgPath)
        return tf(img)
    
    # 生成热力图
    @staticmethod
    def fuseImg(img, mask):
        mask = cv2.resize(mask, img.size()[1:])
        mask /= np.max(mask)
        heatmap = cv2.applyColorMap(np.uint8(255*mask), cv2.COLORMAP_JET)
        heatmap = np.float32(heatmap)/255 + img.permute(1,2,0).cpu().detach().numpy()
        heatmap /= np.max(heatmap)
        return np.uint8(255*heatmap)


if __name__ == "__main__":
    os.chdir("/home/usslab/zwj")
    cam = myGradCAM(layerNames=["16","26","36"])
    img = myGradCAM.loadImg("DL/000370.jpg")
    cam(img)
    result = myGradCAM.fuseImg(img, cam.classActivationMap[0])
    cv2.imwrite("myGradCAM_16.jpg", result)
    result = myGradCAM.fuseImg(img, cam.classActivationMap[1])
    cv2.imwrite("myGradCAM_26.jpg", result)
    result = myGradCAM.fuseImg(img, cam.classActivationMap[2])
    cv2.imwrite("myGradCAM_36.jpg", result)
