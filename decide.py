import numpy as np


def load_dict(path:str):
    # # Load
    number_coordinates_dict = np.load(path, allow_pickle=True).item()

    # load_dict2 = load_dict
    # print(load_dict2, type(load_dict2), len(load_dict2))

    # for number, coordinates in number_coordinates_dict.items():
    #     print(number)
    #     print(coordinates)
    #     break
    
    return number_coordinates_dict

def load_txt(jingdu_path:str, weidu_path:str):
    """加载经度txt文件和纬度txt文件, 将他们对应起来转化为列表返回[[经度, 纬度], [经度, 纬度]]"""

    jingdu_weidu_list = []

    with open(jingdu_path, mode="r") as file1:
        jingdu_list = file1.readlines()
        for index, number in enumerate(jingdu_list):
            jingdu_list[index] = jingdu_list[index].replace("\n", "")

    with open(weidu_path, mode="r") as file2:
        weidu_list = file2.readlines()
        for index, number in enumerate(weidu_list):
            weidu_list[index] = weidu_list[index].replace("\n", "")

    for i in range(0, len(jingdu_list)):
        jingweidu = [jingdu_list[i], weidu_list[i]]
        jingdu_weidu_list.append(jingweidu)

    return jingdu_weidu_list


def is_in_poly(p, poly):
    """
    点是否落在多边形内
    :param p: [x, y]
    :param poly: [[], [], [], [], ...]
    :return:
    """
    px, py = p

    # 转为浮点型
    px = float(px)
    py = float(py)

    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner        
        x2, y2 = poly[next_i]

        # 转为浮点型
        x1, y1 = float(x1), float(y1)
        x2, y2 = float(x2), float(y2)

        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # find horizontal edges of polygon
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = not is_in
    return is_in
 
 
if __name__ == '__main__':
    # point = [3, 3]
    # poly = [[0, 0], [7, 3], [8, 8], [5, 5]]
    # print(is_in_poly(point, poly))

    xuhao_dikuaibianma = dict()

    jingdu_weidu_list= load_txt(jingdu_path="jingdu.txt", weidu_path="weidu.txt")

    sums = 0

    for index, jingweidu in enumerate(jingdu_weidu_list):
        # 遍历问题点
        for i in range(0, 20):
            # 遍历20个切片文件
            number_coordinates_dict = load_dict(path=f"number_coordinates_dict_{i}.npy")            
            for number, coordinates in number_coordinates_dict.items():
                # 遍历所有地块的坐标多边形
                if is_in_poly(p=jingweidu, poly=coordinates):
                    xuhao_dikuaibianma[index+1] = number
                    print(index+1, number)
                sums += 1

    print(f"判断79个点是否可能落在19275个多边形内, 共对比{sums}次")
    print(xuhao_dikuaibianma)
    np.save(f'xuhao_dikuaibianma.npy', xuhao_dikuaibianma) # 注意带上后缀名
