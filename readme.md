未来电视广告接口测试，autho：lm<br>

1.域名支持配置文件，访问的url支持变量，常量，1，（完成，9月6日）<br>
2.字符串截取和拼接，支持字符串分隔，全局变量支持map或者数组，字符串截取和拼接，2<br>
3.支持for循环，且循环包含条件判断，3-4<br>
4.支持函数，5-8<br>

<br>
变量的使用<br>
1、定义，变量可以二次定义<br>
a、单独的一行使用define关键字定义，用于定义全局使用的变量<br>
方法列：function<br>
url列：define<br>
参数名列：变量名，需要使用global_开头，如：global_data<br>
参数值列：任意常量值<br>
b、在get或者post方法中定义，用于定义全局使用的变量，该变量从当前的get或者post的结果中获取数据<br>
变量名列：变量名，需要使用global_开头<br>
变量值列：需要是返回值的路径表示方法，可以从返回值中获取对应的值<br>
c、单独的一行使用split关键字定义，用指定的参数值列的值去分割参数名列所指向的变量，分割出来后将会是一个数组放入原变量中，使用变量加下标方式获取值<br>
方法列：function<br>
url列：split<br>
参数名列：变量名，需要使用global_开头，如：global_data<br>
参数值列：分割的字符，如：,<br>
d、单独的一行使用join关键字定义，用指定的参数值列的值去组合参数名列所指向的变量（该变量必须是数组），分割出来后将会是一个字符串放入原变量中<br>
方法列：function<br>
url列：join<br>
参数名列：变量名，需要使用global_开头，如：global_data<br>
参数值列：分割的字符，如：,<br>
e、单独的一行使用substr关键字定义，用指定的参数值列的值通过开始和结束的方式访问字符串获得子串，获取到的字符串放入原变量<br>
方法列：function<br>
url列：substr<br>
参数名列：变量名，需要使用global_开头，如：global_data<br>
参数值列：分割的字符，如：[1:3]<br>
2、使用，可以在url、参数值中使用变量，使用的时候必须用{$}的形式把变量包裹起来，如：{$global_data}，则会使用找到的值替换，否则保持不变<br>
接口地址：<br>
创建投放接口：http://admin.adott.ottcn.org/api/mediabuy_operate<br>
获取投放接口：http://api.test.adott.ottcn.com/ad?deviceid=1234&at=before&appkey=100001&channelcode=101<br>
