<p align="center">
  <img width="15%" align="center" src="https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/logo.png" alt="logo">
</p>
  <h1 align="center">
  Telegram_Restricted_Media_Downloader
</h1>
<p align="center">
</p>
<p align="center">
  A telegram downloader on windows platform based on Python.
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.11.7-blue.svg?color=00B16A" alt="Python 3.11.7"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/pyrogram@kurigram-2.1.37-blue.svg?color=00B16A" alt="pyrogram@kurigram 2.1.37"/>
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

Github:[点击跳转下载](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/releases)

## 1.1.推荐终端（选看）:

1. 对于Windows11用户，`Winodws Terminal`默认**已经安装好**，可直接**跳过**此步骤。

2. 对于Windows10用户，推荐使用`Winodws Terminal`作为**默认终端**，仅作为推荐安装，无论安装与否**不会影响本软件的使用**，`Winodws Terminal`能提供更出色的显示、交互、体验效果，以及避免出现**文字显示**乱码。

   Winodws Terminal 微软商店:[点击跳转下载](https://apps.microsoft.com/detail/9n0dx20hk701?launch=true&mode=full&hl=zh-cn&gl=cn&ocid=bingwebsearch)

   Winodws Terminal Github:[点击跳转下载](https://github.com/microsoft/terminal/releases)

3. 下载完成完成后`win+r`输入`wt`回车打开，然后将`Winodws Terminal`设为**默认终端**再启动软件，教程如下:

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/1_1_1.png)

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/1_1_2.png)

# 2.0.快速开始:

## 2.1.申请电报API

1. 前往网站:**https://my.telegram.org/auth**

   

2. 填写**自己绑定**`Telegram`电报的**手机号**注意手机号格式先要+地区再写入电话号码例如`+12223334455`，`+1`为地区，`222333445`为你绑定`Telegram`的**手机号**，填写后点击`Next`。

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_1_1.png)

   

3. 打开你的`Telegram`客户端，此时会收到来自`Telegram`账号的消息，将上面的验证码填入`Confirmation code`框中，然后点击`Sign in`。

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_1_2.png)

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_1_3.png)

   

4. 点击`API development tools`按照提示填入即可。

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_1_4.png)

   

5. 申请成功会得到一个`api_hash`和`api_id`保存下载，**切记不要泄露给任何人！**

## 2.2.电报机器人(bot_token)申请及使用教程(选看)

### 	2.2.1.申请教程

1. 前往网站:https://t.me/BotFather 

2. 打开后会**提示**"要打开 Telegram Desktop 吗?"此时**点击**"打开Telegram Desktop"如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_1.png)

   如果没有这个弹窗，说明电脑没有安装**Telegram客户端**，安装后再重试即可。

3. **点击开始**，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_2.png)

4. 然后在当前**聊天框**中输入`/newbot`后回车，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_3.png)

   它会回复你`"Alright, a new bot. How are we going to call it? Please choose a name for your bot."`意思是给机器人取一个名字，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_4.png)

5. 这个名字是显示名称 (display name)，并不是唯一识别码，随便设置一下即可，之后可以通过 `/setname`命令进行修改。

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_5.png)

6. 接着设置机器人的**唯一名称**。字符串必须 以`bot`结尾，比如 `HelloWorld_bot` 或 `HelloWorldbot` 都是合法的。如果设置的名字已经被占用需要重新设置。如设置成了 `trmd_bot`但是这个名字已经有人使用了，此时会提示`"Sorry, this username is already taken. Please try something different."`意思是已经被使用了，需要拟定一个**不重复**的，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_6.png)

   如果结果如**上图**所示，则就代表名字**重复**了，需要**重新拟定**一个。

7. 直到提示你`"Done! Congratulations on your new bot. . ."`如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_7.png)

   如果结果如**上图**所示，则代表`bot_token`申请成功了，箭头指的红框处就是你所申请的`bot_token`，**切记不要泄露给任何人！**

### 	2.2.2.使用教程

1. 申请完成后，在软件配置时询问"是否启用「机器人」(需要提供bot_token)? - 「y|n」(默认n)"选择`y`代表**需要**使用，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_8.png)

   然后在**上图**箭头所指处填入"2.2.1.申请教程"第7步申请的`bot_token`后回车，即可配置完成。

