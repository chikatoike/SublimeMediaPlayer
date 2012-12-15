import sys


def setup_pyglet():
    dummy_argv = not hasattr(sys, 'argv')
    if dummy_argv:
        sys.argv = ['pyglet caption']

    import pyglet

    # pyglet/window/__init__.py
    if pyglet.gl._shadow_window is None:
        pyglet.gl._create_shadow_window()

    if dummy_argv:
        del sys.argv
