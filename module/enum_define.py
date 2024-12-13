# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 0:59
# File:enum_define.py
from enum import Enum


class LinkType(Enum):
    single = 0
    group = 1
    comment = 2

    @property
    def text(self):
        return {
            LinkType.single: 'single',
            LinkType.group: 'group',
            LinkType.comment: 'comment',
        }[self]

    @staticmethod
    def translate(text: 'LinkType.text'):
        translation = {
            LinkType.single.text: '单文件',
            LinkType.group.text: '组文件',
            LinkType.comment.text: '评论文件',
        }
        if text in translation:
            return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class DownloadType(Enum):
    video = 0
    photo = 1
    document = 2

    @property
    def text(self):
        return {
            DownloadType.video: 'video',
            DownloadType.photo: 'photo',
            DownloadType.document: 'document'
        }[self]

    @staticmethod
    def support_type() -> list:
        return [i.text for i in DownloadType]

    @staticmethod
    def translate(text: 'DownloadType.text'):
        translation = {
            DownloadType.video.text: '视频',
            DownloadType.photo.text: '图片',
            DownloadType.document.text: '文档'
        }
        if text in translation:
            return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class DownloadStatus(Enum):
    downloading = 0
    success = 1
    failure = 2
    skip = 3
    all_complete = 4

    @property
    def text(self):
        return {
            DownloadStatus.downloading: 'downloading',
            DownloadStatus.success: 'success',
            DownloadStatus.failure: 'failure',
            DownloadStatus.skip: 'skip'
        }[self]

    @staticmethod
    def translate(text: 'DownloadStatus.text', key_note: bool = False):
        translation = {
            DownloadStatus.downloading.text: '正在下载',
            DownloadStatus.success.text: '成功下载',
            DownloadStatus.failure.text: '失败下载',
            DownloadStatus.skip.text: '跳过下载'
        }
        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')

    @staticmethod
    def all_status() -> list:
        return [i.text for i in DownloadStatus]


class KeyWorld(Enum):
    link = 0
    link_type = 1
    id = 2
    size = 3
    status = 4
    file = 5
    error_size = 6
    actual_size = 7
    already_exist = 8
    chanel = 9
    type = 10
    download_task_error = 11

    @property
    def text(self):
        return {
            KeyWorld.link: 'link',
            KeyWorld.link_type: 'link_type',
            KeyWorld.id: 'id',
            KeyWorld.size: 'size',
            KeyWorld.status: 'status',
            KeyWorld.file: 'file',
            KeyWorld.error_size: 'error_size',
            KeyWorld.actual_size: 'actual_size',
            KeyWorld.already_exist: 'already_exist',
            KeyWorld.chanel: 'chanel',
            KeyWorld.type: 'type',
            KeyWorld.download_task_error: 'download_task_error'
        }[self]

    @staticmethod
    def translate(text: 'KeyWorld.text', key_note: bool = False):
        translation = {
            KeyWorld.link.text: '链接',
            KeyWorld.link_type.text: '链接类型',
            KeyWorld.id.text: '标识',
            KeyWorld.size.text: '大小',
            KeyWorld.status.text: '状态',
            KeyWorld.file.text: '文件',
            KeyWorld.error_size.text: '错误大小',
            KeyWorld.actual_size.text: '实际大小',
            KeyWorld.already_exist.text: '已存在',
            KeyWorld.chanel.text: '频道',
            KeyWorld.type.text: '类型',
            KeyWorld.download_task_error.text: '下载任务错误'
        }

        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class Extension:
    photo = {'image/avif': 'avif',
             'image/bmp': 'bmp',
             'image/gif': 'gif',
             'image/ief': 'ief',
             'image/jpeg': 'jpeg',
             'image/heic': 'heic',
             'image/heif': 'heif',
             'image/png': 'png',
             'image/svg+xml': 'svg',
             'image/tiff': 'tif',
             'image/vnd.microsoft.icon': 'ico',
             'image/x-cmu-raster': 'ras',
             'image/x-portable-anymap': 'pnm',
             'image/x-portable-bitmap': 'pbm',
             'image/x-portable-graymap': 'pgm',
             'image/x-portable-pixmap': 'ppm',
             'image/x-rgb': 'rgb',
             'image/x-xbitmap': 'xbm',
             'image/x-xpixmap': 'xpm',
             'image/x-xwindowdump': 'xwd'}
    video = {'video/mp4': 'mp4',
             'video/mpeg': 'mpg',
             'video/quicktime': 'qt',
             'video/webm': 'webm',
             'video/x-msvideo': 'avi',
             'video/x-sgi-movie': 'movie',
             'video/x-matroska': 'mkv'}