2. 在一切配置完成，软件启动成功后等待提示"「机器人」启动成功。"，就代表机器人可以使用了，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_9.png)

3. 在`Telegram`客户端中找到与`BotFather`的对话框，找到"2.2.1.申请教程"第7步对话的位置(或者用你自己的方式找到你的机器人的对话框)，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_10.png)

   然后在**上图**箭头所指处即可**跳转**到机器人对话框。

4. **点击**开始，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_11.png)

   不出意外，会收到一条来自**机器人**发送的消息，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_12.png)

   **如果没收到**尝试尝试给机器人发送任意命令。

5. 目前机器人支持的命令用法及解释如下表所示：

   | 命令        | 用法                                                         | 解释                                           |
   | ----------- | ------------------------------------------------------------ | ---------------------------------------------- |
   | `/help`     | 向机器人发送发送`/help`即可。                                | 展示**可用**命令。                             |
   | `/download` | 向机器人发送`/download 视频链接1 视频链接2 视频链接3 视频链接n`即可。 | 分配**新的**下载任务。                         |
   | `/table`    | 向机器人发送`/table`即可。                                   | 在**终端**输出**当前**下载情况的**统计信息**。 |
   | `/exit`     | 向机器人发送`/exit`即可。                                    | **退出**软件。                                 |

6. `/help`命令使用教程，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_13.png)

7. 点击**菜单**可以显示机器人可用的命令，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_14.png)

8. `/download`命令使用教程，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_15.png)

   只要发送了正确的下载命令，终端就会创建对应的下载任务，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_16.png)

9. `/table`命令使用教程：

   需要**注意**的是，这个表格是**实时**的**状态**，并不是**最终**下载完成的**结果**，每一次使用它都会随着**当前**的**下载记录**而更新。

   **链接统计表**的使用，如下图所示:

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_17.png)

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_18.png)

   **计数统计表**的使用，如下图所示:

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_19.png)

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_20.png)

10. `/exit`命令使用教程，如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_2_21.png)

## 2.3.配置文件说明

```yaml
# 这里只是介绍每个参数的含义,软件会详细地引导配置参数。
# 如果是按照软件的提示填,选看。如果是手动打开config.yaml修改配置,请仔细阅读下面内容。
# 手动填写时请注意冒号是英文冒号,冒号加一个空格。
api_hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx # 申请的api_hash。
api_id: 'xxxxxxxx' # 申请的api_id。
# bot_token(选填)如果不填,就不能使用机器人功能。可前往https://t.me/BotFather免费申请。
bot_token: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
download_type: # 需要下载的类型。支持的参数:video,photo。
- video 
- photo
is_shutdown: true # 下载完成后是否自动关机。支持的参数:true,false。
links: D:\path\where\your\link\files\save\content.txt # 链接地址写法如下:
# 新建txt文本,一个链接为一行,将路径填入即可请不要加引号,在软件运行前就准备好。
# D:\path\where\your\link\txt\save\content.txt 一个链接一行。
# 不要存在中文或特殊字符。
max_download_task: 3 # 最大的下载任务数,非Telegram会员无效。支持的参数:所有>0的整数。
proxy: # 代理部分,如不使用请全部填null注意冒号后面有空格,否则不生效导致报错。
  enable_proxy: true # 是否开启代理。支持的参数:true,false。
  hostname: 127.0.0.1 # 代理的ip地址。
  is_notice: false # 开关是否询问使用代理的提示。支持的参数:true,false。
  scheme: socks5 # 代理的类型。支持的参数:http,socks4,socks5。
  port: 10808 # 代理ip的端口。支持的参数:0~65535。
  username: null # 代理的账号,没有就填null。
  password: null # 代理的密码,没有就填null。
save_path: F:\directory\media\where\you\save # 下载的媒体保存的目录,不要存在中文或特殊字符。
```

## 2.4.**使用注意事项**

1. 链接获取方法：对想要保存的媒体文件点击**鼠标右键**然后选择**复制消息直链**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_4_1.png)

2. 目前支持**视频**和**图片**两种类型的下载。

3. 如果当前复制的**链接**为多张图片或视频，那么程序会**自动下载当前消息所有的内容**!

