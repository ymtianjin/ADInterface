变量的使用

1、定义，变量可以二次定义

a、单独的一行使用define关键字定义，用于定义全局使用的变量

方法列：define

变量名列：变量名，需要使用global_开头，如：global_data

变量值列：任意常量值


b、在get或者post方法中定义，用于定义全局使用的变量，该变量从当前的get或者post的结果中获取数据

变量名列：变量名，需要使用global_开头

变量值列：需要是返回值的路径表示方法，可以从返回值中获取对应的值

2、使用，可以在url、参数值中使用变量，使用的时候必须用{$}的形式把变量包裹起来，如：{$global_data}，则会使用找到的值替换，否则保持不变


接口地址：

创建投放接口：http://admin.adott.ottcn.org/api/mediabuy_operate

获取投放接口：http://api.test.adott.ottcn.com/ad?deviceid=1234&at=before&appkey=100001&channelcode=101