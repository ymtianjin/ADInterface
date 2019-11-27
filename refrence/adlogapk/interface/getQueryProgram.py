# encoding=utf-8
# @author:chenhaibin

import logging
from util import fileProcess, readConfig
from util.const import Const
from interface import getInterfaceValue


def query_program(block_id, layout_code, cell_code_value, content_id, content_title, content_type, action_type):
    """
    # 在子节目接口中，查询contentUUID,contentType
    :param block_id: 区块id
    :param layout_code: 区块编号
    :param cell_code_value: 推荐位编号
    :param content_id: 内容id
    :param content_title: 内容标题
    :param content_type: 内容类型
    :param action_type: 内容起播类型
    :return program_info: 返回节目相关信息
    """
    try:
        program_info = ""
        s_content_id = ""
        s_program_id = ""
        s_content_type = ""
        s_action_type = ""
        s_location_id = ""
        check_flag = False
        duration_flag = False
        cell_flag = False
        cell_code_value_arr = cell_code_value.split('_')
        cell_code_index = cell_code_value_arr[2]
        conf_dict = readConfig.read_config('Json-Init')
        program_dirt = {'contentUUID': '', 'contentType': '', 'duration': ''}
        url_program = Const.url_program + content_id + '.json' + Const.c_url_program
        program_dirt, json_value = getInterfaceValue.get_url_value(program_dirt, url_program)
        program_id_arr = program_dirt['contentUUID']
        program_type_arr = program_dirt['contentType']
        duration_arr = program_dirt['duration']
        print("节目时长=%s" % duration_arr)
        if duration_arr:
            for c_duration_arr in duration_arr:
                if c_duration_arr >= str(int(conf_dict.get('init_program_duration'))*60):
                    duration_flag = True
                else:
                    duration_flag = False
                    print("节目时长小于%s分钟[%s秒],条件不符合" % (conf_dict.get('init_program_duration'), str(int(conf_dict.get('init_program_duration'))*60)))
                    break
        if duration_flag:
            if program_id_arr:
                sum_program = len(program_id_arr)
                if int(conf_dict.get('init_program_sum')) <= sum_program:
                    # 计算符合条件的推荐位个数
                    getInterfaceValue.set_cell_sum()
                    getInterfaceValue.content_type_dict[content_type] = int(
                        getInterfaceValue.content_type_dict[content_type]) + 1
                    logging.info('更新内容类型[%s=%s]' % (content_type, getInterfaceValue.content_type_dict[content_type]))
                    print("更新内容类型[%s=%s]" % (content_type, getInterfaceValue.content_type_dict[content_type]))
                    for index_program in range(len(program_type_arr)):
                        if index_program >= int(conf_dict.get('init_program_sum')):
                            break
                        s_content_id += content_id + ','
                        s_program_id += program_id_arr[index_program] + ','
                        s_content_type += program_type_arr[index_program] + ','
                        s_action_type += action_type + ','
                        s_location_id += str(block_id) + '+' + str(layout_code) + '+' + str(cell_code_value) + ','
                        index_program += 1

                    # print('seriesID:%s' % str(s_content_id[:-1]))
                    # print('programID:%s' % str(s_program_id[:-1]))
                    # print('contentType:%s' % str(s_content_type[:-1]))
                    # print('actionType:%s' % str(s_action_type[:-1]))
                    # print('locationID:%s' % str(s_location_id[:-1]))
                    # print('contentID:%s' % str(s_content_id[:-1]))

                    logging.info('seriesID:%s' % str(s_content_id[:-1]))
                    logging.info('programID:%s' % str(s_program_id[:-1]))
                    logging.info('contentType:%s' % str(s_content_type[:-1]))
                    logging.info('actionType:%s' % str(s_action_type[:-1]))
                    logging.info('locationID:%s' % str(s_location_id[:-1]))
                    logging.info('contentID:%s' % str(s_content_id[:-1]))

                    print(Const.result_file_path)
                    # 输出预期信息到文件
                    fileProcess.write_txt_file('seriesID:%s' % str(s_content_id[:-1]) + '\n'
                                               + 'programID:%s' % str(s_program_id[:-1]) + '\n'
                                               + 'contentType:%s' % str(s_content_type[:-1]) + '\n'
                                               + 'actionType:%s' % str(s_action_type[:-1]) + '\n'
                                               + 'locationID:%s' % str(s_location_id[:-1]) + '\n'
                                               + 'contentID:%s' % str(s_content_id[:-1]), Const.result_file_path)

                    program_info += "{%s:['%s','%s']}," % (str(int(cell_code_index) - 1), content_type, content_title)
                    print("found:%s" % str(program_info[:-1]))
                    logging.info("found:%s" % str(program_info[:-1]))
                    check_flag = getInterfaceValue.check_content_type_value()
                else:
                    logging.info('子节目个数=%s(小于初始化的子节目个数%s),条件不符合' % (sum_program, conf_dict.get('init_program_sum')))
                    print(u'子节目个数=%s(小于初始化的子节目个数%s),条件不符合' % (sum_program, conf_dict.get('init_program_sum')))
            else:
                logging.info('子节目个数=%s[contentUUID数据有问题,条件不符合]' % program_id_arr)
                print('子节目个数=%s[contentUUID数据有问题,条件不符合]' % program_id_arr)
        return program_info, check_flag
    except BaseException as e:
        logging.error(e)
