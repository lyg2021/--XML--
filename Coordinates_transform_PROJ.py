from pyproj import Proj
from  pyproj  import  CRS
from pyproj import Transformer
from tqdm import tqdm

from xml.etree.ElementTree import *


"""根据标签信息以及网站https://epsg.io/32645查询，WGS_1984_UTM_Zone_45N，
为EPSG:32645标准投影坐标系，计算xml数值时需要转化经纬度为proj投影坐标系"""

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


# longitude = 85.71625242     # 经度

# latitude = 44.24033768      # 纬度

# x, y = transformer.transform(latitude, longitude)   # 前纬度，后经度 
# print(x, y)


def change_to_proj(Coordinates_Text:str):

    Coordinates_Text = Coordinates_Text
    float_number_list = coordinates_text_to_float_number_list(Coordinates_Text=Coordinates_Text)

    crs=CRS.from_epsg(4326)
    transformer = Transformer.from_crs(crs_from=crs, crs_to=32645)

    tem_x = 0
    tem_y = 0
    for index, point in enumerate(float_number_list):
        if index%2 == 0:
            tem_x = point
        else:
            tem_y = point
            float_number_list[index-1], float_number_list[index] = transformer.transform(xx=tem_y, yy=tem_x)

    # 转换为字符串列表
    str_number_list = list(map(str, float_number_list))
    if str_number_list == []:
        new_Coordinates_Text = "0 0 0 0"
    else:
        new_Coordinates_Text = " ".join(str_number_list)
        new_Coordinates_Text = "\n" + new_Coordinates_Text + "\n            "

    return new_Coordinates_Text


def main(input_path:str, output_path:str, GEOGCS_CoordSysStr_Text:str, PROJ_CoordSysStr_Text:str):
    # 创建一个 ElementTree对象
    tree = ElementTree()

    # 获取文件路径
    xml_path = input_path

    # 读取 XML 文件
    tree.parse(xml_path)

    # 获取根节点Element
    root = tree.getroot()

        # 获取到节点深处的某个元素的text，返回一个列表，存放所有的float数据
    Region_Element_list = root.findall("Region")
    for Region in tqdm(Region_Element_list):
        GeometryDef_Element_list = Region.findall("GeometryDef")
        for GeometryDef in tqdm(GeometryDef_Element_list):
            CoordSysStr = GeometryDef.find(
                "CoordSysStr")  # 通过这条的text判断他是地理坐标还是投影坐标
            CoordSysStr_Text = CoordSysStr.text
            if CoordSysStr_Text == GEOGCS_CoordSysStr_Text:
                Polygon_Element_list = GeometryDef.findall("Polygon")
                for Polygon in tqdm(Polygon_Element_list):
                    Exterior_Element_list = Polygon.findall("Exterior")
                    for Exterior in Exterior_Element_list:
                        LinearRing_Element_list = Exterior.findall("LinearRing")
                        for LinearRing in LinearRing_Element_list:
                            Coordinates_Element_list = LinearRing.findall("Coordinates")
                            for Coordinates in Coordinates_Element_list:
                                Coordinates_Text = Coordinates.text
                                Coordinates.text = change_to_proj(Coordinates_Text=Coordinates_Text)                                    
                
                CoordSysStr.text = PROJ_CoordSysStr_Text                            

    # 保存
    tree.write(output_path, encoding="utf-8")

    # 添加一行内容
    with open(output_path, 'r+', encoding="utf-8") as f:
        content = f.read()
        f.seek(0, 0)
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + content)

    print("complete")


if __name__ == "__main__":
    main(input_path="shawan_6_fenlei.xml",          # 需要修改的xml
         output_path="shawan_6_fenlei_PROJ.xml",    # 修改后的xml

         # CoordSysStr_Text 标签的内容(地理坐标)
         GEOGCS_CoordSysStr_Text=r'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
         
         # CoordSysStr_Text 标签的内容(投影坐标)
         PROJ_CoordSysStr_Text=r'PROJCS["WGS_1984_UTM_Zone_45N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",87.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]')
    