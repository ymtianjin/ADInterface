# encoding=utf-8
__author__ = 'lqq'
# 结果写回

import datetime
import os


def get_file_dir(file_name):
    """
    获取文件存储路径
    :return:文件存储路径
    """
    date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    file_path = get_target_dir() + file_name + '-' + date
    return file_path


def get_target_dir():
    """
    获取日志存储上层路径
    :return:日志存储上层目标文件夹
    """
    target_dir = 'D:\\Temp'
    date = datetime.datetime.now().strftime('%Y%m%d')
    target_path = target_dir + '\\' + date + '\\'
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    # else:
    #     print("文件夹已存在")
    return target_path


def write_txt_file(new_str, file_path):
    """
    将预期结果写入txt文件
    :param new_str: 需要写入的内容
    :param file_path:txt文件路径
    :return:
    """
    file_in = new_str+'\n'  # 需要写入的数据
    fp = open(file_path, 'a')  # 打开文件
    fp.write(file_in)  # 写入数据
    fp.flush()  # 刷新缓存
    os.fsync(fp)  # 确保文件写入磁盘
    fp.close()  # 关闭文件



def interface_data_processing(file_path = 'interfaceData'):
    '''
    读取配置文件，将文件内容分离目标导航数据、目标导航页面数据两部分；
    并将分离后的数据处理成目标导航字典，目标导航页面数据列表
    :param file_path 接口数据文件名称
    :return navigation_info_dict,page_block_list_info  目标导航字典，目标导航页面数据列表
    '''
    # cms3.1接口处理后的数据存储的文件路径
    print(os.getcwd())
    interface_data_file_path = os.getcwd()[:-4]+'config\\'+file_path
    print(interface_data_file_path)
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
    return navigation_info_dict,page_block_list_info




def interface_data_return(*args,file_path0 = 'interfaceData',file_path1 = 'interfaceDataReturn'):
    # # 文件路径及读文件
    # interface_data_file_path0 = os.getcwd()[:-4]+'config\\'+file_path0
    # print(interface_data_file_path0)
    #
    # with open(interface_data_file_path0,'r',encoding='UTF-8') as fp:
    #     content = fp.read()
    # # 文件内容字符串转化为list
    # interface_data = eval(content)
    # # 处理读取后的文件数据  Design by lqq
    # for block in interface_data[-1]:
    #     if len(block)>1:
    #         # print(block[-1])
    #         for key in block[-1].keys():
    #             block[-1][key][-1]=detail_title_name
    # print(interface_data)

    # 写回的文件路径Design by lqq
    # date = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # interface_data_file_path1 = os.getcwd()[:-4]+'config\\'+file_path1+date
    interface_data_file_path1 = os.getcwd()[:-4]+'config\\'+file_path1
    print(interface_data_file_path1)


    # 文件内容写回去
    with open(interface_data_file_path1,'w+',encoding='UTF-8') as fp:
        # content = fp.write(str(interface_data)+':'+str(Flag)+'\n')
        # fp.write(str(interface_data)+':'+str(Flag)+'\n')
        cons = ''
        for con in range(len(args)):
            if con+1 == len(args):
                cons += str(args[con])
            else:
                cons += str(args[con])+':'
        fp.write(cons+'\n')








