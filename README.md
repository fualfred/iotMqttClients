# iotMqttClients
基于Mqtt协议编写的IOT设备模拟器（可以根据个人的业务继续修改），开发语言是Python，整体是Flask+paho.mqtt库实现的，提供多个接口用来辅助实现接口自动化测试，可根据个人业务进行修改

开发测试搭建过程

一、测试mqtt服务器搭建（实际开发不需要搭建）
通过docker命令进行搭建

1. 获取 Docker 镜像

 docker pull emqx/emqx:5.0.26
 
2. 启动 Docker 容器

docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:5.0.26

二、代码结构

<img width="423" alt="image" src="https://github.com/fualfred/IotMqttClientDevice/assets/21330243/b6876c75-d84b-49d0-ac2b-cfdaa65663b3">

buleprints: 蓝图文件 用来处理请求，包括设备连接等

config：订阅topic等配置

utils：工具包 包括日志、设备消息存储、mqtt客户端、mqtt设备管理类

config.py: flask框架的基本配置

app.py: 框架运行入口

requirements.txt: 开发需要的python库，可通过pip install -r requirement.txt安装所需要的包

三、提供的接口说明

    
##### 简要描述

- mqtt模拟设备连接mqtt服务

##### 请求URL
- ` http://xx.com/api/device/connect `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |
|host |是  |string | mqtt服务连接地址    |
|port     |是  |string | mqtt服务端口    |

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |



##### 简要描述

- mqtt模拟设备断开连接

##### 请求URL
- ` http://xx.com/api/device/offline?client_id =client_id `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |



##### 简要描述

- mqtt模拟设备重新连接

##### 请求URL
- ` http://xx.com/api/device/reconnect?client_id =client_id `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |

##### 简要描述

- mqtt模拟设备主动上报消息

##### 请求URL
- ` http://xx.com/api/device/upload?client_id =client_id `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |
| payload|是  |string |不用传递payload参数直接传需要上报的json数据   |

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |


##### 简要描述

- 通过requestTime获取服务下发到设备的消息

##### 请求URL
- ` http://xx.com/api/device/getMsgByRequestTime?client_id =client_id `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |
| requestTime|是  |int |请求的时间戳 |

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |


##### 简要描述

- 通过requestTime获取服务下发到设备的消息

##### 请求URL
- ` http://xx.com/api/device/setResponseMsg?client_id =client_id `
  
##### 请求方式
- POST 

##### 参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|client_id |是  |string |设备id   |
| requestTime|是  |string |默认是{requestTime} ,包含在需要预置响应的json数据里面即可|

##### 返回示例 

``` 
  {
    "code": 0,
    "msg": "success"
  }
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|code |int   |0 是成功，其他则是失败  |


实际上 需要实现IOT设备的接口自动化测试，模拟器的开发应该会比这个复杂（需要加上证书验证），但是整体思路可以参考，欢迎大家多多指教！