4. 现在的部分频道为了避免封禁将媒体文件放在了**评论区**，并且还禁止转发，此时如想下载**评论区**里面的**视频**和**图片**，请不要复制当前消息的**链接**。请直接打开评论区，找到任意一个**图片**或者**视频**，按照上面所教的方法**复制评论区**的任意**视频**或**图片**的**消息直链**即可下载当前评论区**所有**的**视频**和**图片**，评论区的**消息直链**复制的后，后缀会带一个`?comment=123456`，代表是下载评论区的内容，请不要将其删除！如果需要下载评论区的内容请勿手动在链接后添加`?comment=123456`，而是采用上述**复制**的方法，避免出错。

5. links的文本**写法1**如下图所示：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_4_2.png)

6. 你所需要下载的视频前提是你当前的Telegram账号，在此视频链接的频道中，否则会报错无法下载！！！

7. 常见的**错误**写法(**请不要这样写**)：

   ![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/2_4_3.png)

   字段解释：

   | 字段              | 解释                     |
   | ----------------- | ------------------------ |
   | `?comment`        | 讨论组。                 |
   | `?single`         | 单独的某个媒体。         |
   | `?single&comment` | 讨论组中单独的某个媒体。 |
   | `/c`              | 私密频道。               |
   
   链接解释:
   
   `Telegram`链接组成:
   
   正常频道:`https://t.me/频道名/消息ID`
   
   私密频道:`https://t.me/c/频道名(10位纯数字)/消息ID`
   
   | 链接                                       | 频道名 | 消息ID | 解释                                           |
   |------------------------------------------| ------ |------|----------------------------------------------|
   | `https://t.me/TEST/111`                  | `TEST` | `111` | 下载该链接的**所有视频图片**。                           |
   | `https://t.me/TEST/111?single`           | `TEST` | `111` | 下载该链接的**所有视频图片**。                            |
   | `https://t.me/TEST/111?comment=666`      | `TEST` | `111` | 下载该链接的**视频图片**的同时，下载该链接下方的**讨论组**的**所有视频图片。** |
   | `https://t.me/TEST/111?single&comment=666` | `TEST` | `111` | 下载该链接的**视频图片**的同时，下载该链接下方的**讨论组**的**所有视频图片。** |
   | `https://t.me/c/1111111111/666`          | `-1001111111111` | `666` | 下载该**私密频道**链接的所有视频图片。                        |
   
   上述表格的**频道名**和**消息ID**都是**相同的**，这就代表的**重复链接**，**不要这样写**。
   
   原因：注意图片中**红框**的内容结合上述表格，你会发现`?comment`，`?single`和`?single&comment`**前面的内容**都是**一模一样**的，这代表这是**同样的一个链接**，如果需要**同时下载评论区和原本链接的内容**，只需填这**一个链接**即可**全部下载**。报错的原因是因为`?comment`链接本身就会下载全部内容，若此时再添加一个**前缀完全相同**的**没有带`?comment`的链接**，就会导致**这条链接的内容**被下载了**两次**，如果**上一次**的任务还没下载完，**同样的链接**的下载任务再一次地被添加进去了，就会导致下载报错。 
   
   如果你并非是想下载**评论区**中的内容，而只是**该链接的内容**。
   
   写法如下:
   
   正常频道:`https://t.me/xxx/111`

   私密频道:`https://t.me/c/xxxxxxxxxx/111`
   
   注意这样写就**不会下载评论区**的内容了!链接中如果带`?single`或`?single&comment`字段，不用管，**直接复制**进来，程序会为你下载该链接的**所有内容**！

# 3.0.在生产环境中运行

```bash
git clone https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader.git
cd Telegram_Restricted_Media_Downloader
pip install -r requirements.txt
python main.py
```



# 4.0.联系作者:

  Telegram交流群:[点击加入](https://t.me/+6KKA-buFaixmNTE1)

  Telegram:[@Gentlesprite](https://t.me/Gentlesprite)

  邮箱:Gentlesprites@outlook.com

# 5.0.支持作者:

![image](https://github.com/Gentlesprite/Telegram_Restricted_Media_Downloader/blob/main/res/pay.png)
