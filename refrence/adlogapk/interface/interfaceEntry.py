# encoding=utf-8
# author:qq
# datetime:2019/8/1 8:53
# software: PyCharm
import os
# 读取接口数据

def interface_data_processing(file_path = 'interfaceData'):
    '''
    读取配置文件，将文件内容分离目标导航数据、目标导航页面数据两部分；
    并将分离后的数据处理成目标导航字典，目标导航页面数据列表
    :param file_path 接口数据文件名称
    :return navigation_info_dict,page_block_list_info  目标导航字典，目标导航页面数据列表
    lqq
    '''
    # cms3.1接口处理后的数据存储的文件路径
    print(os.getcwd())
    interface_data_file_path = os.getcwd()[:-4]+'config\\'+file_path
    # interface_data_file_path = os.getcwd()[:-9]+'config\\'+file_path
    # print(interface_data_file_path)
    # 读取该文件内容
    with open(interface_data_file_path,'r',encoding='UTF-8') as fp:
        content = fp.read()
    # 文件内容字符串转化为list
    interface_data = eval(content)
    # 导航字典
    navigation_info_dict = {'first_class_navigation': '', 'second_class_navigation': ''}
    navigation_data = interface_data[:2]
    navigation_info_dict['first_class_navigation'] = navigation_data[0]
    navigation_info_dict['second_class_navigation'] = navigation_data[-1]
    # 页面接口数据
    page_block_list_info = interface_data[-1]
    # print (navigation_info_dict,page_block_list_info)
    return navigation_info_dict,page_block_list_info






if __name__ == '__main__':
    interface_data_processing(file_path = 'interfaceData')
