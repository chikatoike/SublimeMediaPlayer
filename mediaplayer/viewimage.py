# -*- coding: utf-8 -*-
import pyglet

# def color_code_from_str(rgba):
#     return '#%02X%02X%02X%02X' % (ord(rgba[0]), ord(rgba[1]), ord(rgba[2]), ord(rgba[3]))


def color_code(color):
    rgba = [
        (color >> 24) & 0xff,
        (color >> 16) & 0xff,
        (color >> 8) & 0xff,
        color & 0xff,
        ]
    # return '#%02X%02X%02X%02X' % (rgba[0], rgba[1], rgba[2], rgba[3])
    return '#%02X%02X%02X' % (rgba[0], rgba[1], rgba[2])


def color_int(rgba):
    return (
        ord(rgba[0]) << 24 |
        ord(rgba[1]) << 16 |
        ord(rgba[2]) << 8 |
        ord(rgba[3]))


def color_int_cut(rgba):
    return (
        (ord(rgba[0]) & 0xf0) << 24 |
        (ord(rgba[1]) & 0xf0) << 16 |
        (ord(rgba[2]) & 0xf0) << 8)


def image2intarray(img, width, height, cut_color, xstep=2, ystep=2):
    w = width / xstep
    h = height / xstep
    a = [0] * (w * h)
    if cut_color:
        for i in xrange(width * height):
            a[i] = color_int_cut(img[(i * 4):(i * 4 + 4)])
    else:
        for y in xrange(h):
            for x in xrange(w):
                i = (x * xstep) + (y * ystep * width)
                a[x + y * w] = color_int(img[(i * 4):(i * 4 + 4)])
    return a


def create_color_table(data, width, height, table=None):
    # def generate_chars():
    #     chars = u"　あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ"
    #     # chars = " 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #     # chars = " !\"#$%'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    #     for c in chars:
    #         yield c
    def generate_chars():
        for c in xrange(0x4E00, 0x4E00 + 512):  # CJK Unified Ideographs ~
        # for c in xrange(0x4E00, 0x9FCF + 1):  # CJK Unified Ideographs
        # for c in xrange(0x3042, 0x3042 + 50):  # hiragana
        # for c in xrange(0x3400, 0x4DBF + 1):  # CJK Unified Ideographs Extension A
        # for c in xrange(0x20000, 0x2A6DF + 1):  # CJK Unified Ideographs Extension B
        # for c in xrange(0x2A700, 0x2B73F + 1):  # CJK Unified Ideographs Extension C
        # for c in xrange(0x2B740, 0x2B81F + 1):  # CJK Unified Ideographs Extension D
            yield unichr(c)
            # yield ("\U" + "%08x" % c).decode("unicode-escape")

    if table is None:
        table = {}
    g = generate_chars()
    try:
        for i in xrange(width * height):
            color = data[i]
            if color not in table:
                table[color] = g.next()
    except StopIteration:
        # Incomplete
        pass
    return table


def generate_image_theme(table):
    template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>name</key>
    <string>MediaPlayerImage</string>
    <key>settings</key>
    <array>
        <dict>
            <key>settings</key>
            <dict>
                <key>background</key>
                <string>#272822</string>
                <key>caret</key>
                <string>#F8F8F0</string>
                <key>foreground</key>
                <string>#F8F8F2</string>
            </dict>
        </dict>

        <dict>
            <key>name</key>
            <string>color1</string>
            <key>scope</key>
            <string>color1</string>
            <key>settings</key>
            <dict>
              <key>foreground</key>
              <string>#FF0000</string>
              <key>background</key>
              <string>#FF0000</string>
           </dict>
        </dict>
        %s
    </array>
    <key>uuid</key>
    <string>8C10E5DC-F518-4C7C-85F7-FA9F45333415</string>
</dict>
</plist>
"""
    color_def = """
        <dict>
            <key>name</key>
            <string>%(color)s</string>
            <key>scope</key>
            <string>%(color)s</string>
            <key>settings</key>
            <dict>
              <key>foreground</key>
              <string>%(color)s</string>
              <key>background</key>
              <string>%(color)s</string>
           </dict>
        </dict>"""
    colors = [
        color_def % {'color': color_code(color)}
        for color in table.keys()
        ]
    return template % (''.join(colors))


def generate_image_syntax(table):
    template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>fileTypes</key>
    <array>
        <string></string>
    </array>
    <key>name</key>
    <string>MediaPlayerImage</string>
    <key>patterns</key>
    <array>
        <dict>
            <key>comment</key>
            <string> </string>
            <key>match</key>
            <string>A</string>
            <key>name</key>
            <string>color1</string>
        </dict>
        %s
    </array>
    <key>scopeName</key>
    <string>source.media_player_image</string>
    <key>uuid</key>
    <string>41627401-ecbe-4a7b-b86a-1fd04f967d93</string>
</dict>
</plist>
"""
    color_def = """
        <dict>
            <key>comment</key>
            <string> </string>
            <key>match</key>
            <string>%(char)s</string>
            <key>name</key>
            <string>%(color)s</string>
        </dict>"""
    colors = [
        color_def % {
            'color': color_code(color),
            'char': char
            # 'char': "\\x{%x}" % ord(char)
            }
        for color, char in table.items()
        ]
    return template % (''.join(colors))


class Image(object):
    def __init__(self, filename=None, image=None, cut_color=True):
        if filename is not None:
            img = pyglet.image.load(filename).get_image_data()
        elif image is not None:
            img = image
        else:
            return
        scale = self.image_scale(img.width, img.height)
        self.data = image2intarray(img.get_data('RGBA', img.width * 4), img.width, img.height, cut_color, scale, scale)
        self.width = img.width / scale
        self.height = img.height / scale
        print('mediaplayer: image width = ' + str(self.width) + ' height = ' + str(self.height))

    def get_image_for_view(self, id):
        table = create_color_table(self.data, self.width, self.height)
        print('mediaplayer: image color count = ' + str(len(table)))
        return {
            'content': self.image2text(table),
            'theme': generate_image_theme(table),
            'syntax': generate_image_syntax(table),
            'theme_file': 'MediaPlayer %d.tmTheme' % (id),
            'syntax_file': 'MediaPlayer %d.tmLanguage' % (id),
            }

    def image2text(self, table, blank=' '):
        text = []
        for y in xrange(self.height):
            for x in xrange(self.width):
                color = self.data[x + y * self.width]
                text.append(table.get(color, blank))
            text.append('\n')
        return ''.join(reversed(text))

    def image_scale(self, width, height):
        w = 200
        h = 200
        if width <= w:
            w2 = 1
        else:
            w2 = (width / w)
        if height <= h:
            h2 = 1
        else:
            h2 = (height / h)
        return max(w2, h2)


class Animation(object):
    def __init__(self, filename):
        animation = pyglet.image.load_animation(filename)
        self.frames = [
            {
                'image': Image(image=frame.image, cut_color=False),
                'duration': frame.duration
            }
            for frame in animation.frames]

    def get_image_for_view(self, id):
        table = {}
        frames = []
        for frame in self.frames:
            img = frame['image']
            table = create_color_table(img.data, img.width, img.height, table)
            frames.append({'content': img.image2text(table), 'duration': frame['duration']})
            print('mediaplayer: image color count = ' + str(len(table)))
        return {
            'frames': frames,
            'theme': generate_image_theme(table),
            'syntax': generate_image_syntax(table),
            'theme_file': 'MediaPlayer %d.tmTheme' % (id),
            'syntax_file': 'MediaPlayer %d.tmLanguage' % (id),
            }
