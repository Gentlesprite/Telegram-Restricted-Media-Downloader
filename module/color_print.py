# coding=UTF-8
# Author:DanGill
# Software:PyCharm
# Time:2024/7/25 12:32
# File:color_print
import sys
import platform

colors =   [["Black","000000"],
            ["Maroon","800000"],
            ["Green","008000"],
            ["Olive","808000"],
            ["Navy","000080"],
            ["Purple","800080"],
            ["Teal","008080"],
            ["Silver","c0c0c0"],
            ["Grey","808080"],
            ["Red","ff0000"],
            ["Lime","00ff00"],
            ["Yellow","ffff00"],
            ["Blue","0000ff"],
            ["Fuchsia","ff00ff"],
            ["Aqua","00ffff"],
            ["White","ffffff"],
            ["Grey0","000000"],
            ["NavyBlue","00005f"],
            ["DarkBlue","000087"],
            ["Blue3","0000af"],
            ["Blue3","0000d7"],
            ["Blue1","0000ff"],
            ["DarkGreen","005f00"],
            ["DeepSkyBlue4","005f5f"],
            ["DeepSkyBlue4","005f87"],
            ["DeepSkyBlue4","005faf"],
            ["DodgerBlue3","005fd7"],
            ["DodgerBlue2","005fff"],
            ["Green4","008700"],
            ["SpringGreen4","00875f"],
            ["Turquoise4","008787"],
            ["DeepSkyBlue3","0087af"],
            ["DeepSkyBlue3","0087d7"],
            ["DodgerBlue1","0087ff"],
            ["Green3","00af00"],
            ["SpringGreen3","00af5f"],
            ["DarkCyan","00af87"],
            ["LightSeaGreen","00afaf"],
            ["DeepSkyBlue2","00afd7"],
            ["DeepSkyBlue1","00afff"],
            ["Green3","00d700"],
            ["SpringGreen3","00d75f"],
            ["SpringGreen2","00d787"],
            ["Cyan3","00d7af"],
            ["DarkTurquoise","00d7d7"],
            ["Turquoise2","00d7ff"],
            ["Green1","00ff00"],
            ["SpringGreen2","00ff5f"],
            ["SpringGreen1","00ff87"],
            ["MediumSpringGreen","00ffaf"],
            ["Cyan2","00ffd7"],
            ["Cyan1","00ffff"],
            ["DarkRed","5f0000"],
            ["DeepPink4","5f005f"],
            ["Purple4","5f0087"],
            ["Purple4","5f00af"],
            ["Purple3","5f00d7"],
            ["BlueViolet","5f00ff"],
            ["Orange4","5f5f00"],
            ["Grey37","5f5f5f"],
            ["MediumPurple4","5f5f87"],
            ["SlateBlue3","5f5faf"],
            ["SlateBlue3","5f5fd7"],
            ["RoyalBlue1","5f5fff"],
            ["Chartreuse4","5f8700"],
            ["DarkSeaGreen4","5f875f"],
            ["PaleTurquoise4","5f8787"],
            ["SteelBlue","5f87af"],
            ["SteelBlue3","5f87d7"],
            ["CornflowerBlue","5f87ff"],
            ["Chartreuse3","5faf00"],
            ["DarkSeaGreen4","5faf5f"],
            ["CadetBlue","5faf87"],
            ["CadetBlue","5fafaf"],
            ["SkyBlue3","5fafd7"],
            ["SteelBlue1","5fafff"],
            ["Chartreuse3","5fd700"],
            ["PaleGreen3","5fd75f"],
            ["SeaGreen3","5fd787"],
            ["Aquamarine3","5fd7af"],
            ["MediumTurquoise","5fd7d7"],
            ["SteelBlue1","5fd7ff"],
            ["Chartreuse2","5fff00"],
            ["SeaGreen2","5fff5f"],
            ["SeaGreen1","5fff87"],
            ["SeaGreen1","5fffaf"],
            ["Aquamarine1","5fffd7"],
            ["DarkSlateGray2","5fffff"],
            ["DarkRed","870000"],
            ["DeepPink4","87005f"],
            ["DarkMagenta","870087"],
            ["DarkMagenta","8700af"],
            ["DarkViolet","8700d7"],
            ["Purple","8700ff"],
            ["Orange4","875f00"],
            ["LightPink4","875f5f"],
            ["Plum4","875f87"],
            ["MediumPurple3","875faf"],
            ["MediumPurple3","875fd7"],
            ["SlateBlue1","875fff"],
            ["Yellow4","878700"],
            ["Wheat4","87875f"],
            ["Grey53","878787"],
            ["LightSlateGrey","8787af"],
            ["MediumPurple","8787d7"],
            ["LightSlateBlue","8787ff"],
            ["Yellow4","87af00"],
            ["DarkOliveGreen3","87af5f"],
            ["DarkSeaGreen","87af87"],
            ["LightSkyBlue3","87afaf"],
            ["LightSkyBlue3","87afd7"],
            ["SkyBlue2","87afff"],
            ["Chartreuse2","87d700"],
            ["DarkOliveGreen3","87d75f"],
            ["PaleGreen3","87d787"],
            ["DarkSeaGreen3","87d7af"],
            ["DarkSlateGray3","87d7d7"],
            ["SkyBlue1","87d7ff"],
            ["Chartreuse1","87ff00"],
            ["LightGreen","87ff5f"],
            ["LightGreen","87ff87"],
            ["PaleGreen1","87ffaf"],
            ["Aquamarine1","87ffd7"],
            ["DarkSlateGray1","87ffff"],
            ["Red3","af0000"],
            ["DeepPink4","af005f"],
            ["MediumVioletRed","af0087"],
            ["Magenta3","af00af"],
            ["DarkViolet","af00d7"],
            ["Purple","af00ff"],
            ["DarkOrange3","af5f00"],
            ["IndianRed","af5f5f"],
            ["HotPink3","af5f87"],
            ["MediumOrchid3","af5faf"],
            ["MediumOrchid","af5fd7"],
            ["MediumPurple2","af5fff"],
            ["DarkGoldenrod","af8700"],
            ["LightSalmon3","af875f"],
            ["RosyBrown","af8787"],
            ["Grey63","af87af"],
            ["MediumPurple2","af87d7"],
            ["MediumPurple1","af87ff"],
            ["Gold3","afaf00"],
            ["DarkKhaki","afaf5f"],
            ["NavajoWhite3","afaf87"],
            ["Grey69","afafaf"],
            ["LightSteelBlue3","afafd7"],
            ["LightSteelBlue","afafff"],
            ["Yellow3","afd700"],
            ["DarkOliveGreen3","afd75f"],
            ["DarkSeaGreen3","afd787"],
            ["DarkSeaGreen2","afd7af"],
            ["LightCyan3","afd7d7"],
            ["LightSkyBlue1","afd7ff"],
            ["GreenYellow","afff00"],
            ["DarkOliveGreen2","afff5f"],
            ["PaleGreen1","afff87"],
            ["DarkSeaGreen2","afffaf"],
            ["DarkSeaGreen1","afffd7"],
            ["PaleTurquoise1","afffff"],
            ["Red3","d70000"],
            ["DeepPink3","d7005f"],
            ["DeepPink3","d70087"],
            ["Magenta3","d700af"],
            ["Magenta3","d700d7"],
            ["Magenta2","d700ff"],
            ["DarkOrange3","d75f00"],
            ["IndianRed","d75f5f"],
            ["HotPink3","d75f87"],
            ["HotPink2","d75faf"],
            ["Orchid","d75fd7"],
            ["MediumOrchid1","d75fff"],
            ["Orange3","d78700"],
            ["LightSalmon3","d7875f"],
            ["LightPink3","d78787"],
            ["Pink3","d787af"],
            ["Plum3","d787d7"],
            ["Violet","d787ff"],
            ["Gold3","d7af00"],
            ["LightGoldenrod3","d7af5f"],
            ["Tan","d7af87"],
            ["MistyRose3","d7afaf"],
            ["Thistle3","d7afd7"],
            ["Plum2","d7afff"],
            ["Yellow3","d7d700"],
            ["Khaki3","d7d75f"],
            ["LightGoldenrod2","d7d787"],
            ["LightYellow3","d7d7af"],
            ["Grey84","d7d7d7"],
            ["LightSteelBlue1","d7d7ff"],
            ["Yellow2","d7ff00"],
            ["DarkOliveGreen1","d7ff5f"],
            ["DarkOliveGreen1","d7ff87"],
            ["DarkSeaGreen1","d7ffaf"],
            ["Honeydew2","d7ffd7"],
            ["LightCyan1","d7ffff"],
            ["Red1","ff0000"],
            ["DeepPink2","ff005f"],
            ["DeepPink1","ff0087"],
            ["DeepPink1","ff00af"],
            ["Magenta2","ff00d7"],
            ["Magenta1","ff00ff"],
            ["OrangeRed1","ff5f00"],
            ["IndianRed1","ff5f5f"],
            ["IndianRed1","ff5f87"],
            ["HotPink","ff5faf"],
            ["HotPink","ff5fd7"],
            ["MediumOrchid1","ff5fff"],
            ["DarkOrange","ff8700"],
            ["Salmon1","ff875f"],
            ["LightCoral","ff8787"],
            ["PaleVioletRed1","ff87af"],
            ["Orchid2","ff87d7"],
            ["Orchid1","ff87ff"],
            ["Orange1","ffaf00"],
            ["SandyBrown","ffaf5f"],
            ["LightSalmon1","ffaf87"],
            ["LightPink1","ffafaf"],
            ["Pink1","ffafd7"],
            ["Plum1","ffafff"],
            ["Gold1","ffd700"],
            ["LightGoldenrod2","ffd75f"],
            ["LightGoldenrod2","ffd787"],
            ["NavajoWhite1","ffd7af"],
            ["MistyRose1","ffd7d7"],
            ["Thistle1","ffd7ff"],
            ["Yellow1","ffff00"],
            ["LightGoldenrod1","ffff5f"],
            ["Khaki1","ffff87"],
            ["Wheat1","ffffaf"],
            ["Cornsilk1","ffffd7"],
            ["Grey100","ffffff"],
            ["Grey3","080808"],
            ["Grey7","121212"],
            ["Grey11","1c1c1c"],
            ["Grey15","262626"],
            ["Grey19","303030"],
            ["Grey23","3a3a3a"],
            ["Grey27","444444"],
            ["Grey30","4e4e4e"],
            ["Grey35","585858"],
            ["Grey39","626262"],
            ["Grey42","6c6c6c"],
            ["Grey46","767676"],
            ["Grey50","808080"],
            ["Grey54","8a8a8a"],
            ["Grey58","949494"],
            ["Grey62","9e9e9e"],
            ["Grey66","a8a8a8"],
            ["Grey70","b2b2b2"],
            ["Grey74","bcbcbc"],
            ["Grey78","c6c6c6"],
            ["Grey82","d0d0d0"],
            ["Grey85","dadada"],
            ["Grey89","e4e4e4"],
            ["Grey93","eeeeee"]]

