#!/usr/bin/python3
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import librosa
import librosa.display
from numpy import arange, sin, pi
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.patches as mpatches
from trepan.api import debug
import vlc
UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menu action='FileNew'>
        <menuitem action='FileNewStandard' />
        <menuitem action='FileNewFoo' />
        <menuitem action='FileNewGoo' />
      </menu>
      <menuitem action='FileOpen' />
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditSomething' />
    </menu>
    <menu action='ChoicesMenu'>
      <menuitem action='ChoiceOne'/>
      <menuitem action='ChoiceTwo'/>
      <separator />
      <menuitem action='ChoiceThree'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileQuit' />
  </toolbar>
  <popup name='PopupMenu'>
    <menuitem action='EditCopy' />
    <menuitem action='EditPaste' />
    <menuitem action='EditSomething' />
  </popup>
</ui>
"""
# a Gtk ApplicationWindow

class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        #self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        # import ipdb; ipdb.set_trace()
        if not event.inaxes:
            return
        # if event.inaxes != self.ax2.axes: return
        print(event)
        # debug()
        print('%s move_cursor: x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', 
               event.x, event.y, event.xdata, event.ydata))


        x, y = event.xdata, event.ydata
        # update the line positions
        # self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw_idle()


class MyWindow(Gtk.ApplicationWindow):
    # constructor: the title is "Welcome to GNOME" and the window belongs
    # to the application app
    # cursor = None
    audio_file = ""
    # get file for analysis
    def get_audio(self, filename):
        #load audio with file
        self.audio_file = '/home/David/Music/Video/Stitch/maj_min-E.wav'
        audio, sr = librosa.load(self.audio_file, sr=44100, mono=True, offset=5.0, duration=5.0)
        return audio, sr

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Welcome to GNOME", application=app)
        self.y, self.sr = self.get_audio('filename')
        self.set_default_size(600, 400)
        self.player_paused=False
        self.is_player_active = False

    def set_boxes_and_events(self):
        'plot 1 place holder'
        f = Figure(figsize=(5, 5), dpi=100)
        self.press = None
        ax1 = f.add_subplot(212)
        ax1.margin = (2, 2)
        ax1.set_title('One')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        ax1.plot(t, s)

        # plot 2 audio waveform
        self.ax2 = f.add_subplot(211)
        self.ax2.margin = (2, 2)
        self.ax2.set_title('Two')
        # see https://librosa.github.io/librosa/generated/librosa.display.waveplot.html#librosa.display.waveplot
        librosa.display.waveplot(self.y, sr=self.sr, ax=self.ax2)

        sw = Gtk.ScrolledWindow()
        # A scrolled window border goes outside the scrollbars and viewport
        sw.set_border_width(10)

        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        sw.add_with_viewport(canvas)
        # c = mpatches.Rectangle((0.5, 0.5), 1, 1, facecolor="green",
                    # edgecolor="red", linewidth=3, alpha=0.5)
        # self.ax2.add_patch(c)
        self.cursor = Cursor(self.ax2)

        self.cidpress = canvas.mpl_connect('button_press_event',self. onclick)
        self.cidmotion = canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)
        self.cidrelease = canvas.mpl_connect('button_release_event', self.on_release)

        # Screen content
        action_group = Gtk.ActionGroup("my_actions")

        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)
        self.add_choices_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)

        toolbar = uimanager.get_widget("/ToolBar")
        box.pack_start(toolbar, False, False, 0)

        eventbox = Gtk.EventBox()
        eventbox.connect("button-press-event", self.on_button_press_event)
        box.pack_start(eventbox, True, True, 0)

        label = Gtk.Label("Right-click to see the popup menu.")
        eventbox.add(label)

        self.popup = uimanager.get_widget("/PopupMenu")
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()
        
        self.play_image = Gtk.Image.new_from_icon_name(
                "gtk-media-play",
                Gtk.IconSize.MENU
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "gtk-media-pause",
                Gtk.IconSize.MENU
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "gtk-media-stop",
                Gtk.IconSize.MENU
            )
        
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)
        
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(300,300)

        self.draw_area.modify_bg(Gtk.StateType.NORMAL, Gdk.Color(0, 0, 0))
        
        self.draw_area.connect("realize",self._realized)
        
        self.hbox = Gtk.Box(spacing=6)
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)
        
        #self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        box.pack_start(self.draw_area, True, True, 0)
        box.pack_start(self.hbox, False, False, 0)        # add sw - all matplot stuff
        box.pack_start(sw, True, True, 0)
        self.add(box)
        #{{{ menu methods

    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False
        self.playback_button.set_image(self.play_image)
        
    def toggle_player_playback(self, widget, data=None):

        """
        Handler for Player's Playback Button (Play/Pause).
        """

        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass
        
    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib")
        self.player = self.vlcInstance.media_player_new("--no-xlib")
        self.player = vlc.MediaPlayer('/home/David/Music/Video/Stitch/maj_min-E.wav')
        #self.player = vlc.MediaPlayer('/home/David/Music/Video/Stitch/maj_min-E.wav')
        win_id = widget.get_window().get_xid()
        self.win_id = win_id
        # print(widget)
        # print(win_id)
        self.player.set_xwindow(win_id)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)

        action_new = Gtk.Action("FileNewStandard", "_New",
            "Create a new file", Gtk.STOCK_NEW)
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action_with_accel(action_new, None)

        action_group.add_actions([
            ("FileNewFoo", None, "New Foo", None, "Create new foo",
             self.on_menu_file_new_generic),
            ("FileNewGoo", None, "_New Goo", None, "Create new goo",
             self.on_menu_file_new_generic),
        ])

        action_fileopen = Gtk.Action("FileOpen", None, None, Gtk.STOCK_OPEN)
        action_fileopen.connect("activate", self.on_menu_file_open)
        action_group.add_action(action_fileopen)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def add_edit_menu_actions(self, action_group):
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             self.on_menu_others),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             self.on_menu_others),
            ("EditSomething", None, "Something", "<control><alt>S", None,
             self.on_menu_others)
        ])

    def add_choices_menu_actions(self, action_group):
        action_group.add_action(Gtk.Action("ChoicesMenu", "Choices", None,
            None))

        action_group.add_radio_actions([
            ("ChoiceOne", None, "One", None, None, 1),
            ("ChoiceTwo", None, "Two", None, None, 2)
        ], 1, self.on_menu_choices_changed)

        three = Gtk.ToggleAction("ChoiceThree", "Three", None, None)
        three.connect("toggled", self.on_menu_choices_toggled)
        action_group.add_action(three)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected.")

    def on_menu_file_open(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.player.stop()
            audio_file = dialog.get_filename()
            mrl = "{}".format(audio_file)
            self.player = self.vlcInstance.media_player_new("--no-xlib")
            self.player = vlc.MediaPlayer(audio_file)
            win_id = dialog.get_window().get_xid()
            self.player.set_xwindow(self.win_id)

            self.player.play()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

    def add_filters(self, dialog):

        filter = Gtk.FileFilter()
        filter.set_name("Music files")
        filter.add_pattern("*.wav")
        filter.add_pattern("*.mp3")
        filter.add_pattern("*.mp4")
        dialog.add_filter(filter)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_pattern("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)        
    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def on_menu_choices_changed(self, widget, current):
        print(current.get_name() + " was selected.")

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            print(widget.get_name() + " activated")
        else:
            print(widget.get_name() + " deactivated")

#}}}
    def on_button_press_event(self, widget, event):
        # Check if right mouse button was preseed
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True # event has been handled
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
        # win.do_stuff
        win.set_boxes_and_events()
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