class GradientColor:
    blue_to_purple = ['#0ebeff',
                      '#22b4f9',
                      '#36a9f2',
                      '#4a9fec',
                      '#5e95e6',
                      '#728adf',
                      '#8780d9',
                      '#9b76d3',
                      '#af6bcc',
                      '#c361c6',
                      '#d757c0',
                      '#eb4cb9',
                      '#ff42b3']
    green_to_pink = ['#00ff40',
                     '#14f54c',
                     '#29eb58',
                     '#3de064',
                     '#52d670',
                     '#66cc7c',
                     '#7ac288',
                     '#8fb894',
                     '#a3ada0',
                     '#b8a3ac',
                     '#cc99b8']
    green_to_blue = ['#84fab0',
                     '#85f6b8',
                     '#86f1bf',
                     '#88edc7',
                     '#89e9ce',
                     '#8ae4d6',
                     '#8be0dd',
                     '#8ddce5',
                     '#8ed7ec',
                     '#8fd3f4']
    yellow_to_green = ['#d4fc79',
                       '#cdfa7d',
                       '#c6f782',
                       '#bff586',
                       '#b8f28b',
                       '#b2f08f',
                       '#abed94',
                       '#a4eb98',
                       '#9de89d',
                       '#96e6a1']
    new_life = ['#43e97b',
                '#42eb85',
                '#41ed8f',
                '#3fee9a',
                '#3ef0a4',
                '#3df2ae',
                '#3cf4b8',
                '#3af5c3',
                '#39f7cd',
                '#38f9d7']

    @staticmethod
    def __extend_gradient_colors(colors: list, target_length: int) -> list:
        extended_colors = colors[:]
        while len(extended_colors) < target_length:
            # 添加原列表（除最后一个元素外）的逆序
            extended_colors.extend(colors[-2::-1])
            # 如果仍然不够长，继续添加正序部分
            if len(extended_colors) < target_length:
                extended_colors.extend(colors[:-1])
        return extended_colors[:target_length]

    @staticmethod
    def gen_gradient_text(text: str, gradient_color: list) -> str:
        """当渐变色列表小于文字长度时,翻转并扩展当前列表"""
        text_lst: list = [i for i in text]
        text_lst_len: int = len(text_lst)
        gradient_color_len: int = len(gradient_color)
        if text_lst_len > gradient_color_len:
            # 扩展颜色列表以适应文本长度
            gradient_color = GradientColor.__extend_gradient_colors(gradient_color, text_lst_len)
        result: str = ''
        for i in range(text_lst_len):
            result += f'[{gradient_color[i]}]{text_lst[i]}[/{gradient_color[i]}]'
        return result

    @staticmethod
    def __hex_to_rgb(hex_color: str) -> tuple:
        """将十六进制颜色值转换为RGB元组"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def __rgb_to_hex(r: int, g: int, b: int) -> str:
        """将RGB元组转换为十六进制颜色值"""
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def generate_gradient(start_color: str, end_color: str, steps: int) -> list:
        """根据起始和结束颜色生成颜色渐变列表"""
        steps = 2 if steps <= 1 else steps
        # 转换起始和结束颜色为RGB
        start_rgb = GradientColor.__hex_to_rgb(start_color)
        end_rgb = GradientColor.__hex_to_rgb(end_color)
        # 生成渐变色列表
        gradient_color: list = []
        for i in range(steps):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (steps - 1))
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (steps - 1))
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (steps - 1))
            gradient_color.append(GradientColor.__rgb_to_hex(r, g, b))

        return gradient_color


class ArtFont:
    author_art_1 = r'''
       ______           __  __                     _ __          
      / ____/__  ____  / /_/ /__  _________  _____(_) /____      
     / / __/ _ \/ __ \/ __/ / _ \/ ___/ __ \/ ___/ / __/ _ \     
    / /_/ /  __/ / / / /_/ /  __(__  ) /_/ / /  / / /_/  __/     
    \____/\___/_/ /_/\__/_/\___/____/ .___/_/  /_/\__/\___/      
                                   /_/                           
        '''
    author_art_2 = r'''
    ╔═╗┌─┐┌┐┌┌┬┐┬  ┌─┐┌─┐┌─┐┬─┐┬┌┬┐┌─┐  
    ║ ╦├┤ │││ │ │  ├┤ └─┐├─┘├┬┘│ │ ├┤   
    ╚═╝└─┘┘└┘ ┴ ┴─┘└─┘└─┘┴  ┴└─┴ ┴ └─┘  
        '''
    author_art_3 = r'''
     ██████╗ ███████╗███╗   ██╗████████╗██╗     ███████╗███████╗██████╗ ██████╗ ██╗████████╗███████╗    
    ██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██║     ██╔════╝██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝    
    ██║  ███╗█████╗  ██╔██╗ ██║   ██║   ██║     █████╗  ███████╗██████╔╝██████╔╝██║   ██║   █████╗      
    ██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██║     ██╔══╝  ╚════██║██╔═══╝ ██╔══██╗██║   ██║   ██╔══╝      
    ╚██████╔╝███████╗██║ ╚████║   ██║   ███████╗███████╗███████║██║     ██║  ██║██║   ██║   ███████╗    
     ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝           
            '''
    author_art_4 = r'''                                                                          
                                        ,,                                       ,,                    
  .g8"""bgd                      mm   `7MM                                       db   mm               
.dP'     `M                      MM     MM                                            MM               
dM'       `   .gP"Ya `7MMpMMMb.mmMMmm   MM  .gP"Ya  ,pP"Ybd `7MMpdMAo.`7Mb,od8 `7MM mmMMmm .gP"Ya      
MM           ,M'   Yb  MM    MM  MM     MM ,M'   Yb 8I   `"   MM   `Wb  MM' "'   MM   MM  ,M'   Yb     
MM.    `7MMF'8M""""""  MM    MM  MM     MM 8M"""""" `YMMMa.   MM    M8  MM       MM   MM  8M""""""     
`Mb.     MM  YM.    ,  MM    MM  MM     MM YM.    , L.   I8   MM   ,AP  MM       MM   MM  YM.    ,     
  `"bmmmdPY   `Mbmmd'.JMML  JMML.`Mbmo.JMML.`Mbmmd' M9mmmP'   MMbmmd' .JMML.   .JMML. `Mbmo`Mbmmd'     
                                                              MM                                       
                                                            .JMML.                                     
    '''