if platform.system().lower() == 'windows':
    from ctypes import windll, c_int, byref

    stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
    mode = c_int(0)
    windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
    mode = c_int(mode.value | 4)
    windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)

orignialprint = print


def print(*args, color=None, bcolor=None, sep=" ", **kwargs):
    if len(args) == 1:
        string = str(args[0])
    else:
        string = sep.join(list(map(str, args)))

    if "idlelib.run" in sys.modules:
        orignialprint(string, **kwargs)
    else:
        colorIsHex, bcolorIsHex = 0, 0
        if color != None:
            if color[0] == "#":
                color = color[1:]
                colorIsHex = 1
            for i in range(len(colors)):
                if colors[i][colorIsHex].lower() == color.lower():
                    code = (u"\u001b[38;5;" + str(i) + u"m")
        else:
            code = ""

        if bcolor != None:
            if bcolor[0] == "#":
                bcolor = bcolor[1:]
                bcolorIsHex = 1
            for i in range(len(colors)):
                if colors[i][bcolorIsHex].lower() == bcolor.lower():
                    bcode = (u"\u001b[48;5;" + str(i) + u"m")
        else:
            bcode = ""

        reset = u"\u001b[0m"
        orignialprint(bcode, code, string, reset, sep="", **kwargs)


def rainbow(*args, sep=" ", end="\n", **kwargs):
    if len(args) == 1:
        string = args[0]
    else:
        string = sep.join(list(map(str, args)))

    if "idlelib.run" in sys.modules:
        orignialprint(string, end=end, **kwargs)
    else:
        mainColors = [colors[1], colors[2], colors[3], colors[4], colors[5], colors[6], colors[7], colors[8], colors[9],
                      colors[10], colors[11], colors[12], colors[13], colors[14]]
        for i in range(len(string)):
            print(string[i], color=mainColors[i % len(mainColors)][0], sep="", end="", **kwargs)
        print("", end=end)


