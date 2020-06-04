#coding=utf-8
import requests
import re
import cv2
import numpy as np

import webbrowser

import urllib.request

import sys

# URL到图片
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    # bytearray将数据转换成（返回）一个新的字节数组
    # asarray 复制数据，将结构化数据转换成ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode()函数将数据解码成Opencv图像格式
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image


# dijkstra算法实现，有向图和路由的源点作为函数的输入，最短路径最为输出
def dijkstra(graph, src):
    # 判断图是否为空，如果为空直接退出
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]  # 获取图中的所有节点
    visited = []   # 表示已经路由到最短路径的节点集合
    if src in nodes:  # 如果该节点未被标记
        visited.append(src)  # 标记该节点
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}  # 记录源节点到各个节点的距离
    for i in nodes:
        distance[i] = graph[src][i]  # 初始化
    path = {src: {src: []}}  # 记录源节点到每个节点的路径
    print(path, distance)
    k = pre = src
    while nodes:
        mid_distance = float('inf')
        for v in visited:
            for d in nodes:
                new_distance = graph[src][v]+graph[v][d]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    graph[src][d] = new_distance  # 进行距离更新
                    k = d
                    pre = v
        distance[k] = mid_distance  # 最短路径
        path[src][k] = [i for i in path[src][pre]]
        path[src][k].append(k)
        # 更新两个节点集合
        visited.append(k)
        nodes.remove(k)
        print(visited, nodes)  # 输出节点的添加过程
    return distance, path


def path_planning(list_place,main_location = '成都',zoom_ = 12):
    if main_location =='北京':
        zoom_ = 11
    elif main_location == '成都':
        zoom_ = 11
    print (main_location,zoom_)
    len_place = len(list_place)
    x = len_place
    #两个list转字典
    a = {}
    for i in range(len_place):
        a[i+1]=list_place[i]
    # a = {1:'火车东站',2:'宽窄巷子',3:'春熙路',4:'武侯祠',5:'天府广场',6:'金沙博物馆'}

    # 创建字典存储点位信息
    graph_list = []
    # 创建列表存储距离/时间信息
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}


    print(a,list_place)

    locations_place = []#存放地点坐标
    for i in range(1, x+1):
        list = []  # 列表存储中间的距离/时间
        url1 = "http://restapi.amap.com/v3/place/text?key=0cab33b62a6308e0ba486f1cddc3195e&keywords=" + a[i] \
            + "&types=&city=%s&children=1&offset=1&page=1&extensions=all"%main_location
        data1 = requests.get(url1, headers=head)
        data1.encoding = 'utf-8'
        data1 = data1.text
        pat1 = 'location":"(.*?),(.*?)",".*?ddress'
        result1 = re.findall(pat1, data1)
        locations_place.append((str(result1[0][0]) ,str(result1[0][1])))
        
        for m in range(1, x+1):

            url2 = "http://restapi.amap.com/v3/place/text?key=0cab33b62a6308e0ba486f1cddc3195e&keywords=" + a[m]\
                + "&types=&city=%s&children=1&offset=1&page=1&extensions=all"%locations_place
            data2 = requests.get(url2, headers=head)
            data2.encoding = 'utf-8'
            data2 = data2.text
            result2 = re.findall(pat1, data2)

            url3 = "http://restapi.amap.com/v3/distance?key=0cab33b62a6308e0ba486f1cddc3195e&origins=" +\
                str(result1[0][0]) + "," + str(result1[0][1]) + "&destination=" + str(result2[0][0]) + "," +\
                str(result2[0][1])+"&type=1"
            # print(url3)
            data3 = requests.get(url3, headers=head)
            data3.encoding = 'utf-8'
            data3 = data3.text
            # print(data3)
            pat2 = "distance\":\"(.*?)\",\"duration\":\"(.*?)\""
            result3 = re.findall(pat2, data3)

            #print(result1,'\n',result2,'\n',result3)
            
            # 获得两个节点的距离/时间信息
            list.append(int(result3[0][0]))

        graph_list.append(list)
        #print(graph_list)
        # 将所有的距离/时间信息存储到列表中

    distance, path = dijkstra(graph_list, 0)  # 查找从源点0开始带其他节点的最短路径
    print(distance, path)  # 输出最短距离和行驶路线


    #result_places 路径顺序排列
    result_loctions = []
    result_places = []
    time = 0
    print("最终路径：")  # 输出最优的路线内容
    for key in path[0]:
        result_loctions.append(locations_place[list_place.index(str(a[key+1])) ])
        result_places.append(a[key+1])
        print(a[key+1], str(locations_place[key]))
        time += 1
        if time < x:
            print("到", ' ')
    print(locations_place)
    print(result_places)




    #请求静态地图

    # https://restapi.amap.com/v3/staticmap?location=116.48482,39.94858&zoom=10&size=400*400&labels=朝阳公园,2,0,16,0xFFFFFF,0x008000:116.48482,39.94858&key=您的key 
    # https://restapi.amap.com/v3/staticmap?zoom=15&size=500*500&paths=10,0x0000ff,1,,:116.31604,39.96491;116.320816,39.966606;116.321785,39.966827;116.32361,39.966957&key
    location = str("0,0")#中心坐标
    zoom = str(zoom_)#缩放等级 1,17
    labels = "%s,2,0,16,0xFFFFFF,0x008000:%s"%("start_place",str(locations_place[0][0]+','+locations_place[0][1]))
    # for i,pl in enumerate(locations_place):
    #     labels += "%s,2,0,16,0xFFFFFF,0x008000:%s;"%(list_place[i+1],str(locations_place[i+1][0]+','+locations_place[i+1][1]))
    # labels = labels[:-1]

    markers = 'mid,0xFF0000,A:' #标注点，最多十个
    for pl in locations_place:
        markers += str(pl[0]+','+pl[1])
        markers += ';'
    markers = markers[:-1]

    #绘制折线
    paths = '3,0x0000ff,1,,:'
    for pl in result_loctions:
        paths += str(pl[0]+','+pl[1])
        paths += ';'
    paths = paths[:-1]

    parameters = 'key=0cab33b62a6308e0ba486f1cddc3195e&zoom=%s&size=800*800&markers=%s&labels=%s&paths=%s'%(zoom,markers,labels,paths)
    map_url = 'https://restapi.amap.com/v3/staticmap?'+parameters
    print (map_url)
    png = url_to_image(map_url)
    # cv2.imshow('map',png)
    # cv2.waitKey(0)
    return png,result_places

if __name__ == "__main__":
    a = ["宽窄巷子","火车南站","金沙博物馆","天府广场"]
    path_planning(a)
