#!/user/bin/python3
# -*-coding:utf-8 -*-

"""
# File       : model.py
# Time       ：2023/1/1 16:27
# Author     ：Kermit Li
# version    ：python 3.9
# Description：
"""
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F


class resnet50(nn.Module):
    def __init__(self, num_classes, **kwargs):
        self.features = torchvision.models.resnet50(num_classes=num_classes)


class mish(nn.Module):
    def forward(self, x):
        out = x * torch.tanh(torch.log(1 + torch.exp(x)))
        return out


class hswish(nn.Module):
    def forward(self, x):
        out = x * F.relu6(x + 3, inplace=True) / 6
        return out


class hsigmoid(nn.Module):
    def forward(self, x):
        out = F.relu6(x + 3, inplace=True) / 6
        return out


class BasicConv2d(nn.Module):
    def __init__(self, in_channel, out_channel, **kwargs):
        super(BasicConv2d, self).__init__()
        self.convrelu = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, **kwargs),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.convrelu(x)
        return x


class SeModule(nn.Module):
    def __init__(self, in_channel, reduction=4):
        super(SeModule, self).__init__()
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            BasicConv2d(in_channel, in_channel // reduction, kernel_size=1, stride=1, padding=0, bias=False),
            nn.Conv2d(in_channel // reduction, in_channel, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(in_channel),
            hsigmoid()
        )

    def forward(self, x):
        return x * self.se(x)


class Block(nn.Module):
    def __init__(self, kernel_size, in_channel, expand_size, out_channel, nolinear, semodule, stride):
        super(Block, self).__init__()
        self.stride = stride
        self.se = semodule
        # 1*1展开卷积
        self.conv1 = nn.Conv2d(in_channel, expand_size, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(expand_size)
        self.nolinear1 = nolinear
        # 3*3（或5*5）深度可分离卷积
        self.conv2 = nn.Conv2d(expand_size, expand_size, kernel_size=kernel_size, stride=stride,
                               padding=kernel_size // 2, groups=expand_size, bias=False)
        self.bn2 = nn.BatchNorm2d(expand_size)
        self.nolinear2 = nolinear
        # 1*1投影卷积
        self.conv3 = nn.Conv2d(expand_size, out_channel, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channel)

        self.shortcut = nn.Sequential()
        if stride == 1 and in_channel != out_channel:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channel, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channel),
            )

    def forward(self, x):
        out = self.nolinear1(self.bn1(self.conv1(x)))
        out = self.nolinear2(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        # 注意力模块
        if self.se != None:
            out = self.se(out)
        # 残差链接
        out = out + self.shortcut(x) if self.stride == 1 else out
        return out


class SEWeightModule(nn.Module):

    def __init__(self, channels, reduction=16):
        super(SEWeightModule, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc1 = nn.Conv2d(channels, channels // reduction, kernel_size=1, padding=0)
        self.relu = nn.ReLU(inplace=True)
        self.fc2 = nn.Conv2d(channels // reduction, channels, kernel_size=1, padding=0)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.avg_pool(x)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        weight = self.sigmoid(out)

        return weight


def conv(in_planes, out_planes, kernel_size=3, stride=1, padding=1, dilation=1, groups=1):
    """standard convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=kernel_size, stride=stride,
                     padding=padding, dilation=dilation, groups=groups, bias=False)


class PSAModule(nn.Module):

    def __init__(self, inplans, planes, conv_kernels=[3, 5, 7, 9], stride=1, conv_groups=[1, 4, 8, 16]):
        super(PSAModule, self).__init__()
        self.conv_1 = conv(inplans, planes // 4, kernel_size=conv_kernels[0], padding=conv_kernels[0] // 2,
                           stride=stride, groups=conv_groups[0])
        self.conv_2 = conv(inplans, planes // 4, kernel_size=conv_kernels[1], padding=conv_kernels[1] // 2,
                           stride=stride, groups=conv_groups[1])
        self.conv_3 = conv(inplans, planes // 4, kernel_size=conv_kernels[2], padding=conv_kernels[2] // 2,
                           stride=stride, groups=conv_groups[2])
        self.conv_4 = conv(inplans, planes // 4, kernel_size=conv_kernels[3], padding=conv_kernels[3] // 2,
                           stride=stride, groups=conv_groups[3])
        self.se = SEWeightModule(planes // 4)
        self.split_channel = planes // 4
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        batch_size = x.shape[0]
        x1 = self.conv_1(x)
        x2 = self.conv_2(x)
        x3 = self.conv_3(x)
        x4 = self.conv_4(x)

        feats = torch.cat((x1, x2, x3, x4), dim=1)
        feats = feats.view(batch_size, 4, self.split_channel, feats.shape[2], feats.shape[3])

        x1_se = self.se(x1)
        x2_se = self.se(x2)
        x3_se = self.se(x3)
        x4_se = self.se(x4)

        x_se = torch.cat((x1_se, x2_se, x3_se, x4_se), dim=1)
        attention_vectors = x_se.view(batch_size, 4, self.split_channel, 1, 1)
        attention_vectors = self.softmax(attention_vectors)
        feats_weight = feats * attention_vectors
        for i in range(4):
            x_se_weight_fp = feats_weight[:, i, :, :]
            if i == 0:
                out = x_se_weight_fp
            else:
                out = torch.cat((x_se_weight_fp, out), 1)

        return out


class Inception(nn.Module):
    def __init__(self, in_channel, ch1x1, ch3x3red, ch3x3, ch5x5red, ch5x5, pool_proj):
        super(Inception, self).__init__()

        self.branch1 = BasicConv2d(in_channel, ch1x1, kernel_size=1)

        self.branch2 = nn.Sequential(
            BasicConv2d(in_channel, ch3x3red, kernel_size=1),
            BasicConv2d(ch3x3red, ch3x3, kernel_size=3, padding=1)
        )

        self.branch3 = nn.Sequential(
            BasicConv2d(in_channel, ch5x5red, kernel_size=1),
            BasicConv2d(ch5x5red, ch5x5, kernel_size=5, padding=2)
        )

        self.branch4 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            BasicConv2d(in_channel, pool_proj, kernel_size=1)
        )

    def forward(self, x):
        branch1 = self.branch1(x)
        branch2 = self.branch2(x)
        branch3 = self.branch3(x)
        branch4 = self.branch4(x)

        outputs = [branch1, branch2, branch3, branch4]
        return torch.cat(outputs, 1)


class PSAInception(nn.Module):
    def __init__(self, in_channel, out_channel, ch3x3, ch5x5):
        super(PSAInception, self).__init__()

        self.branch1 = nn.Sequential(
            BasicConv2d(in_channel, ch3x3, kernel_size=3, stride=2, padding=1),
            PSAModule(ch3x3, ch3x3),
            BasicConv2d(ch3x3, out_channel, kernel_size=1)
        )
        self.branch2 = nn.Sequential(
            BasicConv2d(in_channel, ch5x5, kernel_size=5, stride=2, padding=2),
            PSAModule(ch5x5, ch5x5),
            BasicConv2d(ch5x5, out_channel, kernel_size=1)
        )

    def forward(self, x):
        b1 = self.branch1(x)
        b2 = self.branch1(x)
        outputs = [b1, b2]
        return torch.cat(outputs, 1)


class GMv3(nn.Module):
    def __init__(self, num_classes=1000):
        super(GMv3, self).__init__()

        self.Inception = PSAInception(3, 32, 64, 64)
        self.Bneck = nn.Sequential(
            Block(3, 64, 64, 32, nn.ReLU(inplace=True), SeModule(32), 1),
            Block(3, 32, 64, 32, nn.ReLU(inplace=True), SeModule(32), 1),
            Block(3, 32, 72, 16, mish(), None, 1),
            Block(3, 16, 72, 24, mish(), None, 2),
            Block(3, 24, 96, 32, hswish(), None, 2),
            Block(3, 32, 120, 64, hswish(), None, 1),
            Block(3, 64, 288, 96, hswish(), SeModule(96), 2),
            Block(3, 96, 576, 160, hswish(), SeModule(160), 2),
            Block(3, 160, 576, 320, hswish(), None, 1)
        )
        self.conv1 = BasicConv2d(320, 1280, kernel_size=1)
        self.avgp = nn.AdaptiveAvgPool2d(1)
        self.conv2 = BasicConv2d(1280, num_classes, kernel_size=1)

    def forward(self, x):
        out = self.Inception(x)
        out = self.Bneck(out)
        out = self.conv2(self.avgp(self.conv1(out)))
        out = torch.flatten(out, start_dim=1)
        return out