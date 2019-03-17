#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0') 
from gi.repository import Gtk
import sys
import librosa
import librosa.display
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

# a Gtk ApplicationWindow


class MyWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app

    # get file for analysis
    def get_audio(self, filename):
        #load audio with file
        audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
        audio, sr = librosa.load(audio_file, sr=44100, mono=True, offset=5.0, duration=5.0)
        return audio, sr

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to GNOME", application=app)
        y, sr = self.get_audio('filename')
        # plt.figure()
        # plt.subplot(3, 1, 1)
        self.set_default_size(600, 400)
        f = Figure(figsize=(5, 5), dpi=100)
        # ax = mplfigure.add_subplot(311)
        ax1 = f.add_subplot(212)
        ax1.margin = (2, 2)
        ax1.set_title('One')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        ax1.plot(t, s)
        ax2 = f.add_subplot(211)
        ax2.margin = (2, 2)
        ax2.set_title('Two')
        librosa.display.waveplot(y, sr=sr, ax=ax2)
        import ipdb; ipdb.set_trace()
        # ax2.plot()
        # ax2.add_collection(librosa.display.waveplot(y, sr=sr))

        sw = Gtk.ScrolledWindow()
        import ipdb; ipdb.set_trace()
        self.add(sw)
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)

        # f = Figure(figsize=(5, 5), dpi=100)
        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        sw.add_with_viewport(canvas)
        # plt.title('Monophonic')
        # plt.tight_layout()
        # plt.show()


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
