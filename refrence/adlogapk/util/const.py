# encoding=utf-8
__author__ = 'lqq'
# 存放变量、常量

from util import fileProcess, readConfig


class Const(object):
    """
    常用变量、常量类
    """
    pro_log_file_path = fileProcess.get_file_dir('Program') + '.log'  # 运行过程日志记录文件路径

    app_tag = readConfig.read_config("Device-Info").get('appTag')

    # 页面左上角logo的xpath定位，用于判断应用是否正常启动
    logo_xpath = '//android.widget.RelativeLayout[@index=0]/android.widget.ImageView[@index=1]'
    # logo_xpath = '//android.widget.FrameLayout[@index=0]/android.widget.ImageView[@index=0]'

    # 详情页付费按钮id，用于判定节目的收费类型
    vip_id = app_tag + ':id/vip_pay'

    # 详情页标题id，用于判断是否进入指定详情页
    detail_title_id = app_tag + ':id/id_detail_title'

    # 播放失败错误码
    err_code_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=0]'

    # 播放鉴权失败
    err_auth_xpath = '//android.widget.FrameLayout[@index=1]/android.widget.FrameLayout[@index=0]/android.widget.TextView[@index=3]'

    # 一级导航的xpath
    first_class_xpath = '//android.support.v7.widget.RecyclerView[@index=2]/android.widget.FrameLayout[@index=2]/android.widget.TextView'

    # 二级导航的xpath
    second_class_xpath = '//android.widget.FrameLayout[@index=4]/android.widget.RelativeLayout[@index=0]' \
                         '/android.support.v7.widget.RecyclerView[@index=0]/android.widget.RelativeLayout[@index=3]/android.widget.TextView'

    # 查找导航循环次数
    navigation_count= 20
    # 一级导航焦点下移至二级导航时的等待时长
    navigation_wait_time = 5