def demo(showHex=False, showBColor=False):
    if showHex == True:
        space = str(20)
        smallSpace = str(8)
        for color1, color2, color3, color4 in zip(*[iter(colors)] * 4):
            print(("{:<" + smallSpace + "}").format("#" + color1[1]), color=color1[0], sep="", end="")
            print(("{:<" + space + "}").format(color1[0]), color=color1[0], sep="", end="")
            print(("{:<" + smallSpace + "}").format("#" + color2[1]), color=color2[0], sep="", end="")
            print(("{:<" + space + "}").format(color2[0]), color=color2[0], sep="", end="")
            print(("{:<" + smallSpace + "}").format("#" + color3[1]), color=color3[0], sep="", end="")
            print(("{:<" + space + "}").format(color3[0]), color=color3[0], sep="", end="")
            print(("{:<" + smallSpace + "}").format("#" + color4[1]), color=color4[0], sep="", end="")
            print(("{:<" + space + "}").format(color4[0]), color=color4[0], sep="", end="\n")
            if showBColor == True:
                print(("{:<" + smallSpace + "}").format("#" + color1[1]), bcolor=color1[0], sep="", end="")
                print(("{:<" + space + "}").format(color1[0]), bcolor=color1[0], sep="", end="")
                print(("{:<" + smallSpace + "}").format("#" + color2[1]), bcolor=color2[0], sep="", end="")
                print(("{:<" + space + "}").format(color2[0]), bcolor=color2[0], sep="", end="")
                print(("{:<" + smallSpace + "}").format("#" + color3[1]), bcolor=color3[0], sep="", end="")
                print(("{:<" + space + "}").format(color3[0]), bcolor=color3[0], sep="", end="")
                print(("{:<" + smallSpace + "}").format("#" + color4[1]), bcolor=color4[0], sep="", end="")
                print(("{:<" + space + "}").format(color4[0]), bcolor=color4[0], sep="", end="\n\n")

    else:
        space = str(20)
        for color1, color2, color3, color4 in zip(*[iter(colors)] * 4):
            print(("{:<" + space + "}").format(color1[0]), color=color1[0], sep="", end="")
            print(("{:<" + space + "}").format(color2[0]), color=color2[0], sep="", end="")
            print(("{:<" + space + "}").format(color3[0]), color=color3[0], sep="", end="")
            print(("{:<" + space + "}").format(color4[0]), color=color4[0], sep="", end="\n")
            if showBColor == True:
                print(("{:<" + space + "}").format(color1[0]), bcolor=color1[0], sep="", end="")
                print(("{:<" + space + "}").format(color2[0]), bcolor=color2[0], sep="", end="")
                print(("{:<" + space + "}").format(color3[0]), bcolor=color3[0], sep="", end="")
                print(("{:<" + space + "}").format(color4[0]), bcolor=color4[0], sep="", end="\n\n")

