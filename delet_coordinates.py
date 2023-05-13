from xml.etree.ElementTree import *
from tqdm import tqdm


def is_in_poly(p:list, poly:list):
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


def delete_coordinates(tree: ElementTree, poly:list):
    """返回一个处理好的tree"""

    # 获取根节点Element
    root = tree.getroot()

    # print(type(tree), root)

    # for child in root:
    #     print(child.tag, child.attrib)

    # 获取到节点深处的某个元素的text，返回一个列表，存放所有的float数据
    Region_Element_list = root.findall("Region")
    for Region in tqdm(Region_Element_list):
        GeometryDef_Element_list = Region.findall("GeometryDef")
        for GeometryDef in GeometryDef_Element_list:
            CoordSysStr = GeometryDef.find(
                "CoordSysStr")  # 通过这条的text判断他是地理坐标还是投影坐标
            CoordSysStr_Text = CoordSysStr.text
            Polygon_Element_list = GeometryDef.findall("Polygon")
            for Polygon in tqdm(Polygon_Element_list):
                Exterior_Element_list = Polygon.findall("Exterior")
                for Exterior in Exterior_Element_list:
                    LinearRing_Element_list = Exterior.findall("LinearRing")
                    for LinearRing in LinearRing_Element_list:
                        Coordinates_Element_list = LinearRing.findall("Coordinates")
                        for Coordinates in Coordinates_Element_list:
                            Coordinates_Text = Coordinates.text

                            # 在多边形内就将值赋为 "0 0 0 0"  (这条最好解耦下)
                            if delete_in_polygon(Coordinates_Text, poly=poly):
                                Coordinates.text = "0 0 0 0"


    Region_Element_list = root.findall("Region")
    for Region in Region_Element_list:
        GeometryDef_Element_list = Region.findall("GeometryDef")
        for GeometryDef in tqdm(GeometryDef_Element_list):
            CoordSysStr = GeometryDef.find(
                "CoordSysStr")  # 通过这条的text判断他是地理坐标还是投影坐标
            CoordSysStr_Text = CoordSysStr.text
            Polygon_Element_list = GeometryDef.findall("Polygon")
            for Polygon in tqdm(Polygon_Element_list):
                Exterior_Element_list = Polygon.findall("Exterior")
                for Exterior in Exterior_Element_list:
                    LinearRing_Element_list = Exterior.findall("LinearRing")
                    for LinearRing in LinearRing_Element_list:
                        Coordinates_Element_list = LinearRing.findall("Coordinates")
                        for Coordinates in Coordinates_Element_list:
                            if Coordinates.text == "0 0 0 0":
                                # 如果值为 "0 0 0 0"
                                GeometryDef.remove(Polygon)

    return tree


def get_coordinates_list(input_path:str):
    """返回一个坐标系列表"""

    # 创建一个 ElementTree对象
    tree = ElementTree()

    # 获取文件路径
    xml_path = input_path

    # 读取 XML 文件
    tree.parse(xml_path)

    # 获取根节点Element
    root = tree.getroot()

    # 初始化字符串列表
    coordinates_list = []

    # 获取到节点深处的某个元素的text，返回一个列表，存放所有的float数据
    Region_Element_list = root.findall("Region")
    for Region in Region_Element_list:
        GeometryDef_Element_list = Region.findall("GeometryDef")
        for GeometryDef in GeometryDef_Element_list:
            CoordSysStr = GeometryDef.find(
                "CoordSysStr")  # 通过这条的text判断他是地理坐标还是投影坐标
            CoordSysStr_Text = CoordSysStr.text
            Polygon_Element_list = GeometryDef.findall("Polygon")
            for Polygon in Polygon_Element_list:
                Exterior_Element_list = Polygon.findall("Exterior")
                for Exterior in Exterior_Element_list:
                    LinearRing_Element_list = Exterior.findall("LinearRing")
                    for LinearRing in LinearRing_Element_list:
                        Coordinates_Element_list = LinearRing.findall("Coordinates")
                        for Coordinates in Coordinates_Element_list:
                            Coordinates_Text = Coordinates.text
                            coordinates_list.append(Coordinates_Text)

    return coordinates_list
    
                            


def coordinates_text_to_float_number_list(Coordinates_Text: str):
    # 将获取到的字符串转化为类型为浮点数的列表或数组，
    # 返回浮点数列表
    float_number_list = []
    float_number = ""
    Coordinates_Text += " "
    for char in Coordinates_Text:
        if (char != " " and char != "\n"):
            float_number += char
        elif float_number != "":
            float_number = float(float_number)
            float_number_list.append(float_number)
            float_number = ""

    return float_number_list


def delete_in_polygon(Coordinates_Text: str, poly: list = None):
    float_number_list = coordinates_text_to_float_number_list(Coordinates_Text)
    tem_x = 0
    tem_y = 0
    for index, point in enumerate(float_number_list):
        if index%2 == 0:
            tem_x = point
        else:
            tem_y = point
            if is_in_poly(p=[tem_x, tem_y], poly=poly):
                return True
    return False


def get_poly_list_list(poly_xml_path:str):
    """获取poly_list_list"""
    # 多边形xml路径
    poly_xml_path = poly_xml_path

    float_number_list_list = []
    poly_list = []
    poly_list_list = []

    coordinates_text_list = get_coordinates_list(poly_xml_path)

    for index, coordinates_text in enumerate(coordinates_text_list):
        float_number_list = coordinates_text_to_float_number_list(Coordinates_Text=coordinates_text)
        float_number_list_list.append(float_number_list)

    for float_number_list in float_number_list_list:
        poly_list = []
        for index, float_number in enumerate(float_number_list):
            if index%2 == 0:
                temp_list = []
                temp_list.append(float_number)
            else:
                temp_list.append(float_number)
                poly_list.append(temp_list)
        poly_list_list.append(poly_list)

    return poly_list_list


def main(input_path:str, output_path:str, poly_xml_path:str):

    # 创建一个 ElementTree对象
    tree = ElementTree()

    # 获取文件路径
    xml_path = input_path

    # 读取 XML 文件
    tree.parse(xml_path)

    # 获取poly_list_list
    poly_list_list = get_poly_list_list(poly_xml_path=poly_xml_path)

    # 修改,删除多边形范围内的标签
    for poly_list in poly_list_list:
        tree = delete_coordinates(tree, poly=poly_list)

    # 保存
    tree.write(output_path, encoding="utf-8")

    # 添加一行内容
    with open(output_path, 'r+', encoding="utf-8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + content)

    print("complete")


if __name__ == "__main__":
    """用于删除多边形区域内的所有标签, 
    输入1: 用envi画出多边形区域, 把画出的多边形区域导出xml,
    输入2: 待处理的xml标签
    输出: 做删除处理好的标签    
    """

    # 多边形xml路径
    poly_xml_path = "delete.xml"


    # 待处理的xml路径
    input_path = "nongtian_all.xml"
    output_path = "nongtian_all11111.xml"


    main(input_path=input_path,                         # 需要处理的xml标签路径(名称)
         output_path=output_path,                       # 处理后输出的xml标签路径(名称)
         poly_xml_path=poly_xml_path)                   # 多边形xml路径

