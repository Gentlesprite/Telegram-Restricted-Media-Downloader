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
    <img src="https://img.shields.io/badge/pyrogram@kurigram-2.1.36-blue.svg?color=00B16A" alt="pyrogram@kurigram 2.1.36"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Windows%20-blue?color=00B16A" alt="Platform Windows"/>
  </a>
</p>


作者:[Gentlesprite](https://github.com/Gentlesprite)

B站视频教程:[点击观看](https://www.bilibili.com/video/BV1nCp8evEwv)

软件免费使用!并且在GitHub开源，如果你付费那就是被骗了。



# 1.0.下载地址:

蓝奏云:[点击跳转下载](https://wwgr.lanzn.com/b0fopovuf) 密码:ceze

Github:[点击跳转下载](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/releases)

## 1.1.推荐终端（选看）:

1. 对于Windows11用户，**Winodws Terminal**默认已**经安装好**，可直接**跳过**此步骤。

2. 对于Windows10用户，推荐使用**Winodws Terminal**作为**默认终端**，仅作为推荐安装，无论安装与否**不会影响本软件的使用**，**Winodws Terminal**能提供更出色的显示、交互、体验效果，以及避免出现**文字显示**乱码。

   Winodws Terminal 微软商店:[点击跳转下载](https://apps.microsoft.com/detail/9n0dx20hk701?launch=true&mode=full&hl=zh-cn&gl=cn&ocid=bingwebsearch)

   Winodws Terminal Github:[点击跳转下载](https://github.com/microsoft/terminal/releases)

3. 下载完成完成后**win+r**输入**wt**回车打开，然后将**Winodws Terminal**设为**默认终端**再启动软件，教程如下:

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/1_1_1.png)

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/1_1_2.png)

# 2.0.快速开始:

## 2.1.申请电报API

1. 前往网站:**https://my.telegram.org/auth**

   

2. 填写**自己绑定Telegram电报的手机号**注意手机号格式先要+地区再写入电话号码例如+12223334455，**+1**为地区，**222333445**为你绑定Telegram的手机号，填写后点击**Next**。

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_1.png)

   

3. 打开你的**Telegram客户端**，此时会收到来自**Telegram**账号的消息，将上面的验证码填入**Confirmation code**框中，然后点击**Sign in**。

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_2.png)

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_3.png)

   

4. 点击**API development tools**按照提示填入即可。

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_1_4.png)

   

5. 申请成功会得到一个**api_hash**和**api_id**保存下载，**切记不要泄露给任何人**！

## 2.2.配置文件说明

```yaml
# 下载完成直接打开软件即可,软件会一步一步引导你输入的!这里只是介绍每个参数的含义。
# 填入第一步教你申请的api_hash和api_id。
# 如果是按照软件的提示填,不需要加引号,如果是手动打开config.yaml修改配置,请仔细阅读下面内容。
# 手动填写注意区分冒号类型,例如 - 是:不是：。
# 手动填写的时候还请注意参数冒号不加空格会报错,后面有一个空格,例如 - api_hash: xxx而不是api_hash:xxx。
api_hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #api_hash没有引号。
api_id: 'xxxxxxxx' #注意配置文件中只有api_id有引号。
# download_type是指定下载的类型,只支持video和photo写其他会报错。
download_type: 
- video 
- photo
is_shutdown: true # 是否下载完成后自动关机 true为下载完成后自动关机 false为下载完成后不关机。
links: D:\path\where\your\link\txt\save\content.txt # 链接地址写法如下:
# 新建txt文本,一个链接为一行,将路径填入即可请不要加引号,在软件运行前就准备好。
# D:\path\where\your\link\txt\save\content.txt 请注意一个链接一行。
# 列表写法已在v1.1.0版本中弃用,目前只有上述唯一写法。
# 不要存在中文或特殊字符。
max_download_task: 3 # 最大的同时下载任务数 注意:如果你不是Telegram会员,那么最大同时下载数只有1。
proxy: # 代理部分,如不使用请全部填null注意冒号后面有空格,否则不生效导致报错。
  enable_proxy: true # 是否开启代理 true为开启 false为关闭。
  hostname: 127.0.0.1 # 代理的ip地址。
  is_notice: false # 是否开启代理提示, true为每次打开询问你是否开启代理, false则为关闭。
  scheme: socks5 # 代理的类型,支持http,socks4,socks5。
  port: 10808 # 代理ip的端口。
  username: null # 代理的账号,有就填,没有请都填null。
  password: null # 代理的密码,有就填,没有请都填null。
save_path: F:\path\the\media\where\you\save # 下载的媒体保存的地址,没有引号,不要存在中文或特殊字符。
# 再次提醒,由于nuitka打包的性质决定,中文路径无法被打包好的二进制文件识别。
# 故在配置文件时无论是链接路径还是媒体保存路径都请使用英文命名。
```

