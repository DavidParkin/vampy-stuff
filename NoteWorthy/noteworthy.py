#!/usr/bin/python3
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import librosa
import librosa.display
from numpy import arange, sin, pi
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.patches as mpatches

# a Gtk ApplicationWindow

class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        # import ipdb; ipdb.set_trace()
        if not event.inaxes:
            return
        # if event.inaxes != self.ax2.axes: return
        print(event)
        print('%s move_cursor: x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', 
               event.x, event.y, event.xdata, event.ydata))


        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))


class MyWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app
    # cursor = None
    # get file for analysis
    def get_audio(self, filename):
        #load audio with file
        audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
        audio, sr = librosa.load(audio_file, sr=44100, mono=True, offset=5.0, duration=5.0)
        return audio, sr

    # def onclick(self, event):
        # self.cursor.mouse_move(event)
        # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            # ('double' if event.dblclick else 'single', event.button,
            # event.x, event.y, event.xdata, event.ydata))

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to GNOME", application=app)
        y, sr = self.get_audio('filename')
        self.set_default_size(600, 400)
        f = Figure(figsize=(5, 5), dpi=100)
        # ax = mplfigure.add_subplot(311)
        canvas = FigureCanvas(f)
        self.add(canvas)
        self.press = None

        # {{{def onclick(event):
            # # 'on button press we will see if the mouse is over us and store some data'
            # if event.inaxes != self.ax2.axes: return

            # print('%s click_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                # ('double' if event.dblclick else 'single', event.button,
                # event.x, event.y, event.xdata, event.ydata))
            # self.press = event.xdata, event.ydata
            # # import ipdb; ipdb.set_trace()
            # self.ax2.axes.axvline(event.xdata,color='k')
            # old_xdata = event.xdata
            # self.ax2.axes.figure.canvas.draw()
            # self.ax2.figure.canvas.draw_idle()

        # def on_release(event):
            # print('%s release_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                # ('double' if event.dblclick else 'single', event.button,
                # event.x, event.y, event.xdata, event.ydata))
            # canvas.mpl_disconnect(self.cidmotion)
            # self.press = None

        # def on_motion(event):
            # if self.press is None: return
            # # import ipdb; ipdb.set_trace()
            # if event.inaxes != self.ax2.axes: return
            # print('%s move_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                # ('double' if event.dblclick else 'single', event.button,
                # event.x, event.y, event.xdata, event.ydata))

            # x, y = event.xdata, event.ydata
            # # update the line positions
            # self.cursor.lx.set_ydata(y)
            # self.cursor.ly.set_xdata(x)

            # self.cursor.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            # # import ipdb; ipdb.set_trace()
            # self.ax2.axes.figure.canvas.draw()
            #}}} self.ax2.figure.canvas.draw_idle()

        # cid = f.callbacks.connect('button_press_event', self.onclick)
        print (canvas)
        import ipdb; ipdb.set_trace()
        self.cidpress = canvas.mpl_connect('button_press_event', self.onclick)
        self.cidmotion = canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cidrelease = canvas.mpl_connect('button_release_event', self.on_release)
        ax1 = f.add_subplot(212)
        ax1.margin = (2, 2)
        ax1.set_title('One')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        ax1.plot(t, s)
        self.ax2 = f.add_subplot(211)
        self.ax2.margin = (2, 2)
        self.ax2.set_title('Two')
        self.ax2.set_facecolor('red')
        # see https://librosa.github.io/librosa/generated/librosa.display.waveplot.html#librosa.display.waveplot
        librosa.display.waveplot(y, sr=sr, ax=self.ax2)

        sw = Gtk.ScrolledWindow()
        # import ipdb; ipdb.set_trace()
        # self.add(sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)

        # f = Figure(figsize=(5, 5), dpi=100)
        # canvas = FigureCanvas(f)  # a gtk.DrawingArea
        sw.add_with_viewport(canvas)
        c = mpatches.Rectangle((0.5, 0.5), 1, 1, facecolor="green",
                    edgecolor="red", linewidth=3, alpha=0.5)
        self.cursor = Cursor(self.ax2)
        self.ax2.add_patch(c)

        print (canvas)
        import ipdb; ipdb.set_trace()
        self.cidpress = canvas.mpl_connect('button_press_event',self. onclick)
        self.cidmotion = canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.cidrelease = canvas.mpl_connect('button_release_event', self.on_release)

    def onclick(self, event):
        # 'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.ax2.axes: return

        print('%s click_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
              event.x, event.y, event.xdata, event.ydata))
        self.press = event.xdata, event.ydata
        # import ipdb; ipdb.set_trace()
        self.ax2.axes.axvline(event.xdata,color='k')
        old_xdata = event.xdata
        self.ax2.axes.figure.canvas.draw()
        self.ax2.figure.canvas.draw_idle()

    def on_release(self, event):
        print('%s release_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
              event.x, event.y, event.xdata, event.ydata))
        # canvas.mpl_disconnect(self.cidmotion)
        self.press = None

    def on_motion(self, event):
        if self.press is None: return
        # import ipdb; ipdb.set_trace()
        if event.inaxes != self.ax2.axes: return
        print('%s move_init: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
            ('double' if event.dblclick else 'single', event.button,
            event.x, event.y, event.xdata, event.ydata))

        x, y = event.xdata, event.ydata
        # update the line positions    
        self.cursor.lx.set_ydata(y)
        import ipdb; ipdb.set_trace()
        self.cursor.ly.set_xdata(x)

        self.cursor.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        # import ipdb; ipdb.set_trace()
        # not drawing
        self.ax2.axes.figure.canvas.draw()
        self.ax2.figure.canvas.draw_idle()


class MyApplication(Gtk.Application):
    # constructor of the Gtk Application

    def __init__(self):
        Gtk.Application.__init__(self)

    # create and activate a MyWindow, with self (the MyApplication) as
    # application the window belongs to.
    # Note that the function in C activate() becomes do_activate() in Python
    def do_activate(self):
        win = MyWindow(self)
        # show the window and all its content
        # this line could go in the constructor of MyWindow as well
        # f = Figure(figsize=(5, 5), dpi=100)
        # canvas = FigureCanvas(f)  # a gtk.DrawingArea
        # win.add(canvas)
        win.show_all()

    # start up the application
    # Note that the function in C startup() becomes do_startup() in Python
    def do_startup(self):
        Gtk.Application.do_startup(self)

# create and run the application, exit with the value returned by
# running the program
app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
