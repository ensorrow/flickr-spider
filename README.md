# Flickr爬虫

## Overview

爬虫爬取的信息说明：

用户的nsid，用户联系人（联系人将加入用户队列），群组，照片（最多只爬500张），标签。`main.py`作为生产者，将照片url存入数据库，`save.py`作为消费者，根据url下载对应的图片。

文件说明：

- main.py 多线程获取用户信息主流程
- model.py 数据库相关操作，文件读写相关操作函数定义
- service.py 网络接口定义
- utils.py 工具函数定义
- save.py 将表中的图片url多线程下载到本地存储
- *queue.json 用于队列初始化及爬虫中断时队列的本地存储

<!-- 
代码结构说明：
- main.py: 主程序入口，负责协调整个爬虫流程
- model.py: 数据模型和数据库交互逻辑
- service.py: 与Flickr API通信的网络服务层
- utils.py: 通用工具函数集合
- save.py: 图片下载和保存模块
- queue.json: 队列状态持久化文件
-->

## Usage

启动mongodb，初始化queue.json如下：

```json
[1, "128950283@N02", "128161560@N07", "127180464@N07", "61500992@N03", "44542478@N03"]
```

`queue[0]`用于存储队头index，因为考虑去重的需要队列的出队不能采用get方法。之后运行`main.py`再运行`save.py`即可，flickr访问需要科学上网。

<!-- 
运行步骤：
1. 启动MongoDB服务
2. 配置queue.json初始队列数据
3. 执行main.py开始爬取用户信息和图片URL
4. 执行save.py下载图片到本地
注意事项：
- 需要科学上网环境
- MongoDB需正确配置连接参数
- queue.json格式必须正确，第一个元素为队列索引
-->

