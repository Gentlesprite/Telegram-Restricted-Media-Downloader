# coding=UTF-8
# Author:wang_pc, Yihang Liu
# Software:PyCharm
# Time:2024/8/20 21:56
# File:qrterm.py
"""
@author: 'wang_pc', 'Yihang Liu'
@site:
@file: qrterm.py
@time: 2017/2/10 16:38
感谢作者代码
"""
import qrcode


def render_2by1(qr_map):
    BLOCKS = ['█', '▀', '▄', ' ']
    output = ""
    for row in range(0, len(qr_map), 2):
        for col in range(0, len(qr_map[0])):
            pixel_cur = qr_map[row][col]
            pixel_below = 1
            if row < len(qr_map) - 1:
                pixel_below = qr_map[row + 1][col]
            pixel_encode = pixel_cur << 1 | pixel_below
            output += BLOCKS[pixel_encode]
        output += '\n'
    return output[:-1]


def render_3by2(qr_map):
    BLOCKS = [
        '█', '🬝', '🬬', '🬎', '🬴', '🬕', '🬥', '🬆',

        '🬸', '🬙', '🬨', '🬊', '🬰', '🬒', '🬡', '🬂',

        '🬺', '🬛', '🬪', '🬌', '🬲', '▌', '🬣', '🬄',

        '🬶', '🬗', '🬧', '🬈', '🬮', '🬐', '🬟', '🬀',

        '🬻', '🬜', '🬫', '🬍', '🬳', '🬔', '🬤', '🬅',

        '🬷', '🬘', '▐', '🬉', '🬯', '🬑', '🬠', '🬁',

        '🬹', '🬚', '🬩', '🬋', '🬱', '🬓', '🬢', '🬃',

        '🬵', '🬖', '🬦', '🬇', '🬭', '🬏', '🬞', ' ',
    ]

    output = ""

    def get_qrmap(r, c):
        return 1 if r >= len(qr_map) or c >= len(qr_map[0]) else qr_map[r][c]

    for row in range(0, len(qr_map), 3):
        for col in range(0, len(qr_map[0]), 2):
            pixel5 = qr_map[row][col]
            pixel4 = get_qrmap(row, col + 1)
            pixel3 = get_qrmap(row + 1, col)
            pixel2 = get_qrmap(row + 1, col + 1)
            pixel1 = get_qrmap(row + 2, col)
            pixel0 = get_qrmap(row + 2, col + 1)
            pixel_encode = pixel5 << 5 | pixel4 << 4 | pixel3 << 3 | pixel2 << 2 | pixel1 << 1 | pixel0
            output += BLOCKS[pixel_encode]
        output += '\n'

    return output[:-1]


def qr_terminal_str(_str, version=1, render=render_2by1):
    qr = qrcode.QRCode(version)
    qr.add_data(_str)
    qr.make()
    qr_map = []
    qr_row = len(qr.modules) + 2
    qr_col = len(qr.modules[0]) + 2
    qr_map = [[False for _ in range(qr_col)] for _ in range(qr_row)]
    for row_id, row in enumerate(qr.modules):
        for col_id, pixel in enumerate(row):
            qr_map[row_id + 1][col_id + 1] = pixel
    return render(qr_map)


def draw(_str, version=1, render=render_2by1):
    output = qr_terminal_str(_str, version=version, render=render)
    return output
