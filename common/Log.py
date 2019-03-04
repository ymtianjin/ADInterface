# encoding=utf-8
import os,logging,time

# 执行日志写入文件到results中

def  createMainLog(path):
    # 1、判断path是否存在，不存在创建
    if not os.path.exists(path):
        os.makedirs(path)
    # 指定日志路径
    logsDir=path
    #获取根日志,不指定名称，默认返回root
    logRoot=logging.getLogger()
    # 设置日志级别
    logRoot.setLevel(logging.DEBUG)

    #创建filehandle，日志格式
    # %(asctime)s","%(levelname)s","%(name)s","%(message)s"
    # 文件规格tests/results/%Y%m%d%H%M%S_Mainlog.csv
     #且文件的第一行是：'Time,Level,Logger Name,Message'
    logHandleRoot=logging.FileHandler(path+time.strftime('%Y%m%d%H%M%S')+'MainLog.log')
    logHandleRoot.setLevel(logging.DEBUG)
    logRoot.addHandler(logHandleRoot)
    logRoot.info('Time,Level,Logger Name,Message')
    fileFormater=logging.Formatter('%(asctime)s","%(levelname)s","%(name)s","%(message)s')
    logHandleRoot.setFormatter(fileFormater)

    #创建streamhandle，日志格式
    # %(asctime)s","%(levelname)s","%(name)s","%(message)s"
    logdHandle=logging.StreamHandler()
    logdHandle.setLevel(logging.INFO)
    streamFoemater=logging.Formatter('%(asctime)s","%(levelname)s","%(name)s","%(message)s')
    logdHandle.setFormatter(streamFoemater)
    logRoot.addHandler(logdHandle)

    return logRoot
