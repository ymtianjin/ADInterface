# encoding=utf-8
# @author:chenhaibin
import datetime
import logging

from log import programLog
from util import readConfig
from interface import getQueryContent, getQueryProgram, getInterfaceValue


def query_cell_code(block_id, layout_code, unicode_str):
    """
    #在页面信息接口中，根据blockId去分区块划分
    #在页面信息的每个区块中，查询cellCode,contentType,l_id,l_actionType
    :param block_id:区块id
    :param layout_code:区块编号
    :param unicode_str:页面接口json数据
    :return json_cell_value:推荐位json数据
    """
    try:
        json_cell_value = ""
        content_title = ""
        vip_flag_content = ""
        ps_content_type = ""
        check_flag = False
        tv_live_param_flag = False
        conf_dict = readConfig.read_config('Json-Init')
        cell_code_dirt = {'cellCode': '', 'contentType': '', 'l_id': '', 'l_actionType': '', 'video': '', 'l_focusId': ''}
        # 在页面接口数据中，根据区块id，查询每个区块中数据字典中的信息
        cell_code_dirt = getInterfaceValue.get_url_block_id_value(cell_code_dirt, unicode_str, block_id)
        cell_code_arr = cell_code_dirt['cellCode']
        content_type_arr = cell_code_dirt['contentType']
        content_id_arr = cell_code_dirt['l_id']
        action_type_arr = cell_code_dirt['l_actionType']
        video_arr = cell_code_dirt['video']
        focus_id_arr = cell_code_dirt['l_focusId']
        print(video_arr)
        if video_arr:
            playStartTime, playEndTime = getInterfaceValue.get_json_str_dict_value(video_arr)
            system_time = datetime.datetime.now().strftime('%H:%M:%S')
            if (playStartTime < system_time) and (system_time < playEndTime):
                tv_live_param_flag = True
                print("此节目是直播")
            else:
                tv_live_param_flag = False
                # print('此节目是点播')
        if cell_code_arr and not tv_live_param_flag:
            for index_cell in range(len(cell_code_arr)):
                content_id = content_id_arr[index_cell]
                cell_code_value = cell_code_arr[index_cell]
                content_type = content_type_arr[index_cell]
                action_type = action_type_arr[index_cell]
                focus_id = focus_id_arr[index_cell]
                logging.info('------[%s/%s]--------------------------' % (index_cell+1, len(content_id_arr)))
                print('------[%s/%s]--------------------------' % (index_cell+1, len(content_id_arr)))
                logging.info('推荐位列表=%s' % content_id_arr)
                print('推荐位列表=%s' % content_id_arr)
                logging.info('当前推荐位=%s' % str(content_id))
                print('当前推荐位=%s' % str(content_id))
                logging.info('内容类型=%s' % str(content_type))
                print('内容类型=%s' % str(content_type))
                # 内容类型在初始化的列表中才符合要求
                if not getInterfaceValue.get_content_type_flag(content_type):
                    logging.info('内容类型=%s(在列表中才符合要求%s)' % (content_type,str(conf_dict.get('init_content_type_list'))))
                    print('内容类型=%s(在列表中才符合要求%s)' % (content_type,str(conf_dict.get('init_content_type_list'))))
                    continue
                # 查询目标焦点为null的推荐位
                if focus_id is not None:
                    logging.info('目标焦点=%s(目标焦点为null才符合要求)' % str(focus_id))
                    print('目标焦点=%s(目标焦点为null才符合要求)' % str(focus_id))
                    continue
                # 如果初始化的起播类型与此内容的起播类型不相等，则中断迭代，循环下一次迭代
                if conf_dict.get('init_action_type') != action_type:
                    logging.info('起播类型=%s(初始化起播类型为%s,条件不符合)' % (action_type, conf_dict.get('init_action_type')))
                    print('起播类型=%s(初始化起播类型为%s,条件不符合)' % (action_type, conf_dict.get('init_action_type')))
                    continue
                # 如果content_id不等于空，则查询内容接口中的数据
                if content_id != "":
                    content_title, vip_flag_content, ps_content_type = getQueryContent.query_content(content_id, content_type)
                else:
                    print('内容Id为空')
                    logging.info('内容Id为空')
                # 如果vip标识不等于0，则中断迭代，循环下一次迭代
                if '0' != vip_flag_content:
                    logging.info('vip标识=%s[%s不是免费节目，条件不符合]' % (vip_flag_content[0], vip_flag_content[0]))
                    print('vip标识=%s[%s不是免费节目，条件不符合]' % (vip_flag_content[0], vip_flag_content[0]))
                    continue
                # 如果此内容的标题等于空，则中断迭代，循环下一次迭代
                if 'null' == content_title:
                    logging.info('标题为空，条件不符合')
                    logging.info('--------------------------------')
                    print(u'标题为空，条件不符合\n--------------------------------')
                    continue
                # 查询出免费的节目和看点形式(KD)和剧集形式(JH)
                if 'PS' == content_type and 'KD' == ps_content_type:
                    content_type = 'KD'
                elif 'PS' == content_type and 'JH' == ps_content_type:
                    content_type = 'JH'
                # 获取该节目类型输出的次数
                query_content_type_sum = getInterfaceValue.get_content_type_value(content_type)
                if "" == query_content_type_sum or (
                        conf_dict.get('init_content_type_sum') <= str(query_content_type_sum)):
                    logging.info('内容类型个数=%s(大于等于初始化的内容类型%s个数%s,条件不符合)' % \
                                 (str(query_content_type_sum), str(content_type),
                                  str(conf_dict.get('init_content_type_sum'))))
                    print('内容类型个数=%s(大于等于初始化的内容类型%s个数%s,条件不符合)' % \
                          (str(query_content_type_sum), str(content_type), str(conf_dict.get('init_content_type_sum'))))
                    continue
                logging.info('locationID=%s+%s+%s' % (str(block_id), str(layout_code), str(cell_code_value)))
                print('locationID=%s+%s+%s' % (str(block_id), str(layout_code), str(cell_code_value)))
                cell_value, check_flag = getQueryProgram.query_program(block_id, layout_code, cell_code_value,
                                                                       content_id, content_title, content_type,
                                                                       action_type)
                json_cell_value += cell_value
                if check_flag:
                    break
        return json_cell_value, check_flag
    except BaseException as e:
        programLog.error_log(e)
