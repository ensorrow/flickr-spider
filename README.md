# Flickr爬虫 - lzy 2018

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

## Usage

启动mongodb，初始化queue.json如下：

```json
[1, "128950283@N02", "128161560@N07", "127180464@N07", "61500992@N03", "44542478@N03"]
```

`queue[0]`用于存储队头index，因为考虑去重的需要队列的出队不能采用get方法。之后运行`main.py`再运行`save.py`即可，flickr访问需要科学上网。

## Notice

对于使用SS、XX-NET这类代理的用户，运行时由于python requests模块证书不与系统同步的原因，会出现SSL验证错误，解决办法为手动设置`REQUESTS_CA_BUNDLE`为证书地址，以windows下的XX-NET为例，设置系统变量`REQUESTS_CA_BUNDLE`指向`${PATH 2 XX_NET}\data\gae_proxy\CA.crt`，记得运行一下`echo %REQUESTS_CA_BUNDLE%`看看有没有生效。

## 作者信息

### 作者

- **主要开发者**: lzy
- **开发时间**: 2018年
- **项目角色**: 原始开发者和维护者

### 联系方式

如有问题或建议，欢迎通过以下方式联系：

- GitHub: [项目仓库](https://github.com/username/flickr-spider) （请将 username 替换为实际的 GitHub 用户名）
- Issue 提交: 可在 GitHub 项目页面提交 Issue
- Email: [请添加联系邮箱]

### 贡献

欢迎贡献代码和改进建议！

**如何贡献:**
1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

**问题报告:**
- 请在 GitHub Issues 中详细描述遇到的问题
- 包含重现步骤和错误信息
- 提供运行环境信息（操作系统、Python 版本等）

### 许可证

本项目采用开源许可证。具体许可证信息请查看项目根目录下的 LICENSE 文件。

---

*感谢使用 Flickr 爬虫工具！*