## 2.4.**使用注意事项**

1. 链接获取方法：对想要保存的媒体文件点击**鼠标右键**然后选择**复制消息直链**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_4_1.png)

2. 目前支持**视频**和**图片**两种类型的下载。

3. 如果当前复制的**链接**为多张图片或视频，那么程序会**自动下载当前消息所有的内容**!

4. 现在的部分频道为了避免封禁将媒体文件放在了**评论区**，并且还禁止转发，此时如想下载**评论区**里面的**视频**和**图片**，请不要复制当前消息的**链接**。请直接打开评论区，找到任意一个**图片**或者**视频**，按照上面所教的方法**复制评论区**的任意**视频**或**图片**的**消息直链**即可下载当前评论区**所有**的**视频**和**图片**，评论区的**消息直链**复制的后，后缀会带一个?comment=123456，代表是下载评论区的内容，请不要将其删除！如果需要下载评论区的内容请勿手动在链接后添加?comment=123456，而是采用上述**复制**的方法，避免出错。

5. links的文本**写法1**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_4_2.png)

6. 你所需要下载的视频前提是你当前的Telegram账号，在此视频链接的频道中，否则会报错无法下载！！！

7. 常见的**错误**写法(**请不要这样写**)：

   ![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/2_4_3.png)

   字段解释：

   | 字段              | 解释          |
   |-----------------|-------------|
   | ?comment        | 讨论组         |
   | ?single         | 单独的某个媒体     |
   | ?single&comment | 讨论组中单独的某个媒体 |
   | /c              | 私密频道        |
   
   链接解释:
   
   Telegram链接组成:
   
   正常频道:https://t.me/频道名/消息ID
   
   私密频道:https://t.me/c/频道名(10位纯数字)/消息ID
   
   | 链接                                       | 频道名 | 消息ID | 解释                                           |
   |------------------------------------------| ------ |------|----------------------------------------------|
   | https://t.me/TEST/111                    | TEST   | 111  | 下载该链接的**所有视频图片**                             |
   | https://t.me/TEST/111?single             | TEST   | 111  | 下载该链接的**所有视频图片**                             |
   | https://t.me/TEST/111?comment=666        | TEST   | 111  | 下载该链接的**视频图片**的同时，下载该链接下方的**讨论组**的**所有视频图片** |
   | https://t.me/TEST/111?single&comment=666 | TEST   | 111  | 下载该链接的**视频图片**的同时，下载该链接下方的**讨论组**的**所有视频图片** |
   | https://t.me/c/1111111111/666            | -1001111111111   | 666  | 下载该**私密频道**链接的所有视频图片                         |
   
   上述表格的**频道名**和**消息ID**都是**相同的**，这就代表的**重复链接**，**不要这样写**。
   
   原因：注意图片中**红框**的内容结合上述表格，你会发现?comment，?single和?single&comment**前面的内容**都是**一模一样**的，这代表这是**同样的一个链接**，如果需要**同时下载评论区和原本链接的内容**，只需填这**一个链接**即可**全部下载**。报错的原因是因为?comment链接本身就会下载全部内容，若此时再添加一个**前缀完全相同**的**没有带?comment的链接**，就会导致**这条链接的内容**被下载了**两次**，如果**上一次**的任务还没下载完，**同样的链接**的下载任务再一次地被添加进去了，就会导致下载报错。 
   
   如果你并非是想下载**评论区**中的内容，而只是**该链接的内容**。
   
   写法如下:
   
   正常频道:https://t.me/xxx/111

   私密频道:https://t.me/c/xxxxxxxxxx/111
   
   注意这样写就**不会下载评论区**的内容了!链接中如果带?single或?single&comment字段，不用管，**直接复制**进来，程序会为你下载该链接的**所有内容**！

# 3.0.在生产环境中运行

```bash
git clone https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader.git
cd Telegram-Restricted-Media-Downloader
pip install -r requirements.txt
python main.py
```



# 4.0.联系作者:

  Telegram交流群:[点击加入](https://t.me/+6KKA-buFaixmNTE1)

  Telegram:@Gentlesprite

  邮箱:Gentlesprite@163.com

# 5.0.支持作者:

![image](https://github.com/Gentlesprite/Telegram-Restricted-Media-Downloader/blob/main/res/pay.png)