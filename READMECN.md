[ENGLISH](/README.md)

# **主要功能介绍**

支持RINEX版本：
* [RINEX 2.xx 观测值文件 ](https://github.com/KenanZhu111/KNZ_Convert)(通过KNZ_Convert支持)
* RINEX 3.xx 观测值文件和广播星历 
* RINEX 4.xx 观测值文件 

支持GNSS：
* GPS：卫星位置解算&接收机定位
* Galileo：卫星位置解算&接收机定位
* GLONASS：卫星位置解算
* 北斗/Compass：卫星位置解算

支持定位方式
* 伪距定位
* (OINP)

特色功能：
* 实现卫星轨道3D显示

# 主要介绍
## 程序介绍
### 关于KNZ_GeoTrackLab
* 2024年10月24日新增，由KNZ_Calculate与KNZ_Plot合并而成，改进运算逻辑，优化界面显示。
* 阅读更多帮助文档
### 关于 KNZ_Calculate（停止）（与 KNZ_Plot 合并）
* 自 2024 年 10 月 24 日起，KNZ_Calculate 已与 KNZ_Plot 合并为 KNZ_GeoTrackLab。[ADIN 2024/10/26]
### 关于 KNZ_Plot（停止）（与 KNZ_Calculate 合并）
* 自 2024 年 10 月 5 日起，KNZ_Calculate 已与 KNZ_Plot 合并为 KNZ_GeoTrackLab。[ADIN 2024/10/26]
### 关于 PyGMT（停止）
* 自 2024 年 10 月 5 日起，PyGMT 项目将不再考虑。[ADIN 2024/10/5]
### 关于 Matlab（停止）
* 自 2024 年 10 月 5 日起，Matlab 项目将不再已考虑。[ADIN 2024/10/5]

## 项目更新

### 重大更新：2024/10/26
1. 完全的GUI界面
2. 合并 KNZ_Calculate 和 KNZ_Plot。
3. 合并后将项目重命名为 KNZ_GeoTrackLab。
4. 支持 GPS、北斗、Galileo、GLONASS 卫星位置计算。
5. 增加新模块：3D 卫星轨道显示。

### 更新：2024/10/14
1. KNZ_Calculate：支持 GPS、BDS、Galileo 卫星位置计算。
2. KNZ_Plot：支持 GPS 和 Galileo 单点定位。

### 更新：2024/10/09
1. KNZ_Calculate：修改了一些错误并优化了使用体验。
2. KNZ_Plot：更多选择性选项和更统一的 GUI 风格。

### 重命名项目：2024/10/08
1. 更新 KNZ_Plot。
2. 更新更多 GUI 部分。

### 更新：2024/10/06
1. SPP_Plot：实现文件查看功能。
2. SPP_Plot：实现颜色选择 优化操作体验。

### 大更新：2024/10/05
1. 实现完整的 GUI 程序。
2. 完成绘图功能。

### 更新：2024/09/28
1. 通过 WIN32 API 实现 GUI。
2. 优化代码结构。

### 更新：2024/09/26
1. 修复一些 bug。
2. 优化代码结构。

### 更新：2024/09/23
1. 修改一些崩溃。
2. 修复一些 bug。

### 更新：2024/09/22
1. 修改UI。
2. 修复一些bug。

### 大更新：2024/09/21
1. 修正一些错误。
2. 优化代码结构。
3. 完善软件输入输出功能和操作逻辑。
4. 增加和修改多个实用函数的头文件：
-blh2enu.h
-xyz2blh.h
-rahcal.h
-deg2dms.h
-degRrad.h

### 更新：2024/09/20
1. 修正一些错误。
2. 优化代码结构。

## 项目公告
* 编写代码时，借助了已有的开源代码成果，并不同程度的参考，在此一一标注并表示感谢：

| *https://blog.csdn.net/why1472587?type=blog*
| *https://zhuanlan.zhihu.com/p/416072448*
| *https://www.pygmt.org/latest/index.html*
| *https://blog.csdn.net/FrankXCR/article/details/135438701*

### 文档标签说明
* [ADIN TIME]: 新增于“TIME”(如 [ADIN 2024/9/22]: 新增于 2024/9/22)。
* (OINP)：正在进行中的更改，或急需改进的部分。
* (STOP)：不再更新维护或考虑实现功能。

#### *本程序代码仅供学习交流使用* ####
