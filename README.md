[ENGLISH](READMEEN.md)

> [!WARNING]
> 你正在浏览已经被遗弃的仓库 !
> 我们将不再对该项目进行更新。

# **主要功能介绍**

支持RINEX版本：
* [RINEX 2.xx 观测值文件 ](https://github.com/KenanZhu111/KNZ_Convert)(通过KNZ_Convert支持)
* RINEX 3.xx 观测值文件和广播星历 
* RINEX 4.xx 观测值文件 

支持GNSS：
* GPS：卫星位置解算&接收机定位
* Galileo：卫星位置解算&接收机定位
* GLONASS：卫星位置解算(OINP)
* 北斗/Compass：卫星位置解算(OINP)

支持定位方式
* 伪距定位
* (OINP)

# 主要介绍
## 程序介绍
### 关于KNZ_GeoTrackLab
* 2024年10月24日新增，由KNZ_Calculate与KNZ_Plot合并而成，改进运算逻辑，优化界面显示。
* 阅读帮助文档了解更多
### 关于 KNZ_Calculate（停止）（与 KNZ_Plot 合并）
* 自 2024 年 10 月 24 日起，KNZ_Calculate 已与 KNZ_Plot 合并为 KNZ_GeoTrackLab。[ADIN 2024/10/26]
### 关于 KNZ_Plot（停止）（与 KNZ_Calculate 合并）
* 自 2024 年 10 月 24 日起，KNZ_Calculate 已与 KNZ_Plot 合并为 KNZ_GeoTrackLab。[ADIN 2024/10/26]
### 关于 PyGMT（停止）
* 自 2024 年 10 月 5 日起，PyGMT 项目将不再考虑。[ADIN 2024/10/5]
### 关于 Matlab（停止）
* 自 2024 年 10 月 5 日起，Matlab 项目将不再考虑。[ADIN 2024/10/5]

## 项目更新
更新：2024/11/08:
1. KNZ_GeoTrackLab: 修复一些bug。

更新：2024/11/05:
1. KNZ_GeoTrackLab: 修复一些bug, 优化UI逻辑。
2. KNZ_GeoTrackLab: 为View文本编辑器增添保存修改功能。
3. KNZ_GeoTrackLab: 卫星轨迹投影图更改为墨卡托投影，
                    并实现动画显示，卫星号选择，绘
                    制采样频率选择。

更新: 2024/10/31:
1. KNZ_GeoTrackLab: 修复一些bug, 优化UI逻辑。
2. KNZ_GeoTrackLab: 移除3D绘图功能。
2. KNZ_GeoTrackLab: 合并功能并专一化。
3. KNZ_GeoTrackLab: 新增: 
                        卫星轨迹投影图。

更新: 2024/10/31:
1. KNZ_GeoTrackLab: 修复一些bug, 优化UI逻辑.
2. KNZ_GeoTrackLab: 优化代码结构.
3. KNZ_GeoTrackLab: 新增: 
                        截止高度角选项。

更新：2024/10/28
1. KNZ_GeoTrackLab：修复一些bug。
2. KNZ_GeoTrackLab：优化代码结构。

重命名项目并更新：2024/10/26
1. 首次发布 KNZ_GeoTrackLab。
2. KNZ_Calculate：与 KNZ_Plot 合并。
3. KNZ_Plot：与 KNZ_Calculate 合并。
4. KNZ_GeoTrackLab：支持 GPS、北斗、伽利略和 GLONASS。

更新：2024/10/14
1. KNZ_Calculate：支持 GPS、BDS 和伽利略。
2. KNZ_Plot：支持 GPS 和伽利略。

更新：2024/10/09
1. KNZ_Calculate：修改一些崩溃。
2. KNZ_Calculate：优化使用体验。
3. KNZ_Plot：修改 UI。

重命名项目并更新：2024/10/08
1. 首次发布 KNZ_Plot、KNZ_Calculate。
2. KNZ_Plot：修改 UI。
3. KNZ_Calculate：修改 UI。

更新：2024/10/06
1. SPP_Plot：修复一些bug。
2. SPP_Plot：优化使用体验。
3. SPP_Calculate：优化代码结构。
4. SPP_Calculate：修改UI。

更新：2024/10/05
1. 首次发布SPP_Plot
2. SPP_Calculate：修改UI。

更新：2024/09/28
1. 首次发布SPP_Calculate。
2. 优化代码结构。

更新：2024/09/26
1. 修复一些bug。
2. 优化使用体验。

更新：2024/09/23
1. 修复一些bug。
2. 修改一些崩溃。

更新：2024/09/22
1. 修复一些bug。
2. 修改UI。

更新：2024/09/21
1. 修复一些bug。
2. 优化使用体验。

更新：2024/09/20
1. 首次发布。

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

> [!NOTE]
> 你可以对该代码核心功能和界面部分进行二次开发
> 无需额外授权。我们对此不保留任何权利。