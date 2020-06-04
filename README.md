# Dijkstra_travel_path
﻿这是网络优化课程最后的课程报告，利用Dijkstra算法对已知节点进行最短路径规划。
开发环境：

 - ubuntu16 
 - python3.6——pyqt5、opencv-pyhton、urllib、requests

首先，进入[高德地图开放平台](https://lbs.amap.com)，创建应用。选用的是高德地图开发平台的web服务API，可使用的服务如图一，而本文
          需要静态地图API进行地图图片的显示、搜索服务-关键字查询进行地点坐标（经纬度）的查询、行驶距离测量进行两地点驾车距离的运算。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604172531104.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)然后进行计算图的Dijkstra算法应用，最后进行可视化。增加了TSP问题利用GA算法的实现，直接采用[大神](https://blog.csdn.net/luolang_103/article/details/79839849)的代码。

***实现流程图：***
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604173052355.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)

***实现结果：***
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604173120142.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70)![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604173203613.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)![在这里插入图片描述](https://img-blog.csdnimg.cn/2020060417321498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604173227806.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)![在这里插入图片描述](https://img-blog.csdnimg.cn/20200604173239222.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzMyNzY4Njc5,size_16,color_FFFFFF,t_70#pic_center)


感谢[github-dijkstra最短路径规划](https://github.com/zz54165514/dijkstra)提供的最短路径规划案例分享；
感谢[TSP-GA](https://github.com/Greatpanc/-TSP2-)的TSP-GA遗传算法的实现;
本文代码[链接](https://github.com/Youjiangbaba/Dijkstra_travel_path)。
