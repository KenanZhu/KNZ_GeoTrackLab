[中文](/READMECN.md)

# **MAIN FUNCTION INTRODUCTION**

Support version of RINEX:
* [RINEX of Observation of version 2.xx.](https://github.com/KenanZhu111/KNZ_Convert)(Support by KNZ_Convert)
* RINEX of Observation & Navigation of version 3.xx.
* RINEX of Observation of version 4.xx.
  
Support system of GNSS:
* GPS: Satellite position solving & Receiver station orientation
* Galileo : Satellite position solving & Receiver station orientation
* GLONASS : Satellite position solving
* BeiDou / Compass : Satellite position solving

Support method of orientation
* Pseudorange positioning
* (OINP)

Features ：
* Realize 3D display of satellite orbit

# MAIN INTRO
## Program intro
  ### About KNZ_GeoTrackLab
  * Added on October 24, 2024, merged from KNZ_Calculate and KNZ_Plot, improved operation logic, optimized interface display.
  * Read more on help.doc
  ### About KNZ_Calculate(STOP)(Merge with KNZ_Plot )
  * As of October 24, 2024, KNZ_Calculate has been merged with KNZ_Plot to form KNZ_GeoTrackLab.[ADIN 2024/10/26]
  ### About KNZ_Plot(STOP)(Merge with KNZ_Calculate )
  * As of October 5, 2024, KNZ_Calculate has been merged with KNZ_Plot to form KNZ_GeoTrackLab.[ADIN 2024/10/26]
  ### About PyGMT(STOP)
  * As of October 5, 2024, PyGMT plot project will no longer be considered.[ADIN 2024/10/5]    
  ### About Matlab(STOP)
  * As of October 5, 2024, Matlab project will no longer be considered.[ADIN 2024/10/5] 
  
## Project Update

#### Big Update: 2024/10/26
1. Full gui
2. Integrated KNZ_Calculate and KNZ_Plot.
3. Rename the project as GeoTrackLab after the integrate.
4. Realized GPS, BeiDou, Galileo, GLONASS satellite position calculation.
5. New module added: 3D satellite orbit display.

#### Update: 2024/10/14
1. KNZ_Calculate: be able to calculate the sat pos of GPS & BDS & Galileo.
2. KNZ_Plot: be able to Single postiting by GPS & Galileo.

#### Update: 2024/10/09
1. KNZ_Calculate: modified some mistake and optimize the use experience.
2. KNZ_Plot: more selective options and more united style of GUI.

#### Rename the Project: 2024/10/08
1. Update KNZ_Plot.
2. Update more GUI parts.

#### Update: 2024/10/06
1. SPP_Plot: Realize the file view function.
2. SPP_Plot: Realize the color select Optimized operation experience.

#### Big Update: 2024/10/05
1. Realize the full gui program.
2. Complete the plot function.

#### Update: 2024/09/28
1. Implement GUI by WIN32 API.
2. Optimize code structure.

#### Update: 2024/09/26
1. Fix some bug.
2. Optimize code structure.

#### Update: 2024/09/23
1. Modify some crash.
2. Fix some bug.

#### Update: 2024/09/22
1. Modify UI.
2. Fix some bug.

#### Big Update: 2024/09/21
1. Correct some mistake.
2. Optimize code structure.
3. Improve the function and operation logic of software input and output.
4. Adding and modify many useful function in their header file:
-blh2enu.h
-xyz2blh.h
-rahcal.h
-deg2dms.h
-degRrad.h

#### Update: 2024/09/20
1. Correct some mistake.
2. Optimize code structure.

## Project notice
* When writing the code, with the help of the existing open source code results, and different degrees of reference, here one by one mark and express thanks:  

| *https://blog.csdn.net/why1472587?type=blog*   
| *https://zhuanlan.zhihu.com/p/416072448*                   
| *https://www.pygmt.org/latest/index.html*                  
| *https://blog.csdn.net/FrankXCR/article/details/135438701*

###  Document label specification
* [ADIN TIME]: new added in "TIME"(e.g. [ADIN 2024/9/22]: new added in 2024/9/22).
* (OINP): Operation in progress, or in urgent need of improvement.
* (STOP): No longer update maintenance or consider implementing features.
  
#### *This program code is solely for study and communication purposes* ####
