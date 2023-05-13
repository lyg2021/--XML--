
from xml.etree.ElementTree import *

# 创建一个 ElementTree对象
tree = ElementTree()

xml_path = "test2022.xml"

# 读取 XML 文件
tree.parse(xml_path)

# 获取根节点Element 
root = tree.getroot()

# print(type(tree), root)

# for child in root:
#     print(child.tag, child.attrib)

# 获取到节点深处的某个元素的text
Region = root.find("Region")
GeometryDef = Region.find("GeometryDef")
CoordSysStr = GeometryDef.find("CoordSysStr")
Polygon = GeometryDef.find("Polygon")
Exterior = Polygon.find("Exterior")
LinearRing = Exterior.find("LinearRing")
Coordinates = LinearRing.find("Coordinates")

Coordinates_Text = Coordinates.text
# print(Coordinates_Text, type(Coordinates_Text))

# 将获取到的字符串转化为类型为浮点数的列表或数组
float_number_list = []
float_number = ""

for char in Coordinates_Text:    
    if(char != " " and char != "\n"):
        float_number += char
    elif float_number != "":    
        float_number = float(float_number)    
        float_number_list.append(float_number)
        float_number = ""

print(xml_path)
for number in float_number_list:
    print(number, type(number))

# CoordSysStr_Text = CoordSysStr.text
# print(CoordSysStr_Text)


# root = tree.getroot()
# for offspring in root.iter():
#     if offspring.get("Name") == "病人姓名":
#         offspring[0].text = "病患1号"
#         print(offspring[0].text)

# tree.write("xmlData/80.xml", encoding="utf-8")

