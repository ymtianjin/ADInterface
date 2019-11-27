# encoding=utf-8
# @author:chenhaibin

import logging
from util.const import Const
from interface import getInterfaceValue, getQueryCellCode


def query_layout_code(page_name, page_id):
    """
    #在页面信息接口中，查询blockId，layoutCode
    #将页面信息传给函数query_cellCode
    :param page_name:导航名称
    :param page_id:导航id
    :return json_layout_value:区块json数据
    """
    try:
        json_layout_value = ""
        layout_dirt = {'blockId': '', 'layoutCode': ''}
        url_page = Const.url_page + page_id + '.json'
        layout_dirt, json_unicode_str = getInterfaceValue.get_url_value(layout_dirt, url_page)
        block_id_arr = layout_dirt['blockId']
        print(u'区块ID=%s' % block_id_arr)
        logging.info('区块ID=%s' % block_id_arr)
        layout_arr = layout_dirt['layoutCode']
        for index_layout in range(len(layout_arr)):
            layout_info = "%s={%s :[%s,\'%s\']" % (page_name, str(index_layout + 1), str(block_id_arr[index_layout]), str(int(layout_arr[index_layout][7:])))
            print("######################%s######################" % layout_info)
            logging.info(layout_info)
            block_id = block_id_arr[index_layout]
            layout_code = layout_arr[index_layout]
            # 查询每个区块内的推荐位信息
            json_cell_code, check_flag = getQueryCellCode.query_cell_code(block_id, layout_code, json_unicode_str)
            if "" != json_cell_code:
                content_info = "," + str(json_cell_code[:-1])
            else:
                content_info = json_cell_code[:-1]
            json_layout_code = "[\'%s\'%s]," % (str(layout_code[-3:]), content_info)
            json_layout_value += json_layout_code
            if check_flag:
                break
        print('##############################################')
        return json_layout_value
    except BaseException as e:
        logging.error(e)
