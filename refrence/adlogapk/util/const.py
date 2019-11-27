# encoding=utf-8

__author__ = 'zhangwy'
from util import fileProcess, readConfig


class Const(object):
    """
    常用变量、常量类
    """
    result_file_path = fileProcess.get_file_dir('CaseResult') + '.txt'  # CaseResult文件路径
    except_file_path = fileProcess.get_file_dir('CaseExcept') + '.txt'  # CaseExcept文件路径
    log_file_path = fileProcess.get_file_dir('YSYY') + '.log'  # log文件路径
    pro_log_file_path = fileProcess.get_file_dir('Program') + '.log'  # 运行过程日志记录文件路径

    app_tag = readConfig.read_config("Device-Info").get('appTag')

    # 页面左上角logo的xpath定位，用于判断应用是否正常启动
    logo_xpath = '//android.widget.RelativeLayout[@index=0]/android.widget.ImageView[@index=1]'
    # logo_xpath = '//android.widget.FrameLayout[@index=0]/android.widget.ImageView[@index=0]'

    # 详情页付费按钮id，用于判定节目的收费类型
    vip_id = app_tag + ':id/vip_pay'

    # 详情页标题id，用于判断是否进入指定详情页
    detail_title_id = app_tag + ':id/id_detail_title'

    # 播放器进度条左侧时间点，表示当前播放进度
    left_time = app_tag + ':id/seebar_left_time'

    # 播放器进度条右侧时间点，表示节目总时长
    right_time = app_tag + ':id/seebar_right_time'

    # 播放失败错误码
    err_code_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=0]'

    # 播放鉴权失败
    err_auth_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=3]'

    # 一级导航的xpath
    first_class_xpath = '//android.support.v7.widget.RecyclerView[@index=2]/android.widget.FrameLayout[@index=2]/android.widget.TextView'

    # 二级导航的xpath
    second_class_xpath = '//android.widget.FrameLayout[@index=4]/android.widget.RelativeLayout[@index=0]' \
                         '/android.support.v7.widget.RecyclerView[@index=0]/android.widget.RelativeLayout[@index=3]/android.widget.TextView'
    conf_dict = readConfig.read_config('Json-Init')
    # 接口地址
    url = conf_dict.get('url')
    # 央视影音appkey
    app_key = conf_dict.get('app_key')
    # 央视影音ChannelCode
    channel_code = conf_dict.get('channel_code')
    # 导航信息接口
    url_index = url + '/api/v31/' + app_key + '/0/navigation/index.json'
    # 页面信息接口
    url_page = url + '/api/v31/' + app_key + '/0/page/'
    # 内容信息接口
    url_content = url + '/api/v31/' + app_key + '/0/content/'
    # 子节目信息接口部分参数1
    url_program = url + '/api/v31/' + app_key + '/' + channel_code + '/detailsubcontents/'
    # 子节目信息接口部分参数2
    c_url_program = '?subcontenttype=subcontents'
    # Requests设置请求头Headers信息
    request_header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}








