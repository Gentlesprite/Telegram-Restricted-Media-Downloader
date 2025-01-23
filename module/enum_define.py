# coding=UTF-8
# Author:Gentlesprite
# Software:PyCharm
# Time:2024/7/2 0:59
# File:enum_define.py
import os
import ipaddress
from enum import Enum

from module import console, log


class LinkType:
    single: str = 'single'
    group: str = 'group'
    comment: str = 'comment'

    @staticmethod
    def t(text: str) -> str:
        translation = {
            LinkType.single: '单文件',
            LinkType.group: '组文件',
            LinkType.comment: '评论区文件',
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
    def text(self) -> str:
        return {
            DownloadType.video: 'video',
            DownloadType.photo: 'photo',
            DownloadType.document: 'document'
        }[self]

    @staticmethod
    def support_type() -> list:
        return [i.text for i in DownloadType]

    @staticmethod
    def t(text: 'DownloadType.text') -> str:
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

    @property
    def text(self) -> str:
        return {
            DownloadStatus.downloading: 'downloading',
            DownloadStatus.success: 'success',
            DownloadStatus.failure: 'failure',
            DownloadStatus.skip: 'skip'
        }[self]

    @staticmethod
    def t(text: 'DownloadStatus.text', key_note: bool = False) -> str:
        translation = {
            DownloadStatus.downloading.text: '下载中',
            DownloadStatus.success.text: '成功',
            DownloadStatus.failure.text: '失败',
            DownloadStatus.skip.text: '跳过'
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


class Status:
    DOWNLOADING = DownloadStatus.t(DownloadStatus.downloading.text)
    SUCCESS = DownloadStatus.t(DownloadStatus.success.text)
    FAILURE = DownloadStatus.t(DownloadStatus.failure.text)
    SKIP = DownloadStatus.t(DownloadStatus.skip.text)


class _KeyWord:
    link: str = 'link'
    link_type: str = 'link_type'
    size: str = 'size'
    status: str = 'status'
    file: str = 'file'
    error_size: str = 'error_size'
    actual_size: str = 'actual_size'
    already_exist: str = 'already_exist'
    channel: str = 'channel'
    type: str = 'type'
    reason: str = 'reason'

    @staticmethod
    def t(text: str, key_note: bool = False) -> str:
        translation = {
            _KeyWord.link: '链接',
            _KeyWord.link_type: '链接类型',
            _KeyWord.size: '大小',
            _KeyWord.status: '状态',
            _KeyWord.file: '文件',
            _KeyWord.error_size: '错误大小',
            _KeyWord.actual_size: '实际大小',
            _KeyWord.already_exist: '已存在',
            _KeyWord.channel: '频道',
            _KeyWord.type: '类型',
            _KeyWord.reason: '原因'
        }

        if text in translation:
            if key_note:
                return f'[{translation[text]}]'
            else:
                return translation[text]
        else:
            raise ValueError(f'Unsupported Keyword:{text}')


class KeyWord:
    LINK = _KeyWord.t(_KeyWord.link, True)
    LINK_TYPE = _KeyWord.t(_KeyWord.link_type, True)
    SIZE = _KeyWord.t(_KeyWord.size, True)
    STATUS = _KeyWord.t(_KeyWord.status, True)
    FILE = _KeyWord.t(_KeyWord.file, True)
    ERROR_SIZE = _KeyWord.t(_KeyWord.error_size, True)
    ACTUAL_SIZE = _KeyWord.t(_KeyWord.actual_size, True)
    ALREADY_EXIST = _KeyWord.t(_KeyWord.already_exist, True)
    CHANNEL = _KeyWord.t(_KeyWord.channel, True)
    TYPE = _KeyWord.t(_KeyWord.type, True)
    REASON = _KeyWord.t(_KeyWord.reason, False)


class Extension:
    photo = {'image/avif': 'avif',
             'image/bmp': 'bmp',
             'image/gif': 'gif',
             'image/ief': 'ief',
             'image/jpg': 'jpg',
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
                      '#21b4f9',
                      '#33abf3',
                      '#46a1ed',
                      '#5898e8',
                      '#6b8ee2',
                      '#7d85dc',
                      '#907bd6',
                      '#a272d0',
                      '#b568ca',
                      '#c75fc5',
                      '#da55bf',
                      '#ec4cb9',
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
        """当渐变色列表小于文字长度时,翻转并扩展当前列表。"""
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
        """将十六进制颜色值转换为RGB元组。"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def __rgb_to_hex(r: int, g: int, b: int) -> str:
        """将RGB元组转换为十六进制颜色值。"""
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def generate_gradient(start_color: str, end_color: str, steps: int) -> list:
        """根据起始和结束颜色生成颜色渐变列表。"""
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


class Validator:
    @staticmethod
    def is_valid_api_id(api_id: str, valid_length: int = 32) -> bool:
        try:
            if len(api_id) < valid_length:
                if api_id.isdigit():
                    return True
                else:
                    log.warning(f'意外的参数:"{api_id}",不是「纯数字」请重新输入!')
                    return False
            else:
                log.warning(f'意外的参数,填写的"{api_id}"可能是「api_hash」,请填入正确的「api_id」!')
                return False
        except (AttributeError, TypeError):
            log.error('手动编辑config.yaml时,api_id需要有引号!')
            return False

    @staticmethod
    def is_valid_api_hash(api_hash: str, valid_length: int = 32) -> bool:
        return len(str(api_hash)) == valid_length

    @staticmethod
    def is_valid_links_file(file_path: str, valid_format: str = '.txt') -> bool:
        file_path = os.path.normpath(file_path)
        return os.path.isfile(file_path) and file_path.endswith(valid_format)

    @staticmethod
    def is_valid_save_path(save_path: str) -> bool:
        if not os.path.exists(save_path):
            while True:
                try:
                    question = console.input(f'目录:"{save_path}"不存在,是否创建? - 「y|n」(默认y):').strip().lower()
                    if question in ('y', ''):
                        os.makedirs(save_path, exist_ok=True)
                        console.log(f'成功创建目录:"{save_path}"')
                        break
                    elif question == 'n':
                        break
                    else:
                        log.warning(f'意外的参数:"{question}",支持的参数 - 「y|n」')
                except Exception as e:
                    log.error(f'意外的错误,原因:"{e}"')
                    break
        return os.path.isdir(save_path)

    @staticmethod
    def is_valid_max_download_task(max_tasks: int) -> bool:
        try:
            return int(max_tasks) > 0
        except ValueError:
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')

    @staticmethod
    def is_valid_enable_proxy(enable_proxy: str or bool) -> bool:
        if enable_proxy in ('y', 'n'):
            return True

    @staticmethod
    def is_valid_is_notice(is_notice: str) -> bool:
        if is_notice in ('y', 'n'):
            return True

    @staticmethod
    def is_valid_scheme(scheme: str, valid_format: list) -> bool:
        return scheme in valid_format

    @staticmethod
    def is_valid_hostname(hostname: str) -> bool:
        return isinstance(ipaddress.ip_address(hostname), ipaddress.IPv4Address)

    @staticmethod
    def is_valid_port(port: int) -> bool:
        try:
            return 0 < int(port) <= 65535
        except ValueError:  # 处理非整数字符串的情况
            return False
        except TypeError:  # 处理传入非数字类型的情况
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')
            return False

    @staticmethod
    def is_valid_download_type(dtype: int or str) -> bool:
        try:
            _dtype = int(dtype) if isinstance(dtype, str) else dtype
            return 0 < _dtype < 4
        except ValueError:  # 处理非整数字符串的情况
            return False
        except TypeError:  # 处理传入非数字类型的情况
            return False
        except Exception as e:
            log.error(f'意外的错误,原因:"{e}"')
            return False


class QrcodeRender:
    @staticmethod
    def render_2by1(qr_map) -> str:
        blocks_2by1: list = ['█', '▀', '▄', ' ']
        output: str = ''
        for row in range(0, len(qr_map), 2):
            for col in range(0, len(qr_map[0])):
                pixel_cur = qr_map[row][col]
                pixel_below = 1
                if row < len(qr_map) - 1:
                    pixel_below = qr_map[row + 1][col]
                pixel_encode = pixel_cur << 1 | pixel_below
                output += blocks_2by1[pixel_encode]
            output += '\n'
        return output[:-1]

    @staticmethod
    def render_3by2(qr_map) -> str:
        blocks_3by2: list = [
            '█', '🬝', '🬬', '🬎', '🬴', '🬕', '🬥', '🬆',

            '🬸', '🬙', '🬨', '🬊', '🬰', '🬒', '🬡', '🬂',

            '🬺', '🬛', '🬪', '🬌', '🬲', '▌', '🬣', '🬄',

            '🬶', '🬗', '🬧', '🬈', '🬮', '🬐', '🬟', '🬀',

            '🬻', '🬜', '🬫', '🬍', '🬳', '🬔', '🬤', '🬅',

            '🬷', '🬘', '▐', '🬉', '🬯', '🬑', '🬠', '🬁',

            '🬹', '🬚', '🬩', '🬋', '🬱', '🬓', '🬢', '🬃',

            '🬵', '🬖', '🬦', '🬇', '🬭', '🬏', '🬞', ' ',
        ]

        output: str = ''

        def get_qr_map(r, c):
            return 1 if r >= len(qr_map) or c >= len(qr_map[0]) else qr_map[r][c]

        for row in range(0, len(qr_map), 3):
            for col in range(0, len(qr_map[0]), 2):
                pixel5 = qr_map[row][col]
                pixel4 = get_qr_map(row, col + 1)
                pixel3 = get_qr_map(row + 1, col)
                pixel2 = get_qr_map(row + 1, col + 1)
                pixel1 = get_qr_map(row + 2, col)
                pixel0 = get_qr_map(row + 2, col + 1)
                pixel_encode = pixel5 << 5 | pixel4 << 4 | pixel3 << 3 | pixel2 << 2 | pixel1 << 1 | pixel0
                output += blocks_3by2[pixel_encode]
            output += '\n'

        return output[:-1]


class ProcessConfigDType:
    @staticmethod
    def set_dtype(_dtype) -> list:
        i_dtype = int(_dtype)  # 因为终端输入是字符串，这里需要转换为整数。
        if i_dtype == 1:
            return [DownloadType.video.text]
        elif i_dtype == 2:
            return [DownloadType.photo.text]
        elif i_dtype == 3:
            return [DownloadType.video.text, DownloadType.photo.text]

    @staticmethod
    def get_dtype(download_dtype: list) -> dict:
        """获取所需下载文件的类型。"""
        if DownloadType.document.text in download_dtype:
            download_dtype.remove(DownloadType.document.text)
        dt_length = len(download_dtype)
        if dt_length == 1:
            dtype: str = download_dtype[0]
            if dtype == DownloadType.video.text:
                return {'video': True, 'photo': False}
            elif dtype == DownloadType.photo.text:
                return {'video': False, 'photo': True}
        elif dt_length == 2:
            return {'video': True, 'photo': True}
        else:
            return {'error': True}


class IOGetConfigParams:
    UNDEFINED = '无'

    @staticmethod
    def get_api_id(_last_record: str) -> dict:
        while True:
            api_id = console.input(
                f'请输入「api_id」上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」:').strip()
            if api_id == '' and _last_record is not None:
                api_id = _last_record
            if Validator.is_valid_api_id(api_id):
                return {'api_id': api_id, 'record_flag': True}

    @staticmethod
    def get_api_hash(_last_record: str, _valid_length: int = 32) -> dict:
        while True:
            api_hash = console.input(
                f'请输入「api_hash」上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」:').strip().lower()
            if api_hash == '' and _last_record is not None:
                api_hash = _last_record
            if Validator.is_valid_api_hash(api_hash, _valid_length):
                return {'api_hash': api_hash, 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{api_hash}",不是一个「{_valid_length}位」的「值」!请重新输入!')

    @staticmethod
    def get_links(_last_record: str, _valid_format: str = '.txt') -> dict:
        # 输入需要下载的媒体链接文件路径,确保文件存在。
        links_file = None
        while True:
            try:
                links_file = console.input(
                    f'请输入需要下载的媒体链接的「完整路径」。上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」'
                    f'格式 - 「{_valid_format}」:').strip()
                if links_file == '' and _last_record is not None:
                    links_file = _last_record
                if Validator.is_valid_links_file(links_file, _valid_format):
                    return {'links': links_file, 'record_flag': True}
                elif not os.path.normpath(links_file).endswith('.txt'):
                    log.warning(f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,请重新输入!')
                else:
                    log.warning(
                        f'意外的参数:"{links_file}",文件路径必须以「{_valid_format}」结尾,并且「必须存在」,请重新输入!')
            except Exception as _e:
                log.error(f'意外的参数:"{links_file}",请重新输入!{KeyWord.REASON}:"{_e}"')

    @staticmethod
    def get_save_directory(_last_record) -> dict:
        # 输入媒体保存路径,确保是一个有效的目录路径。
        while True:
            save_directory = console.input(
                f'请输入媒体「保存路径」。上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」:').strip()
            if save_directory == '' and _last_record is not None:
                save_directory = _last_record
            if Validator.is_valid_save_path(save_directory):
                return {'save_directory': save_directory, 'record_flag': True}
            elif os.path.isfile(save_directory):
                log.warning(f'意外的参数:"{save_directory}",指定的路径是一个文件并非目录,请重新输入!')
            else:
                log.warning(f'意外的参数:"{save_directory}",指定的路径无效或不是一个目录,请重新输入!')

    @staticmethod
    def get_max_download_task(_last_record) -> dict:
        # 输入最大下载任务数,确保是一个整数且不超过特定限制。
        while True:
            try:
                max_download_task = console.input(
                    f'请输入「最大下载任务数」。上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」'
                    f'非会员建议默认{"(默认3)" if _last_record is None else ""}:').strip()
                if max_download_task == '' and _last_record is not None:
                    max_download_task = _last_record
                if max_download_task == '':
                    max_download_task = 3
                if Validator.is_valid_max_download_task(max_download_task):
                    return {'max_download_task': int(max_download_task), 'record_flag': True}
                else:
                    log.warning(f'意外的参数:"{max_download_task}",任务数必须是「正整数」,请重新输入!')
            except Exception as _e:
                log.error(f'意外的错误,{KeyWord.REASON}:"{_e}"')

    @staticmethod
    def get_download_type(_last_record: list or None) -> dict:

        if isinstance(_last_record, list):
            res: dict = ProcessConfigDType.get_dtype(download_dtype=_last_record)
            if len(res) == 1:
                _last_record = None
            elif res.get('video') and res.get('photo') is False:
                _last_record = 1
            elif res.get('video') is False and res.get('photo'):
                _last_record = 2
            elif res.get('video') and res.get('photo'):
                _last_record = 3

        while True:
            download_type = console.input(
                f'输入需要下载的「媒体类型」。上一次的记录是:「{_last_record if _last_record else IOGetConfigParams.UNDEFINED}」'
                f'格式 - 「1.视频 2.图片 3.视频和图片」{"(默认3)" if _last_record is None else ""}:').strip()
            if download_type == '' and _last_record is not None:
                download_type = _last_record
            if download_type == '':
                download_type = 3
            if Validator.is_valid_download_type(download_type):
                return {'download_type': ProcessConfigDType.set_dtype(_dtype=download_type), 'record_flag': True}
            else:
                log.warning(f'意外的参数:"{download_type}",支持的参数 - 「1或2或3」')

    @staticmethod
    def get_is_shutdown(_last_record: str, _valid_format: str = 'y|n') -> dict:
        if _last_record:
            _last_record = 'y'
        elif _last_record is False:
            _last_record = 'n'
        else:
            _last_record = IOGetConfigParams.UNDEFINED

        while True:
            try:
                question = console.input(
                    f'下载完成后是否「自动关机」。上一次的记录是:「{_last_record}」 - 「{_valid_format}」'
                    f'{"(默认n)" if _last_record == IOGetConfigParams.UNDEFINED else ""}:').strip().lower()
                if question == '' and _last_record != IOGetConfigParams.UNDEFINED:
                    if _last_record == 'y':
                        return {'is_shutdown': True, 'record_flag': True}

                    elif _last_record == 'n':
                        return {'is_shutdown': False, 'record_flag': True}

                elif question == 'y':
                    return {'is_shutdown': True, 'record_flag': True}
                elif question in ('n', ''):
                    return {'is_shutdown': False, 'record_flag': True}
                else:
                    log.warning(f'意外的参数:"{question}",支持的参数 - 「{_valid_format}」')

            except Exception as _e:
                log.error(f'意外的错误,{KeyWord.REASON}:"{_e}"')
