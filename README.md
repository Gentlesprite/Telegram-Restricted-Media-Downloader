<p align="center">
  <img width="15%" align="center" src="https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/logo.png" alt="logo">
</p>
  <h1 align="center">
  Telegram-Restricted-Media-Downloader
</h1>
<p align="center">
</p>
<p align="center">
  A telegram downloader on windows platform based on Python
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.11.7-blue.svg?color=00B16A" alt="Python 3.11.7"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/pyrogram-2.0.106-blue.svg?color=00B16A" alt="pyrogram 2.0.106"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Windows%20-blue?color=00B16A" alt="Platform Windows"/>
  </a>
</p>


作者:[Gentlesprite](https://github.com/Gentlesprite)

软件完全免费使用！禁止倒卖，如果你付费那就是被骗了。

# 1.0.下载地址:

蓝奏云:[点击跳转下载](https://wwgr.lanzn.com/b0fopovuf) 密码:ceze

Github:[点击跳转下载](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/releases)

# 2.0.快速开始:

## 2.1.申请电报API

1. 前往网站**https://my.telegram.org/auth**

   

2. 填写**自己绑定Telegram电报的手机号**注意手机号格式先要**+地区**再写入电话号码例如**+12223334455**，**+1**为地区，**222333445**为你绑定Telegram的手机号，填写后点击**Next**

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_1.png)

   

3. 打开你的**Telegram客户端**，此时会收到来自**Telegram**账号的消息，将上面的验证码填入**Confirmation code**框中，然后点击**Sign in**

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_2.png)

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_3.png)

   

4. 点击**API development tools**按照提示填入即可

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_4.png)

   

5. 申请成功会得到一个**api_hash**和**api_id**保存下载，**切记不要泄露给任何人**！

## 2.2.配置文件说明

```yaml
# 填入第一步教你申请的api_hash和api_id
api_hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #api_hash没有引号
api_id: 'xxxxxxxx' #注意配置文件中只有api_id有引号！！！
links: D:\path\where\your\link\txt\save\content.txt # 链接地址有2种格式:如下
# 新建txt文本,一个链接为一行,将路径填入即可请不要加引号
# 写法1:D:\path\where\your\link\txt\save\content.txt 请注意一个链接一行
# 写法2:['链接1','链接2','链接3','链接4'] 请注意逗号必须为","
max_download_task: 3 # 最大的同时下载任务数
# 注意:如果你不是telegram会员,那么最大同时下载数只有1
proxy: # 代理部分,如不使用请全部填null注意冒号后面有空格,否则不生效导致报错!
  scheme: socks5 # 代理的类型,支持socks5和http
  hostname: 127.0.0.1 # 代理的ip地址
  port: 10808 # 代理ip的端口
  username: null # 代理的账号,有就填,没有请都填null!
  password: null # 代理的密码,有就填,没有请都填null!
save_path: F:\path\the\media\where\you\save # 下载的媒体保存的地址
# 路径都尽量使用英文命名,避免不必要的报错
```

## 2.4.**使用注意事项**

1. 链接获取方法：对想要保存的媒体文件点击**鼠标右键**然后选择**复制消息直链**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_4_1.png)

2. 目前支持**视频**和**图片**两种类型的下载

3. 如果当前复制的**链接**为多张图片或视频，那么程序会**自动下载当前消息所有的内容**!

4. 现在的部分频道为了避免封禁将媒体文件放在了**评论区**，并且还禁止转发，此时如想下载**评论区**里面的**视频**和**图片**，请不要复制当前消息的**链接**。请直接打开评论区，找到任意一个**图片**或者**视频**，按照上面所教的方法**复制评论区**的任意**视频**或**图片**的**消息直链**即可下载当前评论区**所有**的**视频**和**图片**，评论区的**消息直链**复制的后，后缀会带一个**?comment**=123456，代表是下载评论区的内容，请不要将其删除！如果需要下载评论区的内容请勿手动在链接后添加?comment=123456，而是采用上述**复制**的方法，避免出错。

5. links的文本**写法1**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_4_2.png)

6. 你所需要下载的视频前提是你当前的Telegram账号，在此视频链接的频道中，否则会报错无法下载！！！



## 2.3.视频教程

B站视频教程:[在后续完成]()

# 3.0.在生产环境中运行

```bash
# 请使用python 3.11.7版本！
pip install -r requirements.txt
python main.py
```



# 4.0.联系作者:

  Telegram交流群:[点击加入](https://t.me/+6KKA-buFaixmNTE1)

  Telegram:@Gentlesprite

  邮箱:Gentlesprite@163.com

# 5.0.支持作者:

![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/pay.png)