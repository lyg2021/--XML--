from delet_coordinates import main


if __name__ == "__main__":

    for i in range (1, 10):


        # 多边形xml路径
        poly_xml_path = f"D:\Workplace\python\打标XML处理\split_xml\split_part{i}.xml"


        # 待处理的xml路径
        input_path = "shawan_6_fenlei_GEOGCS_new.xml"
        output_path = f"shawan_6_fenlei_GEOGCS_new_part{i}.xml"

        
        main(input_path=input_path,                         # 需要处理的xml标签路径(名称)
            output_path=output_path,                       # 处理后输出的xml标签路径(名称)
            poly_xml_path=poly_xml_path)                   # 多边形xml路径