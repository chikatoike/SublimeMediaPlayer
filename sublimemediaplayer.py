# -*- coding: utf-8 -*-
import os
import sys
import time
import codecs
import sublime
import sublime_plugin

package_dir = os.getcwd()

# required for import pyglet
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())


stop = False


def play_animation(view, frames):
    global stop
    stop = False

    def frame_gen():
        while True:
            for i, f in enumerate(frames):
                yield i, f
    g = frame_gen()

    def update():
        i, frame = g.next()
        print 'mediaplayer: update ' + str(i)
        view.run_command('media_player_replace', {"characters": frame['content']})
        if not stop and view.window() is not None:
            sublime.set_timeout(update, int(frame['duration'] * 1000))

    sublime.set_timeout(update, 0)


class MediaPlayerPlayGifCommand(sublime_plugin.WindowCommand):
    def run(self, file_name=None):
        if file_name is None:
            self.window.show_input_panel("MediaPlayer: GIF file:", "", self.on_done, None, None)
        else:
            self.on_done(file_name)

    def on_done(self, file_name):
        self.window.run_command('new_file')
        view = self.window.active_view()

        view.set_scratch(True)
        view.settings().set('highlight_line', False)

        import mediaplayer
        mediaplayer.setup_pyglet()
        # import mediaplayer.viewimage
        # reload(mediaplayer.viewimage)
        from mediaplayer.viewimage import Animation

        try:
            # image = Animation(os.path.join(package_dir, 'example/dinosaur.gif'))
            file_name = file_name.replace('$', package_dir)
            image = Animation(file_name)
            info = image.get_image_for_view(0)
            self.write_tm_file(info['theme_file'], info['theme'])
            self.write_tm_file(info['syntax_file'], info['syntax'])
            self.wait_tm_caching([])
        except IOError:
            raise
        # view.run_command('insert', {"characters": "0123456789ABCDEF\n\n"})
        view.settings().set('font_size', 1)
        view.settings().set('rulers', [])
        view.set_syntax_file('Packages/' + os.path.basename(package_dir) + '/' + info['syntax_file'])
        view.settings().set('color_scheme', ('Packages/' + os.path.basename(package_dir) + '/' + info['theme_file']))
        # view.run_command('media_player_replace', {"characters": info['content']})
        view.run_command('media_player_replace', {"characters": info['frames'][0]['content']})
        play_animation(view, info['frames'])

    def write_tm_file(self, name, content, remove_cache=True):
        check_cache = True
        fname = os.path.join(package_dir, name)
        cache = fname + '.cache'
        if remove_cache:
            if os.path.exists(cache):
                try:
                    os.unlink(cache)
                except:
                    pass
                check_cache = not os.path.exists(cache)
        with codecs.open(fname, 'w', 'utf-8') as f:
            f.write(content)

    def wait_tm_caching(self, files):
        time.sleep(0.5)


class MediaPlayerReplaceCommand(sublime_plugin.TextCommand):
    def run(self, edit, characters):
        self.view.replace(edit, sublime.Region(0, self.view.size()), characters)
        # self.view.run_command("exit_visual_mode")
        move_cursor(self.view, 0)


def move_cursor(view, point):
    sel_set = view.sel()
    sel_set.clear()
    sel_set.add(sublime.Region(point, point))
    view.show(point)